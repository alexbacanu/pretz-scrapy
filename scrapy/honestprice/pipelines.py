# Define your item pipelines here
import base64
import datetime
import json
import os

import typesense
from google.cloud import firestore, tasks_v2
from google.protobuf import duration_pb2, timestamp_pb2


class DefaultValuesPipeline(object):
    def process_item(self, item, spider):
        # Set default values to null for all fields
        for field in item.fields:
            item.setdefault(field, None)
            item.setdefault("productStars", 0)
            item.setdefault("productReviews", 0)
        return item


class FirestoreAutoWriteBatch:
    def __init__(self, batch, limit=498, auto_commit=True):
        self._total = 0
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
        self._total += self._count
        self._batch.commit()
        self._count = 0

    def commit_if_limit(self):
        if self._count > self._limit:
            self._total += self._count
            self._batch.commit()
            self._count = 0

    def total_commited(self):
        print("---------------------------------")
        print(f"count_firestore:    {self._total}")


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
        self.fdb.collection("startUrls").document("emgStart").set(data)


class GoogleFirestoreProductsPipeline:
    def __init__(self):
        # Initialize Firestore Client
        self.fdb = firestore.Client()
        self.batch = FirestoreAutoWriteBatch(self.fdb.batch())

    def process_item(self, item, spider):
        # Get current time as "2022-09-02"
        date_time = (
            datetime.datetime.now(datetime.timezone.utc).astimezone()
        ).strftime("%Y-%m-%d")

        # Reference to emag_products collection
        products_ref = self.fdb.collection("products").document(
            f"emg{item['productID']}"
        )

        # Set new dict
        timeseries = {
            "timeseries": {
                date_time: {
                    "priceDate": item["crawledAt"],
                    "productPrice": item["productPrice"],
                    "retailPrice": item["retailPrice"],
                    "slashedPrice": item["slashedPrice"],
                    "usedPrice": item["usedPrice"],
                }
            }
        }

        # Reference a new dict
        new_dict = dict(item)

        # Update new dict
        new_dict.update(timeseries)

        # Add data to batch
        self.batch.set(products_ref, new_dict, merge=True)

        return item

    def close_spider(self, spider):
        # Commit batch
        self.batch.commit()

        # Print how many were commited to firestore db
        self.batch.total_commited()


class GoogleTasksPipeline:
    def __init__(self):
        # Variables
        self.project = os.getenv("TASKS_PROJECT")
        self.queue = os.getenv("TASKS_QUEUE")
        self.location = os.getenv("TASKS_LOCATION")
        self.url = os.getenv("TASKS_URL")
        self.service_account = os.getenv("TASKS_SA")
        self.in_seconds = 180
        self.deadline = 900
        self.http_post = tasks_v2.HttpMethod.POST

        # Create a client.
        self.client = tasks_v2.CloudTasksClient()

        # Construct the fully qualified queue name.
        self.parent = self.client.queue_path(self.project, self.location, self.queue)

    def process_item(self, item, spider):
        # Don't make this hard coded
        spider_name = spider.for_spider

        spider_b64 = base64.b64encode(spider_name.encode("utf-8")).decode("ascii")
        url_b64 = base64.b64encode(item["response_url"].encode("utf-8")).decode("ascii")

        payload = {
            "message": {
                "data": spider_b64,
                "url": url_b64,
            }
        }

        task = {
            "http_request": {
                "http_method": self.http_post,
                "url": self.url,
                "oidc_token": {
                    "service_account_email": self.service_account,
                },
            }
        }

        if payload is not None:
            if isinstance(payload, dict):
                # Convert dict to JSON string
                payload = json.dumps(payload)

                # Specify http content-type to application/json
                task["http_request"]["headers"] = {
                    "Content-type": "application/json",
                    "ce-id": "1234567890",
                    "ce-specversion": "1.0",
                    "ce-type": "google.cloud.pubsub.topic.v1.messagePublished",
                    "ce-source": "//pubsub.googleapis.com/projects/pretz-firebase/topics/scrapy-crawl-emag",
                }

            # The API expects a payload of type bytes.
            converted_payload = payload.encode()

            # Add the payload to the request.
            task["http_request"]["body"] = converted_payload

        if self.in_seconds is not None:
            # Convert "seconds from now" into an rfc3339 datetime string.
            date = datetime.datetime.utcnow() + datetime.timedelta(
                seconds=self.in_seconds
            )

            # Create Timestamp protobuf.
            timestamp = timestamp_pb2.Timestamp()
            timestamp.FromDatetime(date)

            # Add the timestamp to the tasks.
            task["schedule_time"] = timestamp

        # if task_name is not None:
        #     # Add the name to tasks.
        #     task["name"] = self.client.task_path(
        #         self.project, self.location, self.queue, task_name
        #     )

        if self.deadline is not None:
            # Add dispatch deadline for requests sent to the worker.
            duration = duration_pb2.Duration()
            task["dispatch_deadline"] = duration.FromSeconds(self.deadline)

        # Use the client to build and send the task.
        response = self.client.create_task(
            request={"parent": self.parent, "task": task}
        )

        print(f"pipelines.py:   Created task ${response.name}")

        return item


class TypesenseProductsPipeline:
    def __init__(self):
        # Initialize empty documents array
        self.documents = []

        # Initialize Typesense Client
        self.client = typesense.Client(
            {
                "nodes": [
                    {
                        "host": "localhost",  # For Typesense Cloud use xxx.a1.typesense.net
                        "port": "8108",  # For Typesense Cloud use 443
                        "protocol": "http",  # For Typesense Cloud use https
                    }
                ],
                "api_key": "test123",
                "connection_timeout_seconds": 300,
            }
        )

        # Define collection
        self.schema = {
            "name": "typesenseProducts",
            "fields": [
                {
                    "name": "id",
                    "type": "string",
                },
                {
                    "name": "productName",
                    "type": "string",
                },
                {
                    "name": "productCategory",
                    "type": "string",
                },
                {
                    "name": "productImg",
                    "type": "string",
                },
                {
                    "name": "productReviews",
                    "type": "int32",
                },
            ],
            "default_sorting_field": "productReviews",
        }

        # Drop schema
        # self.client.collections["typesenseProducts"].delete()

        # Retreive schema
        # client.collections["typesenseProducts"].retrieve()

        # Create schema
        # client.collections.create(schema)

        # Create schema if it doesn't exist
        try:
            self.client.collections["typesenseProducts"].retrieve()
        except Exception as e:
            if 404 in e.args:
                self.client.collections.create(self.schema)

    def process_item(self, item, spider):
        # Index documents
        self.document = {
            "id": f'emg{item["productID"]}',
            "productName": item["productName"],
            "productPrice": item["productPrice"],
            "productCategory": item["productCategory"],
            "productImg": item["productImg"],
            "productReviews": item["productReviews"],
        }

        self.documents.append(self.document)

        return item

    def close_spider(self, spider):
        # Commit batch
        self.client.collections["typesenseProducts"].documents.import_(
            self.documents, {"action": "upsert"}
        )


class HonestpricePipeline:
    def process_item(self, item, spider):
        return item
