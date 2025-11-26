from elasticsearch import Elasticsearch

from config import settings

es_client = Elasticsearch(settings.elasticsearch.url,
                          http_auth=(settings.elasticsearch.username, settings.elasticsearch.password))
