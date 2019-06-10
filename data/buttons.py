from data.languages import Language
from enum import Enum, auto, unique


@unique
class Button(Enum):
    BACK_TO_MAIN_MENU = auto()
    BACK_TO_SETTINGS = auto()
    BACK_TO_WISH_LIST = auto()
    SETTINGS = auto()
    CHANGE_LANGUAGE = auto()
    WISH_LIST = auto()
    INFORMATION = auto()
    ADD_WISH = auto()
    REMOVE_WISH = auto()


buttons = {
    Button.BACK_TO_MAIN_MENU: {
        Language.ENGLISH: 'Back to main menu',
        Language.RUSSIAN: 'Вернуться в главное меню'
    },
    Button.SETTINGS: {
        Language.ENGLISH: 'Settings',
        Language.RUSSIAN: 'Настройки'
    },
    Button.CHANGE_LANGUAGE: {
        Language.ENGLISH: 'Change language',
        Language.RUSSIAN: 'Изменить язык'
    },
    Button.WISH_LIST: {
        Language.ENGLISH: 'My wishes',
        Language.RUSSIAN: 'Мои желания'
    },
    Button.INFORMATION: {
        Language.ENGLISH: 'Information',
        Language.RUSSIAN: 'Информация'
    },
    Button.ADD_WISH: {
        Language.ENGLISH: 'Add wish',
        Language.RUSSIAN: 'Добавить желание'
    },
    Button.BACK_TO_SETTINGS: {
        Language.ENGLISH: 'Back to settings',
        Language.RUSSIAN: 'Вернуться к настройкам'
    },
    Button.BACK_TO_WISH_LIST: {
        Language.ENGLISH: 'Back to wish list',
        Language.RUSSIAN: 'Вернуться к списку желаний'
    },
    Button.REMOVE_WISH: {
        Language.ENGLISH: 'Delete wish',
        Language.RUSSIAN: 'Удалить желание'
    },
}
