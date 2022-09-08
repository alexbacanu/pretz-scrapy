#  Scrapy settings for honestprice project

BOT_NAME = "honestprice"

SPIDER_MODULES = ["honestprice.spiders"]
NEWSPIDER_MODULE = "honestprice.spiders"

#  Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "honestprice/0.9 (Windows NT 10.0; Win64; x64)"

#  Obey robots.txt rules
ROBOTSTXT_OBEY = True

#  Enable cookies
COOKIES_ENABLED = True
# COOKIES_DEBUG = True

#  Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

#  Enable or disable spider middlewares
# SPIDER_MIDDLEWARES = {}

#  Enable or disable downloader middlewares
DOWNLOADER_MIDDLEWARES = {
    "honestprice.middlewares.EmagCookiesMiddleware": 200,
    "honestprice.middlewares.ScrapeDoProxyMiddleware": 120,
    # "honestprice.middlewares.ScrapeAPIProxyMiddleware": 120,
    # "honestprice.middlewares.WebShareProxyMiddleware": 120,
    # "honestprice.middlewares.ProxyPageProxyMiddleware": 120,
    # "honestprice.middlewares.ProxiesAPIProxyMiddleware": 120,
    # "scrapy.downloadermiddlewares.retry.RetryMiddleware": None,
    # "honestprice.middlewares.RetryHTTPErrors": 300,
}

#  Enable or disable extensions
EXTENSIONS = {
    "scrapy.extensions.telnet.TelnetConsole": None,
    "spidermon.contrib.scrapy.extensions.Spidermon": 500,
}

#  Enable Spidermon
SPIDERMON_ENABLED = True
SPIDERMON_SPIDER_CLOSE_MONITORS = "honestprice.monitors.SpiderCloseMonitorSuite"

#  Configure item pipelines
# ITEM_PIPELINES = {}

#  Enable and configure the AutoThrottle extension (disabled by default)
AUTOTHROTTLE_ENABLED = True
#  The initial download delay
AUTOTHROTTLE_START_DELAY = 5
#  The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
#  The average number of requests Scrapy should be sending in parallel
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
#  Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = True

#  Settings for requests (between requests)
DOWNLOAD_DELAY = 5  # Default: 0
CONCURRENT_REQUESTS = 4  # Default: 16

#  Enable and configure HTTP caching (disabled by default)
#  TODO: Test, might not see a difference in Cloud Functions
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 14400
HTTPCACHE_DIR = "/tmp"
HTTPCACHE_IGNORE_HTTP_CODES = ["400", "401", "403", "404", "499", "500", "504", "511"]
HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

#  Retry Middleware
RETRY_ENABLED = True
RETRY_HTTP_CODES = [500, 502, 503, 504, 511, 522, 524, 408, 429, 499]
RETRY_TIMES = 6

#  Log related
LOG_ENABLED = True
LOG_LEVEL = "INFO"
# LOG_FILE = "scrapy.log"

#  Disable redirect
REDIRECT_ENABLED = False
METAREFRESH_ENABLED = False

#  Crawl in BFO order to save memory
DEPTH_PRIORITY = 1
SCHEDULER_DISK_QUEUE = "scrapy.squeues.PickleFifoDiskQueue"
SCHEDULER_MEMORY_QUEUE = "scrapy.squeues.FifoMemoryQueue"

#  Custom settings
# START_URLS_COUNT = 4
