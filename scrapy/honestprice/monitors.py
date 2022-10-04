import math

from spidermon import Monitor, MonitorSuite, monitors


@monitors.name("Item count")
class ItemCountMonitor(Monitor):
    @monitors.name("Minimum number of items")
    def test_minimum_number_of_items(self):
        item_extracted = getattr(self.data.stats, "item_scraped_count", 0)
        minimum_threshold = 1

        msg = "Extracted less than {} items".format(minimum_threshold)
        self.assertTrue(item_extracted >= minimum_threshold, msg=msg)

    @monitors.name("Items collected vs reported")
    def test_collected_vs_reported_items(self):
        items_scraped = getattr(self.data.stats, "item_scraped_count", 0)
        items_reported = getattr(self.data.stats, "item_reported_count", 0)

        msg = f"Values do not match ({items_scraped} vs {items_reported})"
        self.assertTrue(
            # 5% tolerance when comparing
            math.isclose(items_scraped, items_reported, rel_tol=0.05),
            msg=msg,
        )


class SpiderCloseMonitorSuite(MonitorSuite):

    monitors = [
        ItemCountMonitor,
    ]
