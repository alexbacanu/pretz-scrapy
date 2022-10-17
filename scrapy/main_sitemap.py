import logging

from main import crawl
from pretz.settings import SPIDER_SITEMAP

if __name__ == "__main__":
    # Spider name
    spider_name = SPIDER_SITEMAP

    # Crawl all sitemaps
    try:
        crawl(spider_name)
        logging.info(f"[Main->Sitemap] Finished crawling {spider_name}")
        logging.info("─" * 82)

    except Exception as error:
        logging.warning(f"[Main->Sitemap] {spider_name} has encountered an error!")
        logging.error(error)

    # EOF
    logging.info("─" * 91)
