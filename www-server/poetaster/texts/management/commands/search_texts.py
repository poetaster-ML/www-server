from elasticsearch_dsl.connections import get_connection
from texts.models import Text, Author
from texts.documents import TextDocument, AuthorDocument
from common.management.commands import BaseCommand
from pprint import pprint


"""
curl -X GET "search:9200/texts/_search?pretty" -H 'Content-Type: application/json' -d'
{
    "query" : {
        "multi_match": {
          "query": "love",
          "fields": ["raw", "title"]
        }
    },
    "highlight" : {
        "fields" : {
            "raw" : {}
        }
    }
}'
"""


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--query",
            dest="query",
            type=str
        )

    def handle(self, *args, query=None, **options):
        search = TextDocument.search()
        search = search.query(
          # "match", raw=query
          "multi_match", query=query, fields=["raw", "title"]
        )
        search = search.highlight("raw", fragment_size=0)
        search = search.highlight("title", fragment_size=0)

        print("SEARCH PARAMS:\n")

        pprint(search._index)
        pprint(search.to_dict())
        pprint(search._params)

        es = get_connection(search._using)

        raw_response = es.search(
            index=search._index,
            body=search.to_dict(),
            **search._params
        )

        print("RAW RESPONSE:\n")
        pprint(raw_response)

        print("RESPONSE CLASS:")
        print(search._response_class)
        print("-------------------------------")

        response = search._response_class(
            search, raw_response
        )

        print("\nWRAPPED RESPONSE:\n")
        for hit in response:
            pprint(hit.meta.highlight._d_)
