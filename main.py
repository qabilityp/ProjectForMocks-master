# main.py
from pokemon_service import PokemonService
from pokemon_name_translator import PokemonNameTranslator
from pokemon_report import PokemonReport

def main():
    # Initialize services
    pokemon_service = PokemonService()
    translator = PokemonNameTranslator()
    report_generator = PokemonReport()

    # Get Pokemon information
    pokemon_name = "pikachu"
    pokemon_info = pokemon_service.get_pokemon_info(pokemon_name)

    if pokemon_info:
        # Translate Pokemon name
        translated_name = translator.translate(pokemon_name, target_language="fr")

        # Generate and save PDF report
        output_pdf = "pokemon_report.pdf"
        report_generator.generate_report(pokemon_info, translated_name, output_pdf)
        print(f"PDF report saved as {output_pdf}")
    else:
        print("Pokemon not found.")

if __name__ == "__main__":
    main()
