import os
import unittest
from unittest.mock import patch, MagicMock
import main
from pokemon_name_translator import PokemonNameTranslator
from pokemon_report import PokemonReport


class TestMain(unittest.TestCase):
    @patch("main.PokemonService")
    @patch("main.PokemonNameTranslator")
    @patch("main.PokemonReport")
    def test_main(self, mock_report, mock_translator, mock_service):
        mock_service_instance = mock_service.return_value
        mock_service_instance.get_pokemon_info.return_value = {"name": "pikachu", "type": "electric"}

        mock_translator_instance = mock_translator.return_value
        mock_translator_instance.translate.return_value = "pikachu (FR)"

        mock_report_instance = mock_report.return_value
        mock_report_instance.generate_report = MagicMock()

        main.main()

        mock_service_instance.get_pokemon_info.assert_called_once_with("pikachu")

        mock_translator_instance.translate.assert_called_once_with("pikachu", target_language="fr")

        mock_report_instance.generate_report.assert_called_once_with(
            {"name": "pikachu", "type": "electric"},
            "pikachu (FR)",
            "pokemon_report.pdf"
        )

class TestPokemonNameTranslator(unittest.TestCase):
    @patch("pokemon_name_translator.translate.TranslationServiceClient")
    def test_translate(self, mock_translation_client):
        mock_client_instance = mock_translation_client.return_value
        mock_client_instance.translate_text.return_value.translations = [
            MagicMock(translated_text="Pikachu (FR)")
        ]

        mock_client_instance.location_path.return_value = "projects/your-project-id/locations/global"

        translator = PokemonNameTranslator()
        result = translator.translate("pikachu", target_language="fr")

        mock_client_instance.translate_text.assert_called_once_with(
            parent="projects/your-project-id/locations/global",
            contents=["pikachu"],
            target_language_code="fr",
        )

        self.assertEqual(result, "Pikachu (FR)")


class TestPokemonReport(unittest.TestCase):
    def setUp(self):
        self.report = PokemonReport()
        self.pokemon_info = {
            "height": 4,
            "weight": 60,
            "abilities": [{"ability": {"name": "static"}}, {"ability": {"name": "lightning-rod"}}],
        }
        self.translated_name = "Pikachu (FR)"

    def test_create_html_report(self):
        html_file = self.report.create_html_report(self.pokemon_info, self.translated_name)

        self.assertTrue(os.path.exists(html_file))

        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("<title>Pokemon Report</title>", content)
            self.assertIn("<strong>Name:</strong> Pikachu (FR)", content)
            self.assertIn("<strong>Height:</strong> 4 decimetres", content)
            self.assertIn("<strong>Weight:</strong> 60 hectograms", content)
            self.assertIn("<strong>Abilities:</strong> static, lightning-rod", content)

        os.remove(html_file)

    @patch("pokemon_report.pdfkit.from_file")
    def test_generate_report(self, mock_pdfkit):
        output_pdf = "pokemon_report.pdf"

        self.report.generate_report(self.pokemon_info, self.translated_name, output_pdf)

        mock_pdfkit.assert_called_once_with("report_template.html", output_pdf, configuration=unittest.mock.ANY)


if __name__ == "__main__":
    unittest.main()

