import atexit
import logging
import os
from urllib.parse import urlparse, uses_netloc

from peewee import PostgresqlDatabase
from prettytable import PrettyTable
from telegram import ParseMode, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, BaseFilter, CallbackQueryHandler, MessageHandler, Filters

from config import TOKEN, HEROKU_APP

from data.messages import messages, Message
from data.languages import languages, Language
from data.buttons import buttons, Button
from db import get_user, Wish, db, Room, User, get_rooms
from my_scheduler import MyScheduler
import scraper


def start(bot, update):
    msg = '\n'.join(messages[Message.START][language] for language in languages.keys()) + '\n\n' + \
          '\n'.join(messages[Message.CHOOSE_LANGUAGE][language] for language in languages.keys())
    kb = ReplyKeyboardMarkup([[KeyboardButton(s)] for s in languages.values()], resize_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id, text=msg,
                     reply_markup=kb,
                     parse_mode=ParseMode.MARKDOWN)


class ChooseLangFilter(BaseFilter):
    def filter(self, message):
        return message.text in languages.values()


def choose_lang(bot, update):
    lang = list(languages.keys())[list(languages.values()).index(update.message.text)]

    user = get_user(update.message.chat_id)
    user.lang = lang.value
    user.save()

    bot.send_message(chat_id=update.message.chat_id,
                     text=messages[Message.LANGUAGE_CHANGED][lang],
                     parse_mode=ParseMode.MARKDOWN)
    main_menu(bot, update)


class ChangeLangMenuFilter(BaseFilter):
    def filter(self, message):
        return message.text in buttons[Button.CHANGE_LANGUAGE].values()


def change_lang_menu(bot, update):
    user = get_user(update.message.chat_id)
    user_language = Language(user.lang)

    msg = '\n'.join(messages[Message.CHOOSE_LANGUAGE][language] for language in languages.keys())
    kb = ReplyKeyboardMarkup([
        [KeyboardButton(s)] for s in list(languages.values()) + [buttons[Button.BACK_TO_SETTINGS][user_language]]
    ], resize_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id,
                     text=msg,
                     reply_markup=kb,
                     parse_mode=ParseMode.MARKDOWN)


class MainMenuFilter(BaseFilter):
    def filter(self, message):
        return message.text in buttons[Button.BACK_TO_MAIN_MENU].values()


def main_menu(bot, update):
    user = get_user(update.message.chat_id)
    user_language = Language(user.lang)

    msg = messages[Message.MAIN_MENU][user_language]
    kb = ReplyKeyboardMarkup([
        [KeyboardButton(s)] for s in (buttons[Button.SETTINGS][user_language], buttons[Button.WISH_LIST][user_language])
    ], resize_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id,
                     text=msg,
                     reply_markup=kb,
                     parse_mode=ParseMode.MARKDOWN)


class InfoFilter(BaseFilter):
    def filter(self, message):
        return message.text in buttons[Button.INFORMATION].values()


def info(bot, update):
    user = get_user(update.message.chat_id)
    user_language = Language(user.lang)

    msg = messages[Message.INFORMATION][user_language]
    kb = ReplyKeyboardMarkup([[KeyboardButton(buttons[Button.BACK_TO_SETTINGS][user_language])]],
                             resize_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id,
                     text=msg,
                     reply_markup=kb,
                     parse_mode=ParseMode.MARKDOWN)


class MyWishesFilter(BaseFilter):
    def filter(self, message):
        return message.text in buttons[Button.WISH_LIST].values() or message.text in buttons[
            Button.BACK_TO_WISH_LIST].values()


def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


def my_wishes(bot, update):
    user = get_user(update.message.chat_id)
    user_language = Language(user.lang)

    kb = ReplyKeyboardMarkup([
        [KeyboardButton(s)] for s in (buttons[Button.ADD_WISH][user_language],
                                      buttons[Button.BACK_TO_MAIN_MENU][user_language])
    ], resize_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id,
                     text=messages[Message.MY_WISHES][user_language],
                     reply_markup=kb,
                     parse_mode=ParseMode.MARKDOWN)

    wishes = user.wishes
    if len(wishes) == 0:
        bot.send_message(chat_id=update.message.chat_id,
                         text=messages[Message.NO_WISHES][user_language],
                         parse_mode=ParseMode.MARKDOWN)
    else:
        table = PrettyTable()
        table.field_names = [
            messages[Message.NUMBER][user_language],
            messages[Message.DORMITORY][user_language],
            messages[Message.FEMALE_BEDS][user_language],
            messages[Message.MALE_BEDS][user_language],
            messages[Message.CAPACITY][user_language]
        ]
        btns = []
        counter = 1
        for w in wishes:
            table.add_row([x if x is not None else '-' for x in (counter,
                                                                 w.dormitory,
                                                                 w.female_beds,
                                                                 w.male_beds,
                                                                 w.capacity)])
            btns += [InlineKeyboardButton(text=str(counter), callback_data=str(w.id))]
            counter += 1
        bot.send_message(chat_id=update.message.chat_id,
                         text=f'```{table}```',
                         reply_markup=InlineKeyboardMarkup(build_menu(btns, n_cols=5)),
                         parse_mode=ParseMode.MARKDOWN)


class SettingsFilter(BaseFilter):
    def filter(self, message):
        return message.text in buttons[Button.SETTINGS].values() or message.text in buttons[
            Button.BACK_TO_SETTINGS].values()


def settings(bot, update):
    user = get_user(update.message.chat_id)
    user_language = Language(user.lang)

    kb = ReplyKeyboardMarkup([
        [KeyboardButton(s)] for s in (buttons[Button.CHANGE_LANGUAGE][user_language],
                                      buttons[Button.INFORMATION][user_language],
                                      buttons[Button.BACK_TO_MAIN_MENU][user_language])
    ], resize_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id,
                     text=messages[Message.SETTINGS][user_language],
                     reply_markup=kb,
                     parse_mode=ParseMode.MARKDOWN)


class AddWishFilter(BaseFilter):
    def filter(self, message):
        return message.text in buttons[Button.ADD_WISH].values()


def add_wish(bot, update):
    user = get_user(update.message.chat_id)
    user_language = Language(user.lang)

    kb = ReplyKeyboardMarkup([[KeyboardButton(buttons[Button.BACK_TO_WISH_LIST][user_language])]], resize_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id,
                     text=messages[Message.ADD_WISH][user_language],
                     reply_markup=kb,
                     parse_mode=ParseMode.MARKDOWN)


class ParseWishFilter(BaseFilter):
    def filter(self, message):
        text = message.text.replace('\t', '').replace(' ', '')
        data = text.split(',')
        if len(data) != 4:
            return False
        for i in range(4):
            if data[i] != '' and not data[i].isdigit():
                return False
        return True


def parse_wish(bot, update):
    user = get_user(update.message.chat_id)
    user_language = Language(user.lang)

    text = update.message.text.replace('\t', '').replace(' ', '')
    data = text.split(',')
    for i in range(4):
        data[i] = int(data[i]) if data[i] else None
    Wish.create(dormitory=data[0], female_beds=data[1], male_beds=data[2], capacity=data[3], user=user)

    bot.send_message(chat_id=update.message.chat_id,
                     text=messages[Message.WISH_ADDED][user_language],
                     parse_mode=ParseMode.MARKDOWN)
    my_wishes(bot, update)


def wish_info(bot, update):
    user = get_user(update.callback_query.from_user.id)
    user_language = Language(user.lang)
    data = int(update.callback_query.data)

    msg = f'{messages[Message.WISH_STATUS][user_language]}\n'

    rooms_q = get_rooms(data)
    if rooms_q.count() == 0:
        msg += messages[Message.NO_MATCHES][user_language]
    else:
        msg += messages[Message.AVAILABLE_ROOMS][user_language] + '\n'
        counter = 1
        for room in rooms_q:
            msg += f'{counter}. {room.dormitory}, {room.number}\n'
            counter += 1
    kb = ReplyKeyboardMarkup([[KeyboardButton(s)] for s in (
        f'{buttons[Button.REMOVE_WISH][user_language]} {data}',
        buttons[Button.BACK_TO_WISH_LIST][user_language])])
    bot.send_message(chat_id=update.callback_query.from_user.id,
                     text=msg,
                     reply_markup=kb,
                     parse_mode=ParseMode.MARKDOWN)


class RemoveWishFilter(BaseFilter):
    def filter(self, message):
        return any(message.text.startswith(x) for x in buttons[Button.REMOVE_WISH].values())


def remove_wish(bot, update):
    user = get_user(update.message.chat_id)
    user_language = Language(user.lang)

    Wish.delete().where(Wish.id == int(update.message.text.split(' ')[-1])).execute()

    bot.send_message(chat_id=update.message.chat_id,
                     text=messages[Message.WISH_DELETED][user_language],
                     parse_mode=ParseMode.MARKDOWN)
    my_wishes(bot, update)


@atexit.register
def goodbye():
    global my_scheduler
    scraper.active = False
    my_scheduler.clear()


if __name__ == '__main__':
    uses_netloc.append('postgres')
    url = urlparse(os.environ['DATABASE_URL'])
    db.initialize(PostgresqlDatabase(database=url.path[1:],
                                     user=url.username,
                                     password=url.password,
                                     host=url.hostname,
                                     port=url.port))

    # Connect to our database.
    db.connect()

    # Create the tabactive les.
    db.create_tables([User, Wish, Room])

    # Enable logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Set up the Updater
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Add handlers
    dispatcher.add_handler(CommandHandler('start', start))

    choose_lang_filter = ChooseLangFilter()
    dispatcher.add_handler(MessageHandler(Filters.text & choose_lang_filter, choose_lang))

    change_lang_menu_filter = ChangeLangMenuFilter()
    dispatcher.add_handler(MessageHandler(Filters.text & change_lang_menu_filter, change_lang_menu))

    main_menu_filter = MainMenuFilter()
    dispatcher.add_handler(MessageHandler(Filters.text & main_menu_filter, main_menu))

    info_filter = InfoFilter()
    dispatcher.add_handler(MessageHandler(Filters.text & info_filter, info))

    my_wishes_filter = MyWishesFilter()
    dispatcher.add_handler(MessageHandler(Filters.text & my_wishes_filter, my_wishes))

    settings_filter = SettingsFilter()
    dispatcher.add_handler(MessageHandler(Filters.text & settings_filter, settings))

    add_wish_filter = AddWishFilter()
    dispatcher.add_handler(MessageHandler(Filters.text & add_wish_filter, add_wish))

    parse_wish_filter = ParseWishFilter()
    dispatcher.add_handler(MessageHandler(Filters.text & parse_wish_filter, parse_wish))

    remove_wish_filter = RemoveWishFilter()
    dispatcher.add_handler(MessageHandler(Filters.text & remove_wish_filter, remove_wish))

    dispatcher.add_handler(CallbackQueryHandler(wish_info))

    # Start the webhook
    updater.start_webhook(listen="0.0.0.0",
                          port=int(os.environ.get('PORT', '8443')),
                          url_path=TOKEN)
    updater.bot.set_webhook(f'https://{HEROKU_APP}.herokuapp.com/{TOKEN}')

    my_scheduler = MyScheduler()
    scraper.scrap()
    my_scheduler.every(20).minutes.do(scraper.scrap)
    my_scheduler.every(20).minutes.do(lambda: scraper.notify(updater.bot))

    my_scheduler.run_continuously()

    updater.idle()
