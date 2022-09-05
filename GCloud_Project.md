# Pretz

## _Google Cloud Project_

History of a gcloud project.

## Installation

For production environments...

#### Create Firebase project using Firebase CLI

```sh
firebase init
```

#### Select only functions when asked which Firebase features we want to set up

```sh
(*) Functions: Configure a Cloud Functions directory and its files
```

#### Select Create a new project

```sh
(*) Create a new project
```

#### Select a name

```sh
pretz-gcloud
```

#### What would you like to call your project? **Leave empty**

```sh

```

#### Language

```sh
Typescript
```

#### Enable Billing (MANUALLY) on console.firebase.google.com (Pay as you go)

#### Enable Cloud Firestore (MANUALLY) on console.firebase.google.com

#### Use GCloud init (to set project and username)

#### Create pubsub Topic

```sh
gcloud pubsub topics create pub-crawl-emag
```

#### Create scheduler (enable the API if requested)

```sh
gcloud scheduler jobs create pubsub sch-sitemap-emag --schedule="0 8 * * *" --topic=pub-crawl-emag --message-body="emag_sitemap" --time-zone="Europe/Bucharest" --max-retry-attempts="5" --max-retry-duration="5m" --min-backoff="5m" --max-backoff="25m" --max-doublings="15"
```

#### Create Task queue (enable the API if requested)

```sh
gcloud tasks queues create tsk-crawl-emag --max-dispatches-per-second=4 --max-concurrent-dispatches=4 --max-attempts=5 --max-retry-duration=300s --max-doublings=15 --min-backoff=300s --max-backoff=1500s
```

#### Create Function (enable the API if requested)

```sh
gcloud functions deploy fnc-scrapy-stores --gen2 --runtime=python310 --region=europe-west3 --source=. --entry-point=crawl_pubsub --trigger-topic=pub-crawl-emag --memory=512 --timeout=600 --max-instances=50 --env-vars-file .env.yaml
```

# Default region

> europe-west3

# GCloud namings

[x] Scheduler: sch-sitemap-emag
[ ] Scheduler: sch-sitemap-altex
[x] Pub/Sub: pub-crawl-emag
[ ] Pub/Sub: pub-crawl-altex
[x] Tasks: tsk-crawl-emag
[ ] Tasks: tsk-crawl-altex
[x] Functions: fnc-scrapy-stores
