from deep_translator import GoogleTranslator

class TranslatorAdapter:
    def translate(self, text, src="auto", dest="en"):
        # Create a translator for given languages
        translated_text = GoogleTranslator(source=src, target=dest).translate(text)
        return type("Translation", (), {"text": translated_text})
