from datetime import datetime
from elasticsearch import Elasticsearch
import certifi

class Query:
    query = {'query': {}}

    def match_all(self, content={}):
        self.query['query']['match_all'] = content

class ElasticQueryBuilder:
    index = ''

    def __init__(self,  host, use_ssl=True):
        ca_certs = None if use_ssl else certifi.where()
        self.es = Elasticsearch(host, use_ssl=use_ssl, ca_certs=ca_certs)

    def use_index(self, index):
        self.index = index

    def create_index(self, index=None, **kwargs):
        if (self.index != ''):
            index = self.index

        return self.es.index(index=index, **kwargs)

    def get(self, index=None, **kwargs):
        if (self.index != ''):
            index = self.index

        return self.es.get(index, **kwargs)

    def refresh_indices(self, index=None, **kwargs):
        if (self.index != ''):
            index = self.index

        self.es.indices.refresh(index=index)

    def search(self, **kwargs):
        if (self.index != ''):
            index = self.index

        return self.es.search(index=index, **kwargs)

    def query(self):
        return Query()

if __name__ == '__main__':
    qb = ElasticQueryBuilder(host=["http://localhost:9200/"], use_ssl=False)
    qb.use_index("test-index")

    test_index = "test-index"
    doc = {
        'author': 'kimchy',
        'text': 'Elasticsearch: cool. bonsai cool.',
        'timestamp': datetime.now(),
    }

    res = qb.create_index(id=1, body=doc)
    print(res['result'])

    res = qb.get(id=1)
    print(res['_source'])

    qb.refresh_indices()

    res = qb.search(body=qb.query().match_all())
    print("Got %d Hits:" % res['hits']['total'])

    for hit in res['hits']['hits']:
        print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])
