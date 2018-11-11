"""Makes one sample for text meme generator."""

import argparse
import logging
from pathlib import Path

import numpy as np
import torch
from PIL import Image

from experiments.download import MATRIX_PATH, NEW_META_PATH
from mem.gen.sampler import TextSampler
from mem.gen.stages.printer import Printer

logger = logging.getLogger(__name__)


def main(config):
    matrix, meta = np.load(MATRIX_PATH), torch.load(NEW_META_PATH)
    sampler = TextSampler(matrix, meta)

    image = Image.open(config.image)
    text = sampler.sample(image)
    logger.info(f'Sampled text: {text}')

    if config.output_file:
        printer = Printer()
        new_image = printer.print(image, text)
        new_image.save(config.output_file)


def _parse_config():
    parser = argparse.ArgumentParser(
        description='Text sampler for given image',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument('image',
                        type=Path,
                        help='Image to sample text to')

    parser.add_argument('-o', '--output_file',
                        type=Path,
                        help='File to save image to')

    config = parser.parse_args()

    logging.basicConfig(
        format='%(asctime)s | %(message)s',
        handlers=[
            logging.StreamHandler()
        ],
        level=logging.INFO
    )

    return config


if __name__ == '__main__':
    main(_parse_config())
