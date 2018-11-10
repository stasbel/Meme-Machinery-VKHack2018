import configparser
import logging

import torch

from memgen.scrapper.reddit import RedditScrapper

logger = logging.getLogger(__name__)

SUBREDDITS = [
    'AdviceAnimals', 'MemeEconomy', 'ComedyCemetery', 'memes', 'dankmemes',
    'PrequelMemes', 'terriblefacebookmemes', 'PewdiepieSubmissions', 'funny',
    'teenagers', '2meirl4meirl', 'wholesomememes', 'starterpacks', 'meirl'
]
META_PATH = 'reddit_data.pth'
_CONFIG_FILE = 'config.ini'


def main(config):
    reddit = config['REDDIT']
    client_id = reddit['CLIENT_ID']
    client_secret = reddit['CLIENT_SECRET']

    scrapper = RedditScrapper(client_id, client_secret)
    meta = scrapper.scrap(SUBREDDITS)

    logger.info(f'Collected {len(meta)} samples from Reddit.')
    torch.save(meta, META_PATH)


def _parse_config():
    config = configparser.ConfigParser()
    config.read(_CONFIG_FILE)

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
