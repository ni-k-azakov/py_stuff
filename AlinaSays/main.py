import random
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from settings import vk_group_token, vk_group_id
from vk_bot import VkBot
import requests


token = vk_group_token
vk_session = vk_api.VkApi(token=token)

print("Server started")
bot = VkBot()
while True:
    longpoll = VkBotLongPoll(vk_session, vk_group_id)
    vk = vk_session.get_api()
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                message = bot.new_message(event.object.message['text'], event.object.message['from_id'],
                                          event.object.message['peer_id'])
                if message != "no":
                    vk.messages.send(peer_id=event.object.message['peer_id'],
                                     message=message,
                                     random_id=random.randint(0, 2048))
    except requests.exceptions.ReadTimeout as timeout:
        continue
    except requests.exceptions.ConnectionError as timeout:
        continue
