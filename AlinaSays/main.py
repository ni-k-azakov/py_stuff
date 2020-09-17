import vk_api
import vk_bot
from vk_api.longpoll import VkLongPoll, VkEventType

bot = vk_bot.VkBot()
print(bot._get_temp_teacher())