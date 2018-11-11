import logging
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import pytesseract
import tqdm
from PIL import Image
from requests import get

from memgen.scrapper.reddit import RedditScrapper
from memgen.stages.embedder import Embedder

logger = logging.getLogger(__name__)


class Extractor:
    def __init__(self, base_folder=Path('images'), do_caption=True):
        base_folder.mkdir(parents=True, exist_ok=True)
        self.base_folder = base_folder
        self.embedder = Embedder()
        self.do_caption = do_caption

    def extract(self, data, n_processes=20):
        # data = data[:50]

        new_data, m = [], []
        with Pool(n_processes) as p:
            with tqdm.tqdm(total=len(data), desc='Downloading') as pbar:
                args = ((post, i) for post, i in zip(data, range(len(data))))
                iterator = p.imap_unordered(self._extract_one, args)
                for new_post, e in iterator:
                    if new_data is not None:
                        new_data.append(new_post)
                        m.append(e)
                    pbar.update()

        return new_data, np.stack(m)

    @staticmethod
    def download(url):
        try:
            response = get(url, stream=True)
            response.raw.decode_content = True
            return Image.open(response.raw)
        except OSError:
            return None

    def _extract_one(self, args):
        post, i = args
        image = self.download(post.url)
        # image = Image.open(self.base_folder / f'{i}.png')
        if image is None:
            return None, None

        caption = self._extract_caption(image, post) \
            if self.do_caption else None

        file_name = f'{i}.png'
        image.save(self.base_folder / file_name)

        e = self.embedder.embed(image)

        # noinspection PyProtectedMember
        new_post = post._replace(file_name=file_name, caption=caption)

        return new_post, e

    def _extract_caption(self, image, post):
        caption = pytesseract.image_to_string(self._darken_background(image))
        caption = caption.replace('\n', ' ').strip().lower()
        flag, caption = RedditScrapper.purge_comment(caption, post.upvotes)
        return caption if flag else None

    @staticmethod
    def _darken_background(image, limit=255):
        image = image.convert('L')
        image = image.point(lambda x: 0 if x < limit else 255, '1')
        return image
