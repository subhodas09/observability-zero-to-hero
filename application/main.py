import json
import time

from fastapi import FastAPI, HTTPException, Request
from prometheus_client import Counter, Histogram, make_asgi_app

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleSpanProcessor,
)
from opentelemetry.trace import Status, StatusCode


# ---------------------------------------------------------
# Application
# ---------------------------------------------------------

app = FastAPI(title="Observability Zero to Hero")


# ---------------------------------------------------------
# Tracing
# ---------------------------------------------------------

resource = Resource.create(
    {
        "service.name": "lab00-api",
    }
)

tracer_provider = TracerProvider(resource=resource)

tracer_provider.add_span_processor(
    SimpleSpanProcessor(
        ConsoleSpanExporter()
    )
)

trace.set_tracer_provider(tracer_provider)

tracer = trace.get_tracer("lab00")


# ---------------------------------------------------------
# Metrics
# ---------------------------------------------------------

REQUEST_COUNT = Counter(
    "lab00_http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)

REQUEST_DURATION = Histogram(
    "lab00_http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["endpoint"],
)


# ---------------------------------------------------------
# Observability middleware
# ---------------------------------------------------------

@app.middleware("http")
async def observe_request(request: Request, call_next):
    start_time = time.perf_counter()

    span_name = f"{request.method} {request.url.path}"

    with tracer.start_as_current_span(span_name) as span:
        span.set_attribute("http.request.method", request.method)
        span.set_attribute("url.path", request.url.path)

        response = await call_next(request)

        duration = time.perf_counter() - start_time

        status = response.status_code

        span.set_attribute("http.response.status_code", status)
        span.set_attribute("request.duration_seconds", duration)

        if status >= 500:
            span.set_status(
                Status(
                    StatusCode.ERROR,
                    "HTTP server error",
                )
            )

        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status=str(status),
        ).inc()

        REQUEST_DURATION.labels(
            endpoint=request.url.path
        ).observe(duration)

        context = span.get_span_context()

        log_record = {
            "event": "http_request_completed",
            "method": request.method,
            "path": request.url.path,
            "status": status,
            "duration_seconds": round(duration, 4),
            "trace_id": format(context.trace_id, "032x"),
            "span_id": format(context.span_id, "016x"),
        }

        print(json.dumps(log_record))

        return response


# ---------------------------------------------------------
# Endpoints
# ---------------------------------------------------------

@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/slow")
def slow():
    time.sleep(2)
    return {"message": "That was intentionally slow"}


@app.get("/error")
def error():
    raise HTTPException(
        status_code=500,
        detail="Intentional LAB 00 failure",
    )


# Prometheus-compatible metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)
