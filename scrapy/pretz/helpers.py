# Schema validation
validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["pID", "pName"],
        "properties": {
            "pID": {
                "bsonType": "string",
                "description": "Product ID - Required.",
                "uniqueItems": True,
            },
            "pName": {
                "bsonType": "string",
                "description": "Product name - Required.",
            },
            # "pNameTags": {
            #     "bsonType": "array",
            #     "description": "Product name tags - Optional.",
            # },
            "pLink": {
                "bsonType": "string",
                "description": "Product link - Optional.",
            },
            "pImg": {
                "bsonType": "string",
                "description": "Product image - Optional.",
            },
            "pCategoryTrail": {
                "bsonType": "array",
                "description": "Product category trail - Optional.",
            },
            "pCategory": {
                "bsonType": "string",
                "description": "Product category - Optional.",
            },
            "pVendor": {
                "bsonType": "string",
                "description": "Product vendor - Optional.",
            },
            "pStock": {
                "bsonType": "string",
                "description": "Product stock - Optional.",
            },
            "pReviews": {
                "bsonType": "number",
                "description": "Product reviews - Optional.",
            },
            "pStars": {
                "bsonType": "number",
                "description": "Product stars - Optional.",
            },
            "pGeniusTag": {
                "bsonType": "bool",
                "description": "Product genius tag - Optional.",
            },
            "pUsedTag": {
                "bsonType": "bool",
                "description": "Product used tag - Optional.",
            },
            "priceCurrent": {
                "bsonType": "number",
                "description": "Price current - Optional.",
            },
            "priceRetail": {
                "bsonType": "number",
                "description": "Price retail - Optional.",
            },
            "priceSlashed": {
                "bsonType": "number",
                "description": "Price slashed - Optional.",
            },
            "priceUsed": {
                "bsonType": "number",
                "description": "Price used - Optional.",
            },
            "crawledAt": {
                "bsonType": "date",
                "description": "Crawled at - Optional.",
            },
            "timeseries": {
                "bsonType": "object",
                "description": "Product timeseries - Optional.",
                "properties": {
                    "priceDate": {
                        "bsonType": "date",
                        "description": "Price Date - Optional.",
                    },
                    "priceCurrent": {
                        "bsonType": "number",
                        "description": "Price Current - Optional.",
                    },
                    "priceRetail": {
                        "bsonType": "number",
                        "description": "Price Retail - Optional.",
                    },
                    "priceSlashed": {
                        "bsonType": "number",
                        "description": "Price Slashed - Optional.",
                    },
                    "priceUsed": {
                        "bsonType": "number",
                        "description": "Price Used - Optional.",
                    },
                },
            },
            "stats": {
                "bsonType": "object",
                "description": "Price stats - Optional.",
                "properties": {
                    "lowest7": {
                        "bsonType": "object",
                        "description": "Minimum new price of 7 days - Optional.",
                        "properties": {
                            "k": {
                                "bsonType": "date",
                                "description": "Key - Optional",
                            },
                            "v": {
                                "bsonType": "number",
                                "description": "Value - Optional",
                            },
                        },
                    },
                    "lowest30": {
                        "bsonType": "object",
                        "description": "Minimum new price of 30 days - Optional.",
                        "properties": {
                            "k": {
                                "bsonType": "date",
                                "description": "Key - Optional",
                            },
                            "v": {
                                "bsonType": "number",
                                "description": "Value - Optional",
                            },
                        },
                    },
                    "lowest90": {
                        "bsonType": "object",
                        "description": "Minimum new price of 90 days - Optional.",
                        "properties": {
                            "k": {
                                "bsonType": "date",
                                "description": "Key - Optional",
                            },
                            "v": {
                                "bsonType": "number",
                                "description": "Value - Optional",
                            },
                        },
                    },
                    "lowestAll": {
                        "bsonType": "object",
                        "description": "Minimum new price of all time - Optional.",
                        "properties": {
                            "k": {
                                "bsonType": "date",
                                "description": "Key - Optional",
                            },
                            "v": {
                                "bsonType": "number",
                                "description": "Value - Optional",
                            },
                        },
                    },
                    "highest7": {
                        "bsonType": "object",
                        "description": "Highest new price of 7 days - Optional.",
                        "properties": {
                            "k": {
                                "bsonType": "date",
                                "description": "Key - Optional",
                            },
                            "v": {
                                "bsonType": "number",
                                "description": "Value - Optional",
                            },
                        },
                    },
                    "highest30": {
                        "bsonType": "object",
                        "description": "Highest new price of 30 days - Optional.",
                        "properties": {
                            "k": {
                                "bsonType": "date",
                                "description": "Key - Optional",
                            },
                            "v": {
                                "bsonType": "number",
                                "description": "Value - Optional",
                            },
                        },
                    },
                    "highest90": {
                        "bsonType": "object",
                        "description": "Highest new price of 90 days - Optional.",
                        "properties": {
                            "k": {
                                "bsonType": "date",
                                "description": "Key - Optional",
                            },
                            "v": {
                                "bsonType": "number",
                                "description": "Value - Optional",
                            },
                        },
                    },
                    "highestAll": {
                        "bsonType": "object",
                        "description": "Highest new price of all time - Optional.",
                        "properties": {
                            "k": {
                                "bsonType": "date",
                                "description": "Key - Optional",
                            },
                            "v": {
                                "bsonType": "number",
                                "description": "Value - Optional",
                            },
                        },
                    },
                    "deal7": {
                        "bsonType": "object",
                        "description": "Deal new price of 7 days - Optional.",
                        "properties": {
                            "v": {
                                "bsonType": "number",
                                "description": "Value - Optional",
                            }
                        },
                    },
                    "deal30": {
                        "bsonType": "object",
                        "description": "Deal new price of 30 days - Optional.",
                        "properties": {
                            "v": {
                                "bsonType": "number",
                                "description": "Value - Optional",
                            }
                        },
                    },
                    "deal90": {
                        "bsonType": "object",
                        "description": "Deal new price of 90 days - Optional.",
                        "properties": {
                            "v": {
                                "bsonType": "number",
                                "description": "Value - Optional",
                            }
                        },
                    },
                    "dealAll": {
                        "bsonType": "object",
                        "description": "Deal new price of all time - Optional.",
                        "properties": {
                            "v": {
                                "bsonType": "number",
                                "description": "Value - Optional",
                            }
                        },
                    },
                    "average7": {
                        "bsonType": "object",
                        "description": "Average price of 7 days - Optional.",
                        "properties": {
                            "v": {
                                "bsonType": ["number", "null"],
                                "description": "Value - Optional",
                            }
                        },
                    },
                    "average30": {
                        "bsonType": "object",
                        "description": "Average price of 30 days - Optional.",
                        "properties": {
                            "v": {
                                "bsonType": ["number", "null"],
                                "description": "Value - Optional",
                            }
                        },
                    },
                    "average90": {
                        "bsonType": "object",
                        "description": "Average price of 90 days - Optional.",
                        "properties": {
                            "v": {
                                "bsonType": ["number", "null"],
                                "description": "Value - Optional",
                            }
                        },
                    },
                    "averageAll": {
                        "bsonType": "object",
                        "description": "Average price of all time - Optional.",
                        "properties": {
                            "v": {
                                "bsonType": ["number", "null"],
                                "description": "Value - Optional",
                            }
                        },
                    },
                    "cash7": {
                        "bsonType": "object",
                        "description": "Cash price of 7 days - Optional.",
                        "properties": {
                            "v": {
                                "bsonType": ["number", "null"],
                                "description": "Value - Optional",
                            }
                        },
                    },
                    "cash30": {
                        "bsonType": "object",
                        "description": "Cash price of 30 days - Optional.",
                        "properties": {
                            "v": {
                                "bsonType": ["number", "null"],
                                "description": "Value - Optional",
                            }
                        },
                    },
                    "cash90": {
                        "bsonType": "object",
                        "description": "Cash price of 90 days - Optional.",
                        "properties": {
                            "v": {
                                "bsonType": ["number", "null"],
                                "description": "Value - Optional",
                            }
                        },
                    },
                    "cashAll": {
                        "bsonType": "object",
                        "description": "Cash price of all time - Optional.",
                        "properties": {
                            "v": {
                                "bsonType": ["number", "null"],
                                "description": "Value - Optional",
                            }
                        },
                    },
                    "updatedAt": {
                        "bsonType": "date",
                        "description": "Updated at value for stats",
                    },
                },
            },
        },
    }
}

# Pipeline
timeseries_array = {
    "$set": {
        "timeseriesArr": {"$objectToArray": "$timeseries"},
    },
}
generate_stats = {
    "$set": {
        "stats": {
            "lowest7": {
                "$reduce": {
                    "input": {"$reverseArray": "$timeseriesArr"},
                    "initialValue": {
                        "k": "$crawledAt",
                        "v": {"$max": "$timeseriesArr.v.priceCurrent"},
                    },
                    "in": {
                        "$cond": [
                            {
                                "$and": [
                                    {
                                        "$lt": [
                                            "$$this.v.priceDate",
                                            "$$value.k",
                                        ]
                                    },
                                    {
                                        "$gte": [
                                            "$$this.v.priceDate",
                                            {
                                                "$dateTrunc": {
                                                    "date": {
                                                        "$dateSubtract": {
                                                            "startDate": "$crawledAt",
                                                            "amount": 7,
                                                            "unit": "day",
                                                        }
                                                    },
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
                                    {
                                        "$ne": [
                                            "$$this.v.priceCurrent",
                                            "$priceCurrent",
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
                        "k": "$crawledAt",
                        "v": {"$max": "$timeseriesArr.v.priceCurrent"},
                    },
                    "in": {
                        "$cond": [
                            {
                                "$and": [
                                    {
                                        "$lt": [
                                            "$$this.v.priceDate",
                                            "$$value.k",
                                        ]
                                    },
                                    {
                                        "$gte": [
                                            "$$this.v.priceDate",
                                            {
                                                "$dateTrunc": {
                                                    "date": {
                                                        "$dateSubtract": {
                                                            "startDate": "$crawledAt",
                                                            "amount": 30,
                                                            "unit": "day",
                                                        }
                                                    },
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
                                    {
                                        "$ne": [
                                            "$$this.v.priceCurrent",
                                            "$priceCurrent",
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
                        "k": "$crawledAt",
                        "v": {"$max": "$timeseriesArr.v.priceCurrent"},
                    },
                    "in": {
                        "$cond": [
                            {
                                "$and": [
                                    {
                                        "$lt": [
                                            "$$this.v.priceDate",
                                            "$$value.k",
                                        ]
                                    },
                                    {
                                        "$gte": [
                                            "$$this.v.priceDate",
                                            {
                                                "$dateTrunc": {
                                                    "date": {
                                                        "$dateSubtract": {
                                                            "startDate": "$crawledAt",
                                                            "amount": 90,
                                                            "unit": "day",
                                                        }
                                                    },
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
                                    {
                                        "$ne": [
                                            "$$this.v.priceCurrent",
                                            "$priceCurrent",
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
                        "k": "$crawledAt",
                        "v": {"$max": "$timeseriesArr.v.priceCurrent"},
                    },
                    "in": {
                        "$cond": [
                            {
                                "$and": [
                                    {
                                        "$lt": [
                                            "$$this.v.priceDate",
                                            "$$value.k",
                                        ]
                                    },
                                    {
                                        "$gte": [
                                            "$$this.v.priceDate",
                                            {
                                                "$dateTrunc": {
                                                    "date": {
                                                        "$dateSubtract": {
                                                            "startDate": "$crawledAt",
                                                            "amount": 3650,
                                                            "unit": "day",
                                                        }
                                                    },
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
                                    {
                                        "$ne": [
                                            "$$this.v.priceCurrent",
                                            "$priceCurrent",
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
                        "k": "$crawledAt",
                        "v": {"$min": "$timeseriesArr.v.priceCurrent"},
                    },
                    "in": {
                        "$cond": [
                            {
                                "$and": [
                                    {
                                        "$lt": [
                                            "$$this.v.priceDate",
                                            "$$value.k",
                                        ]
                                    },
                                    {
                                        "$gte": [
                                            "$$this.v.priceDate",
                                            {
                                                "$dateTrunc": {
                                                    "date": {
                                                        "$dateSubtract": {
                                                            "startDate": "$crawledAt",
                                                            "amount": 7,
                                                            "unit": "day",
                                                        }
                                                    },
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
                        "k": "$crawledAt",
                        "v": {"$min": "$timeseriesArr.v.priceCurrent"},
                    },
                    "in": {
                        "$cond": [
                            {
                                "$and": [
                                    {
                                        "$lt": [
                                            "$$this.v.priceDate",
                                            "$$value.k",
                                        ]
                                    },
                                    {
                                        "$gte": [
                                            "$$this.v.priceDate",
                                            {
                                                "$dateTrunc": {
                                                    "date": {
                                                        "$dateSubtract": {
                                                            "startDate": "$crawledAt",
                                                            "amount": 30,
                                                            "unit": "day",
                                                        }
                                                    },
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
                        "k": "$crawledAt",
                        "v": {"$min": "$timeseriesArr.v.priceCurrent"},
                    },
                    "in": {
                        "$cond": [
                            {
                                "$and": [
                                    {
                                        "$lt": [
                                            "$$this.v.priceDate",
                                            "$$value.k",
                                        ]
                                    },
                                    {
                                        "$gte": [
                                            "$$this.v.priceDate",
                                            {
                                                "$dateTrunc": {
                                                    "date": {
                                                        "$dateSubtract": {
                                                            "startDate": "$crawledAt",
                                                            "amount": 90,
                                                            "unit": "day",
                                                        }
                                                    },
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
                        "k": "$crawledAt",
                        "v": {"$min": "$timeseriesArr.v.priceCurrent"},
                    },
                    "in": {
                        "$cond": [
                            {
                                "$and": [
                                    {
                                        "$lt": [
                                            "$$this.v.priceDate",
                                            "$$value.k",
                                        ]
                                    },
                                    {
                                        "$gte": [
                                            "$$this.v.priceDate",
                                            {
                                                "$dateTrunc": {
                                                    "date": {
                                                        "$dateSubtract": {
                                                            "startDate": "$crawledAt",
                                                            "amount": 3650,
                                                            "unit": "day",
                                                        }
                                                    },
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
                                    "$$obj.v.priceDate",
                                    "$crawledAt",
                                ]
                            },
                            {
                                "$gte": [
                                    "$$obj.v.priceDate",
                                    {
                                        "$dateTrunc": {
                                            "date": {
                                                "$dateSubtract": {
                                                    "startDate": "$crawledAt",
                                                    "amount": 7,
                                                    "unit": "day",
                                                }
                                            },
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
                                    "$$obj.v.priceDate",
                                    "$crawledAt",
                                ]
                            },
                            {
                                "$gte": [
                                    "$$obj.v.priceDate",
                                    {
                                        "$dateTrunc": {
                                            "date": {
                                                "$dateSubtract": {
                                                    "startDate": "$crawledAt",
                                                    "amount": 30,
                                                    "unit": "day",
                                                }
                                            },
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
                                    "$$obj.v.priceDate",
                                    "$crawledAt",
                                ]
                            },
                            {
                                "$gte": [
                                    "$$obj.v.priceDate",
                                    {
                                        "$dateTrunc": {
                                            "date": {
                                                "$dateSubtract": {
                                                    "startDate": "$crawledAt",
                                                    "amount": 90,
                                                    "unit": "day",
                                                }
                                            },
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
                                    "$$obj.v.priceDate",
                                    "$crawledAt",
                                ]
                            },
                            {
                                "$gte": [
                                    "$$obj.v.priceDate",
                                    {
                                        "$dateTrunc": {
                                            "date": {
                                                "$dateSubtract": {
                                                    "startDate": "$crawledAt",
                                                    "amount": 3650,
                                                    "unit": "day",
                                                }
                                            },
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
}
cleanup = {
    "$set": {
        "stats.deal7": {
            "v": {
                "$cond": [
                    {"$toBool": "$priceCurrent"},
                    {
                        "$subtract": [
                            {
                                "$divide": [
                                    "$priceCurrent",
                                    "$stats.lowest7.v",
                                ]
                            },
                            1,
                        ]
                    },
                    0,
                ]
            }
        },
        "stats.deal30": {
            "v": {
                "$cond": [
                    {"$toBool": "$priceCurrent"},
                    {
                        "$subtract": [
                            {
                                "$divide": [
                                    "$priceCurrent",
                                    "$stats.lowest30.v",
                                ]
                            },
                            1,
                        ]
                    },
                    0,
                ]
            }
        },
        "stats.deal90": {
            "v": {
                "$cond": [
                    {"$toBool": "$priceCurrent"},
                    {
                        "$subtract": [
                            {
                                "$divide": [
                                    "$priceCurrent",
                                    "$stats.lowest90.v",
                                ]
                            },
                            1,
                        ]
                    },
                    0,
                ]
            }
        },
        "stats.dealAll": {
            "v": {
                "$cond": [
                    {"$toBool": "$priceCurrent"},
                    {
                        "$subtract": [
                            {
                                "$divide": [
                                    "$priceCurrent",
                                    "$stats.lowestAll.v",
                                ]
                            },
                            1,
                        ]
                    },
                    0,
                ]
            }
        },
        "stats.average7": {"v": {"$avg": "$stats.average7Arr.v.priceCurrent"}},
        "stats.average30": {"v": {"$avg": "$stats.average30Arr.v.priceCurrent"}},
        "stats.average90": {"v": {"$avg": "$stats.average90Arr.v.priceCurrent"}},
        "stats.averageAll": {"v": {"$avg": "$stats.averageAllArr.v.priceCurrent"}},
        "stats.cash7": {
            "v": {
                "$cond": [
                    {"$toBool": "$priceCurrent"},
                    {"$subtract": ["$priceCurrent", "$stats.lowest7.v"]},
                    0,
                ]
            }
        },
        "stats.cash30": {
            "v": {
                "$cond": [
                    {"$toBool": "$priceCurrent"},
                    {"$subtract": ["$priceCurrent", "$stats.lowest30.v"]},
                    0,
                ]
            }
        },
        "stats.cash90": {
            "v": {
                "$cond": [
                    {"$toBool": "$priceCurrent"},
                    {"$subtract": ["$priceCurrent", "$stats.lowest90.v"]},
                    0,
                ]
            }
        },
        "stats.cashAll": {
            "v": {
                "$cond": [
                    {"$toBool": "$priceCurrent"},
                    {"$subtract": ["$priceCurrent", "$stats.lowestAll.v"]},
                    0,
                ]
            }
        },
        # *This is UTC
        "stats.updatedAt": "$$NOW",
        "timeseriesArr": "$$REMOVE",
        "stats.average7Arr": "$$REMOVE",
        "stats.average30Arr": "$$REMOVE",
        "stats.average90Arr": "$$REMOVE",
        "stats.averageAllArr": "$$REMOVE",
    }
}
