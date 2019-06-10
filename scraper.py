import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from lxml import html
from telegram import ParseMode

from config import SPBU_LOGIN, SPBU_PASS
from data.languages import Language
from data.messages import messages, Message
from db import get_room, get_rooms, User

ua = UserAgent(use_cache_server=False)
base_url = 'https://campus-free.spbu.ru'
login_url = f'{base_url}/en/site/login'
ua_chrome = str(ua.chrome)

active = True


def scrap():
    global active
    with requests.Session() as s:
        result = s.get(login_url, headers={'User-Agent': ua_chrome})
        tree = html.fromstring(result.text)
        authenticity_token = list(set(tree.xpath("//input[@name='_csrf']/@value")))[0]

        payload = {
            "LoginForm[username]": SPBU_LOGIN,
            "LoginForm[password]": SPBU_PASS,
            "_csrf": authenticity_token
        }

        s.post(
            login_url,
            data=payload,
            headers={'referer': login_url, 'User-Agent': ua_chrome}
        )

        counter = 1
        for i in range(300):
            if not active:
                break
            try:
                soup = BeautifulSoup(s.get(f'{base_url}/en/site/index?page={i}').content, features="lxml")
                rows = soup.findChildren('tbody')[0].findChildren('tr')
                for row in rows:
                    try:
                        cells = row.findChildren('td')
                        room = get_room(dormitory=int(cells[0].string.split("№")[-1].strip()), number=cells[1].string)
                        room.female_beds = int(cells[2].string)
                        room.male_beds = int(cells[3].string)
                        room.capacity = int(cells[5].string)
                        room.save()
                        counter += 1
                    except:
                        pass
            except:
                pass


def notify(bot):
    global active
    try:
        for user in User.select():
            if not active:
                break
            user_language = Language(user.lang)
            for wish in user.wishes:
                try:
                    if not active:
                        break
                    rooms_q = get_rooms(wish.id)
                    msg = ''
                    if rooms_q.count() != 0:
                        counter = 1
                        msg += messages[Message.ROOMS_FOUND][user_language] + f'{wish.id}:\n'
                        for room in rooms_q:
                            if not active:
                                break
                            msg += f'{counter}. {room.dormitory}, {room.number}\n'
                            counter += 1
                        bot.send_message(chat_id=user.id,
                                         text=msg,
                                         parse_mode=ParseMode.MARKDOWN)
                except:
                    pass
    except:
        pass
