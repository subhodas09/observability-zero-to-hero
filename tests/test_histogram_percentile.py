import unittest

from tools.histogram_percentile import (
    Bucket,
    estimate_percentile,
    parse_direct_buckets,
    parse_percentiles,
    parse_prometheus,
)


class HistogramPercentileTests(unittest.TestCase):
    def test_p75_interpolates_to_point_4167_seconds(self):
        buckets = parse_direct_buckets("0.10:10,0.25:22,0.50:34,1.00:40")

        estimate = estimate_percentile(buckets, 75)

        self.assertAlmostEqual(estimate.value, 0.4166666667)
        self.assertEqual(estimate.target, 30)
        self.assertEqual(estimate.bucket_count, 12)

    def test_p80_interpolates_to_point_45_seconds(self):
        buckets = parse_direct_buckets("0.10:12,0.25:28,0.50:43,1.00:50")

        estimate = estimate_percentile(buckets, 80)

        self.assertAlmostEqual(estimate.value, 0.45)
        self.assertEqual(estimate.position, 12)
        self.assertEqual(estimate.fraction, 0.8)

    def test_prometheus_delay_series_is_selected_by_label(self):
        exposition = """
# TYPE lab00_http_request_duration_seconds histogram
lab00_http_request_duration_seconds_bucket{endpoint="/delay",le="0.1"} 2
lab00_http_request_duration_seconds_bucket{endpoint="/delay",le="0.25"} 6
lab00_http_request_duration_seconds_bucket{endpoint="/delay",le="0.5"} 9
lab00_http_request_duration_seconds_bucket{endpoint="/delay",le="1.0"} 10
lab00_http_request_duration_seconds_bucket{endpoint="/delay",le="+Inf"} 10
lab00_http_request_duration_seconds_count{endpoint="/delay"} 10
lab00_http_request_duration_seconds_bucket{endpoint="/health",le="0.1"} 20
lab00_http_request_duration_seconds_bucket{endpoint="/health",le="+Inf"} 20
lab00_http_request_duration_seconds_count{endpoint="/health"} 20
"""

        buckets, total, labels = parse_prometheus(
            exposition,
            "lab00_http_request_duration_seconds",
            {"endpoint": "/delay"},
        )
        estimate = estimate_percentile(buckets, 95, total)

        self.assertEqual(total, 10)
        self.assertEqual(labels, {"endpoint": "/delay"})
        self.assertAlmostEqual(estimate.value, 0.75)

    def test_numeric_and_prefixed_percentiles_are_accepted(self):
        self.assertEqual(parse_percentiles(["p50,80,p99"]), [50, 80, 99])

    def test_decreasing_cumulative_counts_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "must not decrease"):
            parse_direct_buckets("0.1:10,0.5:9")

    def test_empty_histogram_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "empty histogram"):
            estimate_percentile([Bucket(0.1, 0)], 50)

    def test_multiple_matching_series_require_more_labels(self):
        exposition = """
metric_bucket{endpoint="/a",le="1"} 1
metric_bucket{endpoint="/a",le="+Inf"} 1
metric_count{endpoint="/a"} 1
metric_bucket{endpoint="/b",le="1"} 1
metric_bucket{endpoint="/b",le="+Inf"} 1
metric_count{endpoint="/b"} 1
"""
        with self.assertRaisesRegex(ValueError, "more than one histogram series"):
            parse_prometheus(exposition, "metric", {})


if __name__ == "__main__":
    unittest.main()
