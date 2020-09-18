import random
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from vk_bot import VkBot
import requests


token = "e6082b87a5ca9afe1590078622439c06a62a0e72da39c025dc8fe33b18a764e7668a71d30ba89a484431d"
vk_session = vk_api.VkApi(token=token)

print("Server started")
while True:
    longpoll = VkBotLongPoll(vk_session, 198784996)
    vk = vk_session.get_api()
    bot = VkBot()
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                message = bot.new_message(event.object.message['text'])
                if message != "no":
                    vk.messages.send(peer_id=event.object.message['peer_id'],
                                     message=message,
                                     random_id=random.randint(0, 2048))
    except requests.exceptions.ReadTimeout as timeout:
        continue
