from modeltranslation.translator import translator, TranslationOptions
from .models import Game, GameInfo


class GameTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


class GameInfoTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


translator.register(Game, GameTranslationOptions)
translator.register(GameInfo, GameInfoTranslationOptions)
