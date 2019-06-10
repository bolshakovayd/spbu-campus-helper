from enum import Enum, unique


@unique
class Language(Enum):
    ENGLISH = 0
    RUSSIAN = 1


languages = {
    Language.ENGLISH: 'English',
    Language.RUSSIAN: 'Русский'
}
