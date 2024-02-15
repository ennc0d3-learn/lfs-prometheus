import logging
import sys

import psutil

from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY, CounterMetricFamily
from prometheus_client.registry import Collector
import signal


class CPUMetricCollector(Collector):
    """CPU metric collector"""

    def collect(self):
        """Collect CPU metrics"""
        logging.info("Collecting CPU metrics")
        counter = CounterMetricFamily(
            "cpu_usage_seconds_total", "Total CPU usage in seconds", labels=["mode"]
        )
        for mode, value in psutil.cpu_times()._asdict().items():
            counter.add_metric([mode], value)
        yield counter


def run():
    # Start the prometheus server
    port = 8100
    logging.info(f"Starting the server on port {port}")
    if sys.argv[1:]:
        port = int(sys.argv[1])
    REGISTRY.register(CPUMetricCollector())
    print("Starting the server on port", port)
    server, t = start_http_server(port)
    server.serve_forever()


if __name__ == "__main__":
    print("Starting the CPU metrics exporter")
    run()
