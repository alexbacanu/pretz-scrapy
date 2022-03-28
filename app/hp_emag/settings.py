#  Scrapy settings for hp_emag project
#
BOT_NAME = "hp_emag"

SPIDER_MODULES = ["hp_emag.spiders"]
NEWSPIDER_MODULE = "hp_emag.spiders"

#  Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "hp_emag/0.5 (Windows NT 10.0; Win64; x64)"

#  Obey robots.txt rules
#  TODO: Turn this to True when we don't use proxy
ROBOTSTXT_OBEY = False

#  Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 4

#  Configure a delay for requests for the same website (default: 0)
DOWNLOAD_DELAY = 2
#  The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16
#  Retries
RETRY_TIMES = 6

#  Disable cookies (enabled by default)
COOKIES_ENABLED = False

#  Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

#  Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#     "Accept-Language": "en",
# }

#  Enable or disable spider middlewares
# SPIDER_MIDDLEWARES = {
#     "hp_emag.middlewares.StartUrlsMiddleware": 100,
# }

#  Enable or disable downloader middlewares
# DOWNLOADER_MIDDLEWARES = {
#     "hp_emag.middlewares.HpEmagDownloaderMiddleware": 543,
# }

#  Enable or disable extensions
EXTENSIONS = {
    "scrapy.extensions.telnet.TelnetConsole": None,
}

#  Configure item pipelines
# ITEM_PIPELINES = {
#     "hp_emag.pipelines.DefaultValuesPipeline": 100,
#     "hp_emag.pipelines.RedisPipelineProductsTS": 110,
#     "hp_emag.pipelines.RedisPipelineProductsJSON": 111,
# }

#  Enable and configure the AutoThrottle extension (disabled by default)
AUTOTHROTTLE_ENABLED = True
#  The initial download delay
AUTOTHROTTLE_START_DELAY = 2
#  The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
#  The average number of requests Scrapy should be sending in parallel to each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
#  Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

#  Enable and configure HTTP caching (disabled by default)
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 3600
HTTPCACHE_DIR = ".httpcache"
HTTPCACHE_IGNORE_HTTP_CODES = ["400", "401", "403", "404", "500", "504"]
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
