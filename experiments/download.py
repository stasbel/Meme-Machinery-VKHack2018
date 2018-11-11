"""Downloads prescribed data from the Internet, embed and store it."""

import logging

import numpy as np
import torch

from experiments.scrap import META_PATH
from mem.gen.stages.extractor import Extractor

logger = logging.getLogger(__name__)

MATRIX_PATH = 'matrix.npy'
NEW_META_PATH = 'processed_reddit_data.pth'


def main(_):
    meta = torch.load(META_PATH)

    extractor = Extractor()
    meta, matrix = extractor.extract(meta)

    torch.save(meta, NEW_META_PATH)
    logger.info(f'Obtain matrix of shape {matrix.shape}.')
    np.save(MATRIX_PATH, matrix)


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
