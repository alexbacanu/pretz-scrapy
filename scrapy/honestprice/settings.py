#  Scrapy settings for honestprice project
#

BOT_NAME = "honestprice"

SPIDER_MODULES = ["honestprice.spiders"]
NEWSPIDER_MODULE = "honestprice.spiders"

#  Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "honestprice/0.6 (Windows NT 10.0; Win64; x64)"

#  Obey robots.txt rules
ROBOTSTXT_OBEY = True

#  Disable cookies (enabled by default)
COOKIES_ENABLED = False

#  Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

#  Enable or disable spider middlewares
SPIDER_MIDDLEWARES = {
    # "honestprice.middlewares.HonestpriceSpiderMiddleware": 543,
}

#  Enable or disable downloader middlewares
DOWNLOADER_MIDDLEWARES = {
    "honestprice.middlewares.ScrapeAPIProxyMiddleware": 130,
    "scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware": 170,
    # "honestprice.middlewares.HonestpriceDownloaderMiddleware": 543,
}

#  Enable or disable extensions
EXTENSIONS = {
    "scrapy.extensions.telnet.TelnetConsole": None,
}

#  Configure item pipelines
# ITEM_PIPELINES = {
#     "honestprice.pipelines.DefaultValuesPipeline": 150,
# }

#  Enable and configure the AutoThrottle extension (disabled by default)
AUTOTHROTTLE_ENABLED = True
#  The initial download delay
AUTOTHROTTLE_START_DELAY = 5
#  The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
#  The average number of requests Scrapy should be sending in parallel
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
#  Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

#  Enable and configure HTTP caching (disabled by default)
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 14400
HTTPCACHE_DIR = "/tmp"
HTTPCACHE_IGNORE_HTTP_CODES = ["400", "401", "403", "404", "500", "504", "511"]
HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

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
START_URLS_COUNT = 1
RETRY_TIMES = 6
DOWNLOAD_DELAY = 5  # Default: 0
CONCURRENT_REQUESTS = 4  # Default: 16