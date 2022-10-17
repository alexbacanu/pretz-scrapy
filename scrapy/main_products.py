import logging

from main import crawl
from pretz.settings import SPIDER_PRODUCTS

if __name__ == "__main__":
    # Spider name
    spider_name = SPIDER_PRODUCTS

    # Crawl all products
    while True:
        try:
            crawl(spider_name)
            logging.info(f"[Main->Products] Finished crawling {spider_name}")
            logging.info("─" * 82)

        except Exception as error:
            logging.warning(f"[Main->Products] {spider_name} has no urls to crawl!")
            logging.error(error)
            break

    # EOF
    logging.info("─" * 91)
