import logging

from constants import SPIDER_SITEMAP
from main import crawl

if __name__ == "__main__":
    # Spider name
    spider_name = SPIDER_SITEMAP

    # Crawl all sitemaps
    try:
        crawl(spider_name)
        logging.info(f"[Main->Sitemap] Finished crawling {spider_name}")

    except Exception as error:
        logging.error(error)

    # EOF
    logging.info("─" * 91)
