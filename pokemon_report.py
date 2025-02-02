# pokemon_report.py
import pdfkit
import os
config = pdfkit.configuration(wkhtmltopdf=os.path.abspath(os.path.join("wkhtmltox", "bin","wkhtmltopdf.exe")))

class PokemonReport:
    def generate_report(self, pokemon_info, translated_name, output_pdf):
        # Create an HTML report
        html_report = self.create_html_report(pokemon_info, translated_name)

        # Convert HTML to PDF
        pdfkit.from_file(html_report, output_pdf, configuration=config)

    def create_html_report(self, pokemon_info, translated_name):
        # Format abilities as a comma-separated list
        abilities = ", ".join(ability["ability"]["name"] for ability in pokemon_info["abilities"])

        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Pokemon Report</title>
        </head>
        <body>
            <h1>Pokemon Report</h1>
            <p><strong>Name:</strong> {translated_name}</p>
            <p><strong>Height:</strong> {pokemon_info['height']} decimetres</p>
            <p><strong>Weight:</strong> {pokemon_info['weight']} hectograms</p>
            <p><strong>Abilities:</strong> {abilities}</p>
        </body>
        </html>
        """

        # Create HTML report by substituting values into the template
        html_report = html_template.format(translated_name=translated_name, pokemon_info=pokemon_info, abilities=abilities)

        # Save the HTML report to a file
        with open("report_template.html", "w", encoding="utf-8") as f:
            f.write(html_report)

        return "report_template.html"
