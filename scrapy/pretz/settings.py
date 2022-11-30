import os

from dotenv import load_dotenv

load_dotenv()

BOT_NAME = "pretz"

SPIDER_MODULES = ["pretz.spiders"]
NEWSPIDER_MODULE = "pretz.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "pretz/1.0 (Windows NT 10.0; Win64; x64)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

#  Enable cookies
COOKIES_ENABLED = True
# COOKIES_DEBUG = True

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# SPIDER_MIDDLEWARES = {
#    'pretz.middlewares.PretzSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
DOWNLOADER_MIDDLEWARES = {
    "pretz.middlewares.ScrapeDoMiddleware": 120,
    "pretz.middlewares.FailedUrlsMiddleware": 250,
}

# Enable or disable extensions
EXTENSIONS = {
    "scrapy.extensions.telnet.TelnetConsole": None,
}

# Configure item pipelines
# ITEM_PIPELINES = {
#    'pretz.pipelines.PretzPipeline': 300,
# }

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1
DOWNLOAD_DELAY = 4

# Enable and configure the AutoThrottle extension (disabled by default)
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 4
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 20
# The average number of requests Scrapy should be sending in parallel to each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 25200
HTTPCACHE_DIR = "/tmp"
HTTPCACHE_IGNORE_HTTP_CODES = ["400", "401", "403", "404", "499", "500", "504", "511"]
HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

# Retry Middleware
RETRY_ENABLED = True
RETRY_HTTP_CODES = [500, 502, 503, 504, 511, 522, 524, 408, 429, 499]
RETRY_TIMES = 6

# Log related
LOG_ENABLED = True
LOG_LEVEL = "INFO"
LOG_FILE = "scrapy.log"

# Disable redirect
REDIRECT_ENABLED = False
METAREFRESH_ENABLED = False

# Crawl in BFO order to save memory
DEPTH_PRIORITY = 1
SCHEDULER_DISK_QUEUE = "scrapy.squeues.PickleFifoDiskQueue"
SCHEDULER_MEMORY_QUEUE = "scrapy.squeues.FifoMemoryQueue"

# App specific
DEV_TAG = "_dev"  # !DEV TAG
SCRAPEDO_KEY = f"{os.getenv('SCRAPEDO_KEY')}"

MONGO_URI = f"{os.getenv('MONGO_URI')}"
MONGO_DB = f"{os.getenv('MONGO_DB')}{DEV_TAG}"
MONGO_COLL = f"{os.getenv('MONGO_COLL')}{DEV_TAG}"

REDIS_URI = f"{os.getenv('REDIS_URI')}"

MAX_IDLE_TIME = 5
