from modeltranslation.translator import translator, TranslationOptions
from .models import EcoBranch


class EcoBranchTranslationOptions(TranslationOptions):
    fields = ('name', 'information')


translator.register(EcoBranch, EcoBranchTranslationOptions)
