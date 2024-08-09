import os
from scrapy.http import FormRequest, Request
from cedulas_profesionales.spiders.base import BaseSpider

class CedulasProfesionalesSpider(BaseSpider):
    name = "cedulas_profesionales"

    INIT_URL = "https://www.buholegal.com"
    SEARCH_URL = INIT_URL + "/consultasep/"

    def __init__(self, *args, nombre=None, paterno=None, materno=None, **kwargs):
        super(CedulasProfesionalesSpider, self).__init__(*args, **kwargs)
        self.nombre = nombre
        self.paterno = paterno
        self.materno = materno
        self.results = None  # Asegúrate de definir el atributo results

    def start_requests(self):
        """Start the scraping process by checking the availability of the website."""
        self.logger.info(f"Opening spider: {self.name}")

        init_request = Request(
            url=self.INIT_URL,
            callback=self.search_cedula,
            errback=self.errback_httpbin,
            dont_filter=True,
        )
        yield init_request

    def search_cedula(self, response):
        """Initiate a cedula search by submitting a form with specific search criteria."""
        self.logger.info(f"The website {response.request.url} is up and running.")

        formdata = {
            "nombre": self.nombre or "",
            "paterno": self.paterno or "",
            "materno": self.materno or "",
        }

        self.logger.info("Starting a license search...")

        request = FormRequest(
            url=self.SEARCH_URL,
            method="POST",
            formdata=formdata,
            callback=self.extract_cedula_records,
            errback=self.errback_httpbin,
        )
        
        yield request

    def extract_cedula_records(self, response):
        """Extract and process license records from the search results page."""
        self.logger.info("Extracting and processing license records...")

        rows = response.xpath('//div[@class="table-responsive"]//tbody/tr')

        match len(rows):
            case 0:
                self.logger.error("No se encontraron resultados")
                self.results = "No se encontraron resultados"
            case _:
                self.results = self.extract_data(rows)
        
        self.save_results()  # Guarda los resultados en un archivo

    def extract_record(self, row):
        """Extract details from a single row in the search results page."""
        try:
            return {
                'cedula': self.clean_text(row.xpath('.//th[1]/a/text()').get()),
                'tipo': self.clean_text(row.xpath('.//td[1]/text()').get()),
                'nombre_completo': self.clean_text(row.xpath('.//td[2]/text()').get()),
                'carrera': self.clean_text(row.xpath('.//th[2]/text()').get()),
                'universidad': self.clean_text(row.xpath('.//td[3]/text()').get()),
                'estado': self.clean_text(row.xpath('.//th[3]/text()').get()),
                'año': self.clean_text(row.xpath('.//td[4]/text()').get())
            }
        except Exception as e:
            self.logger.error(f"Error extracting record: {e}")
            return {}

    def extract_data(self, rows):
        """Extract details from multiple rows in the search results page."""
        records = {}
        for index, row in enumerate(rows):
            record = self.extract_record(row)
            if record:
                records[index] = record
        self.logger.info(f"Multiple records found: {records}")
        return records

    def save_results(self):
        """Save the results to a text file."""
        results_path = os.path.join(os.getcwd(), 'results.txt')
        with open(results_path, 'w', encoding='utf-8') as f:
            # Asegúrate de que self.results sea un diccionario
            if isinstance(self.results, dict):
                for idx, record in self.results.items():
                    if isinstance(record, dict):
                        f.write(f"Registro {idx + 1}:\n")
                        for key, value in record.items():
                            f.write(f"{key.capitalize()}: {value}\n")
                        f.write("\n")
                    else:
                        f.write(f"Registro {idx + 1}: {record}\n")
                        f.write("\n")
            else:
                # Imprime el contenido de self.results si no es un diccionario
                f.write(f"{self.results}\n")