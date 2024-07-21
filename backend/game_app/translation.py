from modeltranslation.translator import translator, TranslationOptions
from .models import Game


class GameTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


translator.register(Game, GameTranslationOptions)
