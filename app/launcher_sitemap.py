# launcher.py
# See: https://blog.vikfand.com/posts/scrapy-fargate-sls-guide/
import json
import sys

from hp_emag.crawl import crawl


def scrape(event={}, context={}):
<<<<<<< HEAD:app/launcher_sitemap.py
    spider_name = "emag_sitemap"
=======
    spider_name = "emag_products"
>>>>>>> 60b11f5302d2e3386e92fceefdb97af06de00453:app/launcher_products.py
    crawl(spider_name)


if __name__ == "__main__":
    try:
        event = json.loads(sys.argv[1])
    except IndexError:
        event = {}
    scrape(event)
