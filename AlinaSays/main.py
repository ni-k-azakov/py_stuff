import random
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from vk_bot import VkBot
import requests

token = "Здеся Был Токен Но Я Его Убрал"
vk_session = vk_api.VkApi(token=token)

print("Server started")
while True:
    longpoll = VkBotLongPoll(vk_session, 198784996)
    vk = vk_session.get_api()
    bot = VkBot()
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if bot.new_message(event.object.message['text']) != "no":
                    vk.messages.send(peer_id=event.object.message['peer_id'],
                                     message=bot.new_message(event.object.message['text']),
                                     random_id=random.randint(0, 2048))
    except requests.exceptions.ReadTimeout as timeout:
        continue
