import logging
import random

import vk_api
from vk_api import VkUpload
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from mem.gen.stages.extractor import Extractor

logger = logging.getLogger(__name__)


class VKBot:
    FAILED_REPLY = 'Пожалуйста, пришлите нам фотографию или текст.'
    GEN_REPLY = 'Посмотри, какой мем мы сгенерировали!'

    def __init__(self, login, password, token, group_id, album_id,
                 text2desc=lambda t: (t, None),
                 image2desc=lambda i: (None, i),
                 generator1=None, generator2=None,
                 p_generate=0.5, p_choose=0.5,
                 tmp_image='image.png'):
        self.vk_session = vk_api.VkApi(login, password,
                                       token=token, api_version='5.87')

        try:
            self.vk_session.auth(token_only=True)
        except vk_api.AuthError as error_msg:
            logger.debug(error_msg)
            return

        self.group_id = group_id
        self.album_id = album_id
        self.tmp_image = tmp_image

        self.text2desc = text2desc
        self.image2desc = image2desc
        self.generator1 = generator1
        self.generator2 = generator2
        self.p_generate = p_generate
        self.p_choose = p_choose

        self.longpoll = None
        self.vk = None
        self.upload = None

    def listen(self):
        self.longpoll = VkBotLongPoll(self.vk_session, self.group_id)
        self.vk = self.vk_session.get_api()
        self.upload = VkUpload(self.vk_session)

        for event in self.longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                url = self._fetch_url(event)
                text = event.obj.text

                if url is None and text is not None:
                    logger.info(f'Received text: {event.obj.text}')

                    reply_text, reply_image = self.text2desc(text)

                    self._send_text(event, reply_text)
                    self._sent_image(event, reply_image)
                elif url is not None:
                    logger.info(f'Receive image.')

                    image = Extractor.download(url)
                    reply_text, reply_image = self.image2desc(image)

                    self._send_text(event, reply_text)
                    self._sent_image(event, reply_image)

                    if random.random() < self.p_generate:
                        self._send_text(event, self.GEN_REPLY)
                        if random.random() < self.p_choose:
                            self._sent_image(event, self.generator1(image))
                        else:
                            self._sent_image(event, self.generator2(image))
                else:
                    self._send_text(event, self.FAILED_REPLY)

    @staticmethod
    def _fetch_url(event):
        attachments = event.obj.attachments
        if not len(attachments):
            return None

        photos = [a['photo'] for a in attachments if a['type'] == 'photo']
        if not len(photos):
            return None

        photo = photos[0]
        url = next(s['url'] for s in photo['sizes'] if s['type'] == 'z')
        return url

    def _send_text(self, event, text):
        if text is None:
            return

        self.vk.messages.send(user_id=event.obj.from_id,
                              message=text,
                              group_id=self.group_id)

    def _sent_image(self, event, image):
        if image is None:
            return

        image.save(self.tmp_image)
        photo = self.upload.photo(self.tmp_image,
                                  album_id=self.album_id,
                                  group_id=self.group_id)[0]

        attachment = 'photo{}_{}'.format(photo['owner_id'], photo['id'])
        self.vk.messages.send(user_id=event.obj.from_id,
                              attachment=attachment,
                              group_id=self.group_id)
