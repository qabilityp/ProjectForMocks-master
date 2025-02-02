# pokemon_name_translator.py
from google.cloud import translate

class PokemonNameTranslator:
    def __init__(self):
        self.client = translate.TranslationServiceClient()

    def translate(self, text, target_language="en"):
        parent = self.client.location_path("your-project-id", "global")
        response = self.client.translate_text(
            parent=parent,
            contents=[text],
            target_language_code=target_language,
        )

        for translation in response.translations:
            return translation.translated_text
