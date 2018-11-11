"""Tests search engine."""

import logging

from mem.search.text import TextSearcher

logger = logging.getLogger(__name__)


def main(_):
    searcher = TextSearcher()

    # searcher.build_index([(0, 'mam'), (1, 'dad')])

    # searcher.clear()

    query = 'mam'
    result = searcher.search(query)

    logger.info(result)


def _parse_config():
    logging.basicConfig(
        format='%(asctime)s | %(message)s',
        handlers=[
            logging.StreamHandler()
        ],
        level=logging.INFO
    )


if __name__ == '__main__':
    main(_parse_config())
