from enum import auto, Enum, unique

from data.languages import Language


@unique
class Message(Enum):
    START = auto()
    CHOOSE_LANGUAGE = auto()
    LANGUAGE_CHANGED = auto()
    MAIN_MENU = auto()
    SETTINGS = auto()
    MY_WISHES = auto()
    INFORMATION = auto()
    ADD_WISH = auto()
    WISH_ADDED = auto()
    NO_WISHES = auto()
    DORMITORY = auto()
    FEMALE_BEDS = auto()
    MALE_BEDS = auto()
    CAPACITY = auto()
    NUMBER = auto()
    WISH_DELETED = auto()
    WISH_STATUS = auto()
    NO_MATCHES = auto()
    AVAILABLE_ROOMS = auto()
    ROOMS_FOUND = auto()


messages = {
    Message.START: {
        Language.ENGLISH: 'Hello!',
        Language.RUSSIAN: 'Привет!'
    },
    Message.CHOOSE_LANGUAGE: {
        Language.ENGLISH: 'Choose language',
        Language.RUSSIAN: 'Выберете язык'
    },
    Message.LANGUAGE_CHANGED: {
        Language.ENGLISH: 'Language changed to English',
        Language.RUSSIAN: 'Язык изменен на русский'
    },
    Message.MAIN_MENU: {
        Language.ENGLISH: 'Main menu',
        Language.RUSSIAN: 'Основное меню'
    },
    Message.SETTINGS: {
        Language.ENGLISH: 'Settings',
        Language.RUSSIAN: 'Настройки'
    },
    Message.INFORMATION: {
        Language.ENGLISH: 'SPbU Campus Notifier Bot v. 1.0',
        Language.RUSSIAN: 'СПбГУ Кампус Нотифайер Бот в. 1.0'
    },
    Message.MY_WISHES: {
        Language.ENGLISH: 'My wishes:',
        Language.RUSSIAN: 'Мои желания:'
    },
    Message.ADD_WISH: {
        Language.ENGLISH: 'Enter _dormitory_, _available female beds_, _available male beds_ and _capacity_ '
                          'separated by commas. If some parameters are unnecessary then just skip them.\n\nFor example: if you '
                          'want to live in 10th dormitory in room with 3 beds such that 2 of them already occupied by girls '
                          'then enter\n`10,1,,3`',
        Language.RUSSIAN: 'Введите через запятую _общежитие_, _количество свободных женских мест_, _мужских_ и _общую '
                          'вместимость_. '
                          'Если какие-то параметры несущественны, то просто пропустите их.\n\nПример: если вы хотите '
                          'жить в 10 общежитии в комнате с 3 кроватями, две из которых уже заняты девушками, '
                          'то введите\n`10,1,,3`'
    },
    Message.WISH_ADDED: {
        Language.ENGLISH: 'Wish added!',
        Language.RUSSIAN: 'Желание добавлено!'
    },
    Message.NO_WISHES: {
        Language.ENGLISH: 'You have no wishes',
        Language.RUSSIAN: 'У вас пока нет желаний'
    },
    Message.DORMITORY: {
        Language.ENGLISH: 'Dorm.',
        Language.RUSSIAN: 'Общ.'
    },
    Message.FEMALE_BEDS: {
        Language.ENGLISH: '♀',
        Language.RUSSIAN: '♀'
    },
    Message.MALE_BEDS: {
        Language.ENGLISH: '♂',
        Language.RUSSIAN: '♂'
    },
    Message.CAPACITY: {
        Language.ENGLISH: 'Cap.',
        Language.RUSSIAN: 'Вмес.'
    },
    Message.NUMBER: {
        Language.ENGLISH: '#',
        Language.RUSSIAN: '№'
    },
    Message.WISH_DELETED: {
        Language.ENGLISH: 'Wish deleted!',
        Language.RUSSIAN: 'Желание удалено!'
    },
    Message.WISH_STATUS: {
        Language.ENGLISH: 'Current wish status:',
        Language.RUSSIAN: 'Текущее состояние желания:'
    },
    Message.NO_MATCHES: {
        Language.ENGLISH: 'Rooms which match this wish not found',
        Language.RUSSIAN: 'Не найдено комнат, удовлеторяющих этому желанию'
    },
    Message.AVAILABLE_ROOMS: {
        Language.ENGLISH: 'Available rooms:',
        Language.RUSSIAN: 'Список доступных комнат:',
    },
    Message.ROOMS_FOUND: {
        Language.ENGLISH: 'New rooms found for wish ',
        Language.RUSSIAN: 'Найдены новые результаты по желанию ',
    }
}
