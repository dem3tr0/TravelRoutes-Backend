from django.core.cache import cache
from .models import BannedWord
import re


def get_banned_words():
    return BannedWord.objects.all().values_list('word', flat=True)


def compile_list(words):
    if words:
        pattern = r'\b(?:' + '|'.join(map(re.escape, words)) + r')\b'
        return re.compile(pattern, re.IGNORECASE)
    return re.compile(r'(?!x)x')  # Регулярное выражение, которое никогда не найдёт совпадений


class Moderation:
    CACHE_KEY_BANNED_WORDS = 'banned_words_regex'
    CACHE_TIMEOUT = 3600  # Время жизни кэша в секундах (1 час)

    def get_regex(self):
        # Попытка получить скомпилированное регулярное выражение из кэша
        regex = cache.get(self.CACHE_KEY_BANNED_WORDS)
        if regex is None:
            # Если в кэше нет, загружаем список запрещённых слов и компилируем регулярное выражение
            words = get_banned_words()
            regex = compile_list(words)
            # Сохраняем в кэше
            cache.set(self.CACHE_KEY_BANNED_WORDS, regex, self.CACHE_TIMEOUT)
        return regex

    def moderate(self, text: str) -> bool:
        regex = self.get_regex()
        if regex:
            return regex.search(text) is None
        # Если регулярное выражение не удалось получить, считаем описание неподходящим
        return False
