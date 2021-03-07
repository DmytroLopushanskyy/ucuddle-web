import json

import jsonpickle
from elasticsearch import Elasticsearch

es = Elasticsearch()


class MyEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


def elastic_search(search_line):
    query = {
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": search_line,
                        "fuzziness": "AUTO",
                        "minimum_should_match": "30%",
                        "operator": "or",
                        "fields": {
                            "title^5",
                            "text",
                        },
                    },
                },
            },
        },
        "suggest": {
            "my-suggestion": {
                "text": search_line,
                "term": {
                    "field": "title",
                },
            },
        },
    }
    res = es.search(
        index="t_english_sites3",
        body=jsonpickle.encode(query, unpicklable=False)
    )
    print("Got %d Hits:" % res['hits']['total']['value'])
    hits_list = []
    for hit in res['hits']['hits']:
        hits_list.append(hit["_source"])

    return hits_list
