import logging
import os

import redis

from constants import EMAG_REDIS_URL_KEY, EMAG_SPIDER_PRODUCTS
from main import crawl

if __name__ == "__main__":
    # Spider name
    spider_name = EMAG_SPIDER_PRODUCTS

    # Redis check for urls to crawl
    r = redis.Redis.from_url(os.getenv("REDIS_URL"), decode_responses=True)
    url_key = EMAG_REDIS_URL_KEY
    count = r.scard(url_key)

    # Crawl all in queue
    if count == 0:
        logging.warning(f"[Main->Products] {url_key} has no urls to crawl!")
    else:
        for val in range(count):
            try:
                crawl(spider_name)
                logging.info(
                    f"[Main->Products] Finished crawling {spider_name} on {url_key}:{val}"
                )
                logging.info("─" * 82)

            except Exception as error:
                logging.error(error)

    # Move log file
    # TODO: do a cron job
    # if os.path.isfile("./scrapy.log"):
    #     logging.info("[Main->Products] Copy scrapy.log file to ./logs")
    #     shutil.copyfile(
    #         "./scrapy.log",
    #         f"./logs/scrapy_{datetime.now().astimezone().strftime('%Y-%m-%d')}.log",
    #     )

    # EOF
    logging.info("─" * 91)
