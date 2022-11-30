import os
import time
from datetime import datetime, timedelta
from decimal import ROUND_DOWN, Decimal

from pretz.settings import DEV_TAG
from pymongo import MongoClient


def main():
    # Debug only
    start = time.time()

    # Initialize PyMongo
    client = MongoClient(os.environ.get("MONGO_URI"))
    db = f"{os.environ.get('MONGO_DB')}{DEV_TAG}"
    coll = f"{os.environ.get('MONGO_COLL')}{DEV_TAG}"

    # Get today's date as 2022-13-11T00:00:00.000
    # *This is UTC
    today = datetime.utcnow().replace(
        hour=0, minute=0, second=0, microsecond=0
    ) + timedelta(days=0)

    # Set pipeline
    pipeline = [
        {
            "$match": {
                # Filter out used items
                "pUsedTag": False,
                "priceCurrent": {"$exists": True},
                # Filter only recent or not updated
                "crawledAt": {"$gte": today},
                "$or": [
                    {"stats.updatedAt": {"$exists": False}},
                    {"stats.updatedAt": {"$lt": today}},
                ],
            }
        },
        {
            "$set": {
                "timeseriesArr": {"$objectToArray": "$timeseries"},
            },
        },
        {
            "$match": {
                "timeseriesArr.v.priceCurrent": {"$exists": True},
            },
        },
        {
            "$set": {
                "stats": {
                    "lowest7": {
                        "$reduce": {
                            "input": {"$reverseArray": "$timeseriesArr"},
                            "initialValue": {
                                "k": {
                                    "$dateSubtract": {
                                        "startDate": {
                                            "$dateTrunc": {
                                                "date": "$crawledAt",
                                                "unit": "day",
                                            }
                                        },
                                        "amount": 15,
                                        "unit": "minute",
                                    }
                                },
                                "v": {"$max": "$timeseriesArr.v.priceCurrent"},
                            },
                            "in": {
                                "$cond": [
                                    {
                                        "$and": [
                                            {
                                                "$lt": [
                                                    {
                                                        "$dateFromString": {
                                                            "dateString": "$$this.k",
                                                            "format": "%Y-%m-%d",
                                                        }
                                                    },
                                                    "$$value.k",
                                                ]
                                            },
                                            {
                                                "$gte": [
                                                    {
                                                        "$dateFromString": {
                                                            "dateString": "$$this.k",
                                                            "format": "%Y-%m-%d",
                                                        }
                                                    },
                                                    {
                                                        "$dateSubtract": {
                                                            "startDate": "$crawledAt",
                                                            "amount": 7,
                                                            "unit": "day",
                                                        }
                                                    },
                                                ]
                                            },
                                            {"$toBool": "$$this.v.priceCurrent"},
                                            {
                                                "$lte": [
                                                    "$$this.v.priceCurrent",
                                                    "$$value.v",
                                                ]
                                            },
                                        ]
                                    },
                                    {
                                        "k": "$$this.v.priceDate",
                                        "v": "$$this.v.priceCurrent",
                                    },
                                    "$$value",
                                ]
                            },
                        }
                    },
                    "lowest30": {
                        "$reduce": {
                            "input": {"$reverseArray": "$timeseriesArr"},
                            "initialValue": {
                                "k": {
                                    "$dateSubtract": {
                                        "startDate": {
                                            "$dateTrunc": {
                                                "date": "$crawledAt",
                                                "unit": "day",
                                            }
                                        },
                                        "amount": 15,
                                        "unit": "minute",
                                    }
                                },
                                "v": {"$max": "$timeseriesArr.v.priceCurrent"},
                            },
                            "in": {
                                "$cond": [
                                    {
                                        "$and": [
                                            {
                                                "$lt": [
                                                    {
                                                        "$dateFromString": {
                                                            "dateString": "$$this.k",
                                                            "format": "%Y-%m-%d",
                                                        }
                                                    },
                                                    "$$value.k",
                                                ]
                                            },
                                            {
                                                "$gte": [
                                                    {
                                                        "$dateFromString": {
                                                            "dateString": "$$this.k",
                                                            "format": "%Y-%m-%d",
                                                        }
                                                    },
                                                    {
                                                        "$dateSubtract": {
                                                            "startDate": "$crawledAt",
                                                            "amount": 30,
                                                            "unit": "day",
                                                        }
                                                    },
                                                ]
                                            },
                                            {"$toBool": "$$this.v.priceCurrent"},
                                            {
                                                "$lte": [
                                                    "$$this.v.priceCurrent",
                                                    "$$value.v",
                                                ]
                                            },
                                        ]
                                    },
                                    {
                                        "k": "$$this.v.priceDate",
                                        "v": "$$this.v.priceCurrent",
                                    },
                                    "$$value",
                                ]
                            },
                        }
                    },
                    "lowest90": {
                        "$reduce": {
                            "input": {"$reverseArray": "$timeseriesArr"},
                            "initialValue": {
                                "k": {
                                    "$dateSubtract": {
                                        "startDate": {
                                            "$dateTrunc": {
                                                "date": "$crawledAt",
                                                "unit": "day",
                                            }
                                        },
                                        "amount": 15,
                                        "unit": "minute",
                                    }
                                },
                                "v": {"$max": "$timeseriesArr.v.priceCurrent"},
                            },
                            "in": {
                                "$cond": [
                                    {
                                        "$and": [
                                            {
                                                "$lt": [
                                                    {
                                                        "$dateFromString": {
                                                            "dateString": "$$this.k",
                                                            "format": "%Y-%m-%d",
                                                        }
                                                    },
                                                    "$$value.k",
                                                ]
                                            },
                                            {
                                                "$gte": [
                                                    {
                                                        "$dateFromString": {
                                                            "dateString": "$$this.k",
                                                            "format": "%Y-%m-%d",
                                                        }
                                                    },
                                                    {
                                                        "$dateSubtract": {
                                                            "startDate": "$crawledAt",
                                                            "amount": 90,
                                                            "unit": "day",
                                                        }
                                                    },
                                                ]
                                            },
                                            {"$toBool": "$$this.v.priceCurrent"},
                                            {
                                                "$lte": [
                                                    "$$this.v.priceCurrent",
                                                    "$$value.v",
                                                ]
                                            },
                                        ]
                                    },
                                    {
                                        "k": "$$this.v.priceDate",
                                        "v": "$$this.v.priceCurrent",
                                    },
                                    "$$value",
                                ]
                            },
                        }
                    },
                    "lowestAll": {
                        "$reduce": {
                            "input": {"$reverseArray": "$timeseriesArr"},
                            "initialValue": {
                                "k": {
                                    "$dateSubtract": {
                                        "startDate": {
                                            "$dateTrunc": {
                                                "date": "$crawledAt",
                                                "unit": "day",
                                            }
                                        },
                                        "amount": 15,
                                        "unit": "minute",
                                    }
                                },
                                "v": {"$max": "$timeseriesArr.v.priceCurrent"},
                            },
                            "in": {
                                "$cond": [
                                    {
                                        "$and": [
                                            {
                                                "$lt": [
                                                    {
                                                        "$dateFromString": {
                                                            "dateString": "$$this.k",
                                                            "format": "%Y-%m-%d",
                                                        }
                                                    },
                                                    "$$value.k",
                                                ]
                                            },
                                            {
                                                "$gte": [
                                                    {
                                                        "$dateFromString": {
                                                            "dateString": "$$this.k",
                                                            "format": "%Y-%m-%d",
                                                        }
                                                    },
                                                    {
                                                        "$dateSubtract": {
                                                            "startDate": "$crawledAt",
                                                            "amount": 3650,
                                                            "unit": "day",
                                                        }
                                                    },
                                                ]
                                            },
                                            {"$toBool": "$$this.v.priceCurrent"},
                                            {
                                                "$lte": [
                                                    "$$this.v.priceCurrent",
                                                    "$$value.v",
                                                ]
                                            },
                                        ]
                                    },
                                    {
                                        "k": "$$this.v.priceDate",
                                        "v": "$$this.v.priceCurrent",
                                    },
                                    "$$value",
                                ]
                            },
                        }
                    },
                    "highest7": {
                        "$reduce": {
                            "input": {"$reverseArray": "$timeseriesArr"},
                            "initialValue": {
                                "k": {
                                    "$dateSubtract": {
                                        "startDate": {
                                            "$dateTrunc": {
                                                "date": "$crawledAt",
                                                "unit": "day",
                                            }
                                        },
                                        "amount": 15,
                                        "unit": "minute",
                                    }
                                },
                                "v": {"$min": "$timeseriesArr.v.priceCurrent"},
                            },
                            "in": {
                                "$cond": [
                                    {
                                        "$and": [
                                            {
                                                "$lt": [
                                                    {
                                                        "$dateFromString": {
                                                            "dateString": "$$this.k",
                                                            "format": "%Y-%m-%d",
                                                        }
                                                    },
                                                    "$$value.k",
                                                ]
                                            },
                                            {
                                                "$gte": [
                                                    {
                                                        "$dateFromString": {
                                                            "dateString": "$$this.k",
                                                            "format": "%Y-%m-%d",
                                                        }
                                                    },
                                                    {
                                                        "$dateSubtract": {
                                                            "startDate": "$crawledAt",
                                                            "amount": 7,
                                                            "unit": "day",
                                                        }
                                                    },
                                                ]
                                            },
                                            {"$toBool": "$$this.v.priceCurrent"},
                                            {
                                                "$gte": [
                                                    "$$this.v.priceCurrent",
                                                    "$$value.v",
                                                ]
                                            },
                                        ]
                                    },
                                    {
                                        "k": "$$this.v.priceDate",
                                        "v": "$$this.v.priceCurrent",
                                    },
                                    "$$value",
                                ]
                            },
                        }
                    },
                    "highest30": {
                        "$reduce": {
                            "input": {"$reverseArray": "$timeseriesArr"},
                            "initialValue": {
                                "k": {
                                    "$dateSubtract": {
                                        "startDate": {
                                            "$dateTrunc": {
                                                "date": "$crawledAt",
                                                "unit": "day",
                                            }
                                        },
                                        "amount": 15,
                                        "unit": "minute",
                                    }
                                },
                                "v": {"$min": "$timeseriesArr.v.priceCurrent"},
                            },
                            "in": {
                                "$cond": [
                                    {
                                        "$and": [
                                            {
                                                "$lt": [
                                                    {
                                                        "$dateFromString": {
                                                            "dateString": "$$this.k",
                                                            "format": "%Y-%m-%d",
                                                        }
                                                    },
                                                    "$$value.k",
                                                ]
                                            },
                                            {
                                                "$gte": [
                                                    {
                                                        "$dateFromString": {
                                                            "dateString": "$$this.k",
                                                            "format": "%Y-%m-%d",
                                                        }
                                                    },
                                                    {
                                                        "$dateSubtract": {
                                                            "startDate": "$crawledAt",
                                                            "amount": 30,
                                                            "unit": "day",
                                                        }
                                                    },
                                                ]
                                            },
                                            {"$toBool": "$$this.v.priceCurrent"},
                                            {
                                                "$gte": [
                                                    "$$this.v.priceCurrent",
                                                    "$$value.v",
                                                ]
                                            },
                                        ]
                                    },
                                    {
                                        "k": "$$this.v.priceDate",
                                        "v": "$$this.v.priceCurrent",
                                    },
                                    "$$value",
                                ]
                            },
                        }
                    },
                    "highest90": {
                        "$reduce": {
                            "input": {"$reverseArray": "$timeseriesArr"},
                            "initialValue": {
                                "k": {
                                    "$dateSubtract": {
                                        "startDate": {
                                            "$dateTrunc": {
                                                "date": "$crawledAt",
                                                "unit": "day",
                                            }
                                        },
                                        "amount": 15,
                                        "unit": "minute",
                                    }
                                },
                                "v": {"$min": "$timeseriesArr.v.priceCurrent"},
                            },
                            "in": {
                                "$cond": [
                                    {
                                        "$and": [
                                            {
                                                "$lt": [
                                                    {
                                                        "$dateFromString": {
                                                            "dateString": "$$this.k",
                                                            "format": "%Y-%m-%d",
                                                        }
                                                    },
                                                    "$$value.k",
                                                ]
                                            },
                                            {
                                                "$gte": [
                                                    {
                                                        "$dateFromString": {
                                                            "dateString": "$$this.k",
                                                            "format": "%Y-%m-%d",
                                                        }
                                                    },
                                                    {
                                                        "$dateSubtract": {
                                                            "startDate": "$crawledAt",
                                                            "amount": 90,
                                                            "unit": "day",
                                                        }
                                                    },
                                                ]
                                            },
                                            {"$toBool": "$$this.v.priceCurrent"},
                                            {
                                                "$gte": [
                                                    "$$this.v.priceCurrent",
                                                    "$$value.v",
                                                ]
                                            },
                                        ]
                                    },
                                    {
                                        "k": "$$this.v.priceDate",
                                        "v": "$$this.v.priceCurrent",
                                    },
                                    "$$value",
                                ]
                            },
                        }
                    },
                    "highestAll": {
                        "$reduce": {
                            "input": {"$reverseArray": "$timeseriesArr"},
                            "initialValue": {
                                "k": {
                                    "$dateSubtract": {
                                        "startDate": {
                                            "$dateTrunc": {
                                                "date": "$crawledAt",
                                                "unit": "day",
                                            }
                                        },
                                        "amount": 15,
                                        "unit": "minute",
                                    }
                                },
                                "v": {"$min": "$timeseriesArr.v.priceCurrent"},
                            },
                            "in": {
                                "$cond": [
                                    {
                                        "$and": [
                                            {
                                                "$lt": [
                                                    {
                                                        "$dateFromString": {
                                                            "dateString": "$$this.k",
                                                            "format": "%Y-%m-%d",
                                                        }
                                                    },
                                                    "$$value.k",
                                                ]
                                            },
                                            {
                                                "$gte": [
                                                    {
                                                        "$dateFromString": {
                                                            "dateString": "$$this.k",
                                                            "format": "%Y-%m-%d",
                                                        }
                                                    },
                                                    {
                                                        "$dateSubtract": {
                                                            "startDate": "$crawledAt",
                                                            "amount": 3650,
                                                            "unit": "day",
                                                        }
                                                    },
                                                ]
                                            },
                                            {"$toBool": "$$this.v.priceCurrent"},
                                            {
                                                "$gte": [
                                                    "$$this.v.priceCurrent",
                                                    "$$value.v",
                                                ]
                                            },
                                        ]
                                    },
                                    {
                                        "k": "$$this.v.priceDate",
                                        "v": "$$this.v.priceCurrent",
                                    },
                                    "$$value",
                                ]
                            },
                        }
                    },
                    "average7Arr": {
                        "$filter": {
                            "input": {"$reverseArray": "$timeseriesArr"},
                            "as": "obj",
                            "cond": {
                                "$and": [
                                    {
                                        "$lt": [
                                            {
                                                "$dateFromString": {
                                                    "dateString": "$$obj.k",
                                                    "format": "%Y-%m-%d",
                                                }
                                            },
                                            {
                                                "$dateSubtract": {
                                                    "startDate": {
                                                        "$dateTrunc": {
                                                            "date": "$crawledAt",
                                                            "unit": "day",
                                                        }
                                                    },
                                                    "amount": 15,
                                                    "unit": "minute",
                                                }
                                            },
                                        ]
                                    },
                                    {
                                        "$gte": [
                                            {
                                                "$dateFromString": {
                                                    "dateString": "$$obj.k",
                                                    "format": "%Y-%m-%d",
                                                }
                                            },
                                            {
                                                "$dateSubtract": {
                                                    "startDate": "$crawledAt",
                                                    "amount": 7,
                                                    "unit": "day",
                                                }
                                            },
                                        ]
                                    },
                                    {"$toBool": "$$obj.v.priceCurrent"},
                                ]
                            },
                        }
                    },
                    "average30Arr": {
                        "$filter": {
                            "input": {"$reverseArray": "$timeseriesArr"},
                            "as": "obj",
                            "cond": {
                                "$and": [
                                    {
                                        "$lt": [
                                            {
                                                "$dateFromString": {
                                                    "dateString": "$$obj.k",
                                                    "format": "%Y-%m-%d",
                                                }
                                            },
                                            {
                                                "$dateSubtract": {
                                                    "startDate": {
                                                        "$dateTrunc": {
                                                            "date": "$crawledAt",
                                                            "unit": "day",
                                                        }
                                                    },
                                                    "amount": 15,
                                                    "unit": "minute",
                                                }
                                            },
                                        ]
                                    },
                                    {
                                        "$gte": [
                                            {
                                                "$dateFromString": {
                                                    "dateString": "$$obj.k",
                                                    "format": "%Y-%m-%d",
                                                }
                                            },
                                            {
                                                "$dateSubtract": {
                                                    "startDate": "$crawledAt",
                                                    "amount": 30,
                                                    "unit": "day",
                                                }
                                            },
                                        ]
                                    },
                                    {"$toBool": "$$obj.v.priceCurrent"},
                                ]
                            },
                        }
                    },
                    "average90Arr": {
                        "$filter": {
                            "input": {"$reverseArray": "$timeseriesArr"},
                            "as": "obj",
                            "cond": {
                                "$and": [
                                    {
                                        "$lt": [
                                            {
                                                "$dateFromString": {
                                                    "dateString": "$$obj.k",
                                                    "format": "%Y-%m-%d",
                                                }
                                            },
                                            {
                                                "$dateSubtract": {
                                                    "startDate": {
                                                        "$dateTrunc": {
                                                            "date": "$crawledAt",
                                                            "unit": "day",
                                                        }
                                                    },
                                                    "amount": 15,
                                                    "unit": "minute",
                                                }
                                            },
                                        ]
                                    },
                                    {
                                        "$gte": [
                                            {
                                                "$dateFromString": {
                                                    "dateString": "$$obj.k",
                                                    "format": "%Y-%m-%d",
                                                }
                                            },
                                            {
                                                "$dateSubtract": {
                                                    "startDate": "$crawledAt",
                                                    "amount": 90,
                                                    "unit": "day",
                                                }
                                            },
                                        ]
                                    },
                                    {"$toBool": "$$obj.v.priceCurrent"},
                                ]
                            },
                        }
                    },
                    "averageAllArr": {
                        "$filter": {
                            "input": {"$reverseArray": "$timeseriesArr"},
                            "as": "obj",
                            "cond": {
                                "$and": [
                                    {
                                        "$lt": [
                                            {
                                                "$dateFromString": {
                                                    "dateString": "$$obj.k",
                                                    "format": "%Y-%m-%d",
                                                }
                                            },
                                            {
                                                "$dateSubtract": {
                                                    "startDate": {
                                                        "$dateTrunc": {
                                                            "date": "$crawledAt",
                                                            "unit": "day",
                                                        }
                                                    },
                                                    "amount": 15,
                                                    "unit": "minute",
                                                }
                                            },
                                        ]
                                    },
                                    {
                                        "$gte": [
                                            {
                                                "$dateFromString": {
                                                    "dateString": "$$obj.k",
                                                    "format": "%Y-%m-%d",
                                                }
                                            },
                                            {
                                                "$dateSubtract": {
                                                    "startDate": "$crawledAt",
                                                    "amount": 3650,
                                                    "unit": "day",
                                                }
                                            },
                                        ]
                                    },
                                    {"$toBool": "$$obj.v.priceCurrent"},
                                ]
                            },
                        }
                    },
                }
            }
        },
        {
            "$set": {
                "stats.deal7": {
                    "v": {
                        "$subtract": [
                            {"$divide": ["$priceCurrent", "$stats.lowest7.v"]},
                            1,
                        ]
                    }
                },
                "stats.deal30": {
                    "v": {
                        "$subtract": [
                            {"$divide": ["$priceCurrent", "$stats.lowest30.v"]},
                            1,
                        ]
                    }
                },
                "stats.deal90": {
                    "v": {
                        "$subtract": [
                            {"$divide": ["$priceCurrent", "$stats.lowest90.v"]},
                            1,
                        ]
                    }
                },
                "stats.dealAll": {
                    "v": {
                        "$subtract": [
                            {"$divide": ["$priceCurrent", "$stats.lowestAll.v"]},
                            1,
                        ]
                    }
                },
                "stats.average7": {
                    "v": {"$avg": "$stats.average7Arr.v.priceCurrent"},
                },
                "stats.average30": {
                    "v": {"$avg": "$stats.average30Arr.v.priceCurrent"}
                },
                "stats.average90": {
                    "v": {"$avg": "$stats.average90Arr.v.priceCurrent"}
                },
                "stats.averageAll": {
                    "v": {"$avg": "$stats.averageAllArr.v.priceCurrent"}
                },
                "stats.cash7": {
                    "v": {"$subtract": ["$priceCurrent", "$stats.lowest7.v"]}
                },
                "stats.cash30": {
                    "v": {"$subtract": ["$priceCurrent", "$stats.lowest30.v"]}
                },
                "stats.cash90": {
                    "v": {"$subtract": ["$priceCurrent", "$stats.lowest90.v"]}
                },
                "stats.cashAll": {
                    "v": {"$subtract": ["$priceCurrent", "$stats.lowestAll.v"]}
                },
                # *This is UTC
                "stats.updatedAt": "$$NOW",
                "timeseriesArr": "$$REMOVE",
                "stats.average7Arr": "$$REMOVE",
                "stats.average30Arr": "$$REMOVE",
                "stats.average90Arr": "$$REMOVE",
                "stats.averageAllArr": "$$REMOVE",
            }
        },
        {
            "$merge": {
                "into": f"emag{DEV_TAG}",
                "on": "_id",
                "whenMatched": "replace",
                "whenNotMatched": "insert",
            }
        },
    ]

    # Run aggregation
    client[db][coll].aggregate(pipeline)

    # Debug only
    end = time.time()
    print(Decimal(end - start).quantize(Decimal(".01"), rounding=ROUND_DOWN))


if __name__ == "__main__":
    main()
