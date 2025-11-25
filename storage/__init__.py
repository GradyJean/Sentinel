from config import settings
from elasticsearch import Elasticsearch

es_client = Elasticsearch(settings.elasticsearch.url,
                          http_auth=(settings.elasticsearch.username, settings.elasticsearch.password))
