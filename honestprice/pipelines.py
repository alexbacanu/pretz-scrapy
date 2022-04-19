# Define your item pipelines here
#
# pylint: disable=unused-argument
import datetime

from google.cloud import firestore


class DefaultValuesPipeline(object):
    def process_item(self, item, spider):
        # Set default values (0) for all fields
        for field in item.fields:
            item.setdefault(field, 0)
        return item


class FirestoreAutoWriteBatch:
    def __init__(self, batch, limit=498, auto_commit=True):
        self._batch = batch
        self._limit = limit
        self._auto_commit = auto_commit
        self._count = 0

    def create(self, *args, **kwargs):
        self._batch.create(*args, **kwargs)
        self._count += 1

        if self._auto_commit:
            self.commit_if_limit()

    def set(self, *args, **kwargs):
        self._batch.set(*args, **kwargs)
        self._count += 1

        if self._auto_commit:
            self.commit_if_limit()

    def update(self, *args, **kwargs):
        self._batch.update(*args, **kwargs)
        self._count += 1

        if self._auto_commit:
            self.commit_if_limit()

    def delete(self, *args, **kwargs):
        self._batch.delete(*args, **kwargs)
        self._count += 1

        if self._auto_commit:
            self.commit_if_limit()

    def commit(self, *args, **kwargs):
        self._batch.commit()
        self._count = 0

    def commit_if_limit(self):
        if self._count > self._limit:
            self._batch.commit()
            self._count = 0


class AmazonDynamoDBPipeline:
    def process_item(self, item, spider):
        # Save item to Amazon Dynamo DB
        return item


class AzureCosmosDBPipeline:
    def process_item(self, item, spider):
        # Save item to Azure Cosmos DB
        return item


class GoogleFirestoreSitemapPipeline:
    def __init__(self):
        # Initialize Firestore
        self.fdb = firestore.Client()
        self.collected_urls = []

    def process_item(self, item, spider):
        # Collect urls
        self.collected_urls.extend({item["response_url"]})
        return item

    def close_spider(self, spider):
        # Add data to firestore
        data = {"response_url": self.collected_urls}
        self.fdb.collection("emag_start_urls").document("start").set(data)


class GoogleFirestoreProductsPipeline:
    def __init__(self):
        # Initialize Firestore Client
        self.fdb = firestore.Client()
        self.batch = FirestoreAutoWriteBatch(self.fdb.batch())

    def process_item(self, item, spider):
        # Reference to emag_products collection
        products_ref = self.fdb.collection("emag_products").document(item["product_id"])
        timeseries_ref = self.fdb.collection("emag_timeseries").document(item["product_id"])
        date_time = datetime.datetime.now(tz=datetime.timezone.utc).strftime("%Y-%m-%d")

        # Add data to batch
        self.batch.set(products_ref, dict(item))
        self.batch.set(
            timeseries_ref,
            {
                date_time: {
                    "product_id": item["product_id"],
                    "price_rrp": item["price_rrp"],
                    "price_old": item["price_old"],
                    "price_new": item["price_new"],
                }
            },
            merge=True,
        )

        return item

    def close_spider(self, spider):
        # Commit batch
        self.batch.commit()


class HonestpricePipeline:
    def process_item(self, item, spider):
        return item
