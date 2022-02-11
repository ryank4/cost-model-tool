import urllib

import pymongo

# mongo_uri = "mongodb+srv://ryank:" + urllib.parse.quote("URRvF@C!56!!Cz4") + "@cluster0.odvfa.mongodb.net/test?retryWrites" \
#                                                                        "=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"

mongo_uri = "mongodb://127.0.0.1:27017"

client = pymongo.MongoClient(mongo_uri)

db = client.testdb

