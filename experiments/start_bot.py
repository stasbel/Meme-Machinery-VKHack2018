"""Starts BK bot and listen to messages."""

import configparser
import logging

from experiments.scrap import CONFIG_FILE
from mem.bot.vk import VKBot


def main(config):
    vk = config['VK']
    token, group_id, album_id = vk['TOKEN'], vk['GROUP_ID'], vk['ALBUM_ID']
    login, password = vk['LOGIN'], vk['PASSWORD']

    bot = VKBot(login, password, token, group_id, album_id)
    bot.listen()


def _parse_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

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
