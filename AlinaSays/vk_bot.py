from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pytz
import collections
import random
from progress_bar import progress
from Chat import Chat


class VkBot:
    def __init__(self):
        print("Alina was born")
        self._commands = ["!алина", "!алина завтра", "!алина сегодня", "!команды", "!обновление", "понимаю",
                          "!обновления", "панимаю", "ЗаХаРеВиЧ", "!обновление все", "!флуд", "!сайт",
                          "!флуд точно", "!save state", "!дедлайны", "!анекдот"]
        request = requests.get('https://itmo.ru/ru/schedule/0/M3206/raspisanie_zanyatiy_M3206.htm')
        self._itmo_schedule = BeautifulSoup(request.text, 'lxml')
        request = requests.get("http://www.xn--80aajbde2dgyi4m.xn--p1ai/")
        parsed_text = BeautifulSoup(request.text, 'lxml')
        day = parsed_text.find("p", id="day").text
        self._prev_day = day
        self._flood = {}
        self._id_to_name = {}
        self._flood_amount = collections.Counter()
        self._load_state()

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

    def _get_name(self, user_id):
        if self._id_to_name.get(user_id) is None:
            request = requests.get("https://vk.com/id" + str(user_id))
            bs = BeautifulSoup(request.text, "lxml")
            user_name = bs.find("title").text
            self._id_to_name[user_id] = user_name.split()[0] + " " + user_name.split()[1]
        return self._id_to_name[user_id]

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

    def _deadlines(self):
        request = requests.get('https://usachova.gitbook.io/m3206/')
        parsed_text = BeautifulSoup(request.text, 'html5lib')
        table = parsed_text.find("tbody")
        week = []
        deadlines = []
        for row in table.find_all("tr"):
            parsed_row = row.find_all("td")
            day = row.find("p").text
            if day == "день недели":
                continue
            week.append(parsed_row[0].find("p").text)
            deadline = parsed_row[1].find("p").text.replace('\u200b', "")
            deadlines.append(deadline)
        output = "---Дедлайны недели---\n"
        for i in range(0, len(deadlines)):
            if not deadlines[i]:
                continue
            week[i] = week[i][0].upper() + week[i][1:]
            output += week[i] + ": " + deadlines[i] + '\n'
        return output

    @staticmethod
    def _command_info():
        return "Список команд Алины:\n1) !алина: ближайшая пара на сегодня\n2) !алина сегодня: расписание на" \
               " сегодня\n3) " \
               "!алина завтра: расписание на завтра\n4) !обновление: новости о последнем обновлении\n5) !обновление " \
               "все: список всех последних обновлений\n6) !флуд: активность участников беседы в процентах\n7) !сайт: " \
               "ссылочка на Машин сайт со всей инфой по парам\n8) !флуд точно: активность участников беседы (" \
               "количество сообщений + проценты)\n9) !дедлайны: дедлайны этой недели \n10) !анекдот: случайный" \
               " анекдот уровня Б\n\n---\n\nСписок команд Махи:\n1) !очередь [ооп/оси]: текущая очередь\n" \
               "2) !запись [ооп/оси]: встать в очередь\n3) !запись последним [ооп/оси] - встать в конец очереди" \
               "\n4) !очистить [ооп/оси] - кнопка смерти"

    @staticmethod
    def _update():
        return "Update 9:\n1) в список команд добавлены команды бота Махи\n"
    
    @staticmethod
    def _update_all():
        return "Update 1:\n1) Команда `алина говорит` изменена на !алина\n2) Новая команда: !алина сегодня\n3) Новая " \
              "команда: !алина завтра\n4) Новая команда: !команды\n----\nUpdate 2:\n1) Пиво было заменено на сидр\n" \
              "2) Новая команда: !обновление все\n----\nUpdate 3:\n1) Sunday bug fix\n----\nUpdate 4:\n" \
              "1) Новая команда: !флуд \n----\nUpdate 5:\n1) Новая команда: !сайт\n2) У команды !флуд изменен " \
              "функционал. Теперь показывается только процент флуда (для отображения количества сообщений теперь " \
              "другая команда - !флуд точно)\n3) Новая команда: !флуд точно\n4) Команды !флуд и !флуд точно больше " \
              "не учитывают сообщения с командами\n----\nUpdate 6:\n1) Ускорена работа команд !флуд и !флуд точно\n" \
              "2) Теперь бот сохраняет активность участников даже после обновления\n---\nUpdate 7:\n" \
              "1) Новая команда: !дедлайны\n---\nUpdate 8:\n1) Новая команда: !анекдот\n2) Микро фиксы\n---\nUpdate " \
               "9:\n1) в список команд добавлены команды бота Махи"

    @staticmethod
    def joke():
        joke_id = int(random.random() * 1142)
        request = requests.get('https://baneks.ru/' + str(joke_id))
        request.encoding = 'utf8'
        parsed_text = BeautifulSoup(request.text, 'html5lib')
        joke = parsed_text.find("article").find("p").text
        return joke

    def _participation(self, chat_id, message):
        output = ""
        for key, value in self._flood[chat_id].get_all().items():
            output += self._get_name(key) + ": "
            if message == self._commands[12]:
                output += str(value) + '\n'
            output += progress(value, self._flood_amount[chat_id]) + '\n'
        if output == "":
            return "Пока всё тихо..."
        return output

    def _save_state(self):
        file = open('flood.txt', 'w')
        for key, value in self._flood.items():
            file.write('index: ' + str(key) + ' ' + str(self._flood_amount[key]) + '\n')
            for key_2, value_2 in self._flood[key].get_all().items():
                file.write(str(key_2) + ' ' + str(value_2) + '\n')
        file.close()
        file = open('id_to_name.txt', 'w')
        for key, value in self._id_to_name.items():
            file.write(str(key) + " " + value + '\n')
        file.close()

    def _load_state(self):
        file = open('flood.txt', 'r')
        temp_chat = ''
        for line in file:
            if line == '':
                continue
            if line.split()[0] == 'index:':
                temp_chat = int(line.split()[1])
                self._flood[temp_chat] = Chat()
                self._flood_amount[temp_chat] = int(line.split()[2])
                continue
            temp_user = int(line.split()[0])
            for _ in range(0, int(line.split()[1])):
                self._flood[temp_chat].plus(temp_user)
        file.close()
        file = open('id_to_name.txt', 'r')
        for line in file:
            if line == '':
                continue
            self._id_to_name[int(line.split()[0])] = line.split()[1] + " " + line.split()[2]
        file.close()

    def new_message(self, message, user_id, chat_id):
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
            self._save_state()
            return "Спасибо за понимание"
        if message == self._commands[8]:
            self._save_state()
            return "зАхАрЕвИч!"
        if message.lower() == self._commands[9]:
            return self._update_all()
        if message.lower() == self._commands[10] or message.lower() == self._commands[12]:
            self._save_state()
            return self._participation(chat_id, message.lower())
        if message.lower() == self._commands[11]:
            self._save_state()
            return "usachova.gitbook.io"
        if message.lower() == self._commands[13]:
            self._save_state()
            return "Saved"
        if message.lower() == self._commands[14]:
            self._save_state()
            return self._deadlines()
        if message.lower() == self._commands[15]:
            return self.joke()
        if self._flood.get(chat_id) is None:
            self._flood[chat_id] = Chat()
        self._flood[chat_id].plus(user_id)
        self._flood_amount[chat_id] += 1
        return "no"
