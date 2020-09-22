from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pytz
import collections
from progress_bar import progress
from settings import update_list
from Chat import Chat


def _get_name(user_id):
    request = requests.get("https://vk.com/id" + str(user_id))
    bs = BeautifulSoup(request.text, "lxml")
    user_name = bs.find("title").text
    return user_name.split()[0] + " " + user_name.split()[1]


class VkBot:
    def __init__(self):
        print("Alina was born")
        self._commands = ["!алина", "!алина завтра", "!алина сегодня", "!команды", "!обновление", "понимаю",
                          "!обновления", "панимаю", "ЗаХаРеВиЧ", "!обновление все", "!флуд"]
        request = requests.get('https://itmo.ru/ru/schedule/0/M3206/raspisanie_zanyatiy_M3206.htm')
        self._itmo_schedule = BeautifulSoup(request.text, 'lxml')
        request = requests.get("http://www.xn--80aajbde2dgyi4m.xn--p1ai/")
        parsed_text = BeautifulSoup(request.text, 'lxml')
        day = parsed_text.find("p", id="day").text
        self._prev_day = day
        self._flood = {}
        self._flood_amount = collections.Counter()

    @staticmethod
    def _get_time():
        tz = pytz.timezone('Europe/Moscow')
        time = datetime.now(tz=tz).strftime('%H:%M:%S')
        time = time[:-1]
        time = time[:-1]
        return time[:-1]

    @staticmethod
    def _get_day():
        request = requests.get("http://www.xn--80aajbde2dgyi4m.xn--p1ai/")
        parsed_text = BeautifulSoup(request.text, 'lxml')
        day = parsed_text.find("p", id="day").text
        return day

    def _get_info(self):
        if self._itmo_schedule.find("strong").text == 'нечетная':
            request = requests.get('https://itmo.ru/ru/schedule/0/M3206/2/raspisanie_zanyatiy_M3206.htm')
        else:
            request = requests.get('https://itmo.ru/ru/schedule/0/M3206/1/raspisanie_zanyatiy_M3206.htm')
        parsed_text = BeautifulSoup(request.text, 'html5lib')
        switch = {
            'Понедельник': '1day',
            'Вторник': '2day',
            'Среда': '3day',
            'Четверг': '4day',
            'Пятница': '5day',
            'Суббота': '6day',
            'Воскресенье': '7day',
        }
        more_lessons = False
        temp_lesson = ""
        temp_day = parsed_text.find("table", id=switch.get(self._get_day()))
        if temp_day is not None:
            for tag in temp_day.find("tbody").find_all("tr"):
                temp_time = tag.select_one(".time")
                if temp_time is not None:
                    time = temp_time.find("span").text.split('-')
                    lesson_block = tag.select_one(".lesson").find("dd").text
                    if time[0] >= self._get_time() and not more_lessons:
                        more_lessons = True
                        temp_lesson = lesson_block
                    if time[0] <= self._get_time() <= time[1]:
                        lesson = lesson_block
                        teacher = tag.select_one(".lesson").find("b").text.replace('\n', "").replace(" ", "")
                        if teacher == "":
                            return "Выпиваю с незнакомцем, ведущим " + lesson + " (" + time[0] + "-" + time[1] + ")"
                        output_teacher = ""
                        for letter in teacher:
                            if letter.lower() != letter:
                                output_teacher += ' '
                            output_teacher += letter
                        return "Закрепляю сидром " + lesson + " (" + time[0] + "-" + time[1] + ")" + output_teacher
                if more_lessons:
                    time = temp_time.find("span").text.split('-')
                    return "Попиваю сидр в ожидании пары (" + temp_lesson + ")\nНачало в " + time[0]
        return "Сейчас отдыхаю. Сидр попиваю. Тейлор снимаю"

    def _day_info(self, which_day):
        switch = {
            0: '1day',
            1: '2day',
            2: '3day',
            3: '4day',
            4: '5day',
            5: '6day',
            6: '7day',
        }
        switch2 = {
            'Понедельник': 0,
            'Вторник': 1,
            'Среда': 2,
            'Четверг': 3,
            'Пятница': 4,
            'Суббота': 5,
            'Воскресенье': 6,
        }
        if switch.get(self._get_day()) != 'Воскресенье':
            if self._itmo_schedule.find("strong").text == 'нечетная':
                request = requests.get('https://itmo.ru/ru/schedule/0/M3206/2/raspisanie_zanyatiy_M3206.htm')
            else:
                request = requests.get('https://itmo.ru/ru/schedule/0/M3206/1/raspisanie_zanyatiy_M3206.htm')
        else:
            if self._itmo_schedule.find("strong").text == 'нечетная':
                request = requests.get('https://itmo.ru/ru/schedule/0/M3206/1/raspisanie_zanyatiy_M3206.htm')
            else:
                request = requests.get('https://itmo.ru/ru/schedule/0/M3206/2/raspisanie_zanyatiy_M3206.htm')
        parsed_text = BeautifulSoup(request.text, 'html5lib')
        temp_day = parsed_text.find("table", id=switch.get((switch2.get(self._get_day()) + which_day) % 7))
        table = ""
        if which_day == 0:
            table = "Сегодня пью на:\n"
        elif which_day == 1:
            table = "Завтра буду пить на:\n"
        if temp_day is not None:
            for tag in temp_day.find("tbody").find_all("tr"):
                temp_time = tag.select_one(".time")
                if temp_time is not None:
                    time = temp_time.find("span").text.split('-')
                    lesson_block = tag.select_one(".lesson").find("dd").text
                    teacher = tag.select_one(".lesson").find("b").text.replace('\n', "").replace(" ", "")
                    table += lesson_block + " (" + time[0] + "-" + time[1] + ")"
                    output_teacher = ""
                    if teacher != "":
                        for letter in teacher:
                            if letter.lower() != letter:
                                output_teacher += ' '
                            output_teacher += letter
                    table += output_teacher + '\n----\n'
            return table
        return "В этот день отдыхаю. Сидр попиваю. Тейлор снимаю"

    @staticmethod
    def _command_info():
        return "Список команд:\n1) !алина: ближайшая пара на сегодня\n2) !алина сегодня: расписание на сегодня\n3) " \
               "!алина завтра: расписание на завтра\n4) !обновление: новости о последнем обновлении\n5) !обновление " \
               "все: список всех последних обновлений\n6) !флуд: активность участников беседы"

    @staticmethod
    def _update():
        return "Update 4:\n1) Новая команда: !флуд"
    
    @staticmethod
    def _update_all():
        return update_list

    def _participation(self, chat_id):
        output = ""
        for key, value in self._flood[chat_id].get_all().items():
            output += str(key) + ": " + str(value) + " " + progress(value, self._flood_amount[chat_id]) + '\n'
        return output

    def new_message(self, message, user_id, chat_id):
        if self._flood.get(chat_id) is None:
            self._flood[chat_id] = Chat()
        self._flood[chat_id].plus(user_id)
        self._flood_amount[chat_id] += 1
        switch_time = {
            'Понедельник': 0,
            'Вторник': 1,
            'Среда': 2,
            'Четверг': 3,
            'Пятница': 4,
            'Суббота': 5,
            'Воскресенье': 6,
        }
        if switch_time.get(self._prev_day) > switch_time.get(self._get_day()):
            self._prev_day = self._get_day()
            request = requests.get('https://itmo.ru/ru/schedule/0/M3206/raspisanie_zanyatiy_M3206.htm')
            self._itmo_schedule = BeautifulSoup(request.text, 'lxml')
        if message.lower() == self._commands[0]:
            return self._get_info()
        if message.lower() == self._commands[1]:
            return self._day_info(1)
        if message.lower() == self._commands[2]:
            return self._day_info(0)
        if message.lower() == self._commands[3]:
            return self._command_info()
        if message.lower() == self._commands[4] or message.lower() == self._commands[6]:
            return self._update()
        if message.lower() == self._commands[5] or message.lower() == self._commands[7]:
            return "Спасибо за понимание"
        if message == self._commands[8]:
            return "зАхАрЕвИч!"
        if message.lower() == self._commands[9]:
            return self._update_all()
        if message.lower() == self._commands[10]:
            return self._participation(chat_id)
        return "no"
