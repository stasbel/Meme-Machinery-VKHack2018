import os

from whoosh import writing
from whoosh.fields import Schema, ID, TEXT
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser


class TextSearcher:
    SCHEMA = Schema(id=ID(stored=True), text=TEXT(stored=True))

    def __init__(self, index_path='index'):
        if not os.path.exists(index_path):
            os.mkdir(index_path)
            self.ix = create_in(index_path, self.SCHEMA)
        else:
            self.ix = open_dir(index_path)

    def build_index(self, data):
        writer = self.ix.writer()
        for id_, text in data:
            writer.add_document(id=str(id_), text=text)

        writer.commit()

    def clear(self):
        with self.ix.writer() as writer:
            writer.mergetype = writing.CLEAR

    def search(self, query):
        with self.ix.searcher() as searcher:
            parser = QueryParser('text', self.ix.schema)
            query_parser = parser.parse(query)
            return [int(r['id']) for r in searcher.search(query_parser)]
