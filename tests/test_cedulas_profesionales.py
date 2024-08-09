import unittest
from unittest.mock import MagicMock
from scrapy.http import HtmlResponse, FormRequest
from cedulas_profesionales.spiders.cedulas_profesionales import CedulasProfesionalesSpider

class TestCedulasProfesionalesSpider(unittest.TestCase):
    def setUp(self):
        self.spider = CedulasProfesionalesSpider(nombre="Diego", paterno="Vazquez", materno="Monzon")

    def test_search_cedula(self):
        # Mock response for search_cedula method
        response = HtmlResponse(url='https://www.buholegal.com', body=b'', encoding='utf-8')
        response.request = MagicMock(url='https://www.buholegal.com')
        results = list(self.spider.search_cedula(response))

        self.assertEqual(len(results), 1)
        self.assertIsInstance(results[0], FormRequest)
        self.assertEqual(results[0].url, self.spider.SEARCH_URL)
        self.assertEqual(results[0].method, 'POST')
        self.assertEqual(results[0].callback, self.spider.extract_cedula_records)
        self.assertEqual(results[0].errback, self.spider.errback_httpbin)

        # Verifica que la URL sea la esperada
        self.assertEqual(results[0].url, self.spider.SEARCH_URL)

    def test_extract_record(self):
        # Mock row HTML content for testing
        row_html = """
        <tr>
            <th><a>13569518</a></th>
            <td>C1</td>
            <td>DIEGO JULIAN VAZQUEZ MONZON</td>
            <th>LICENCIATURA EN CONTADURÍA</th>
            <td>UNIVERSIDAD AUTÓNOMA DE CHIAPAS</td>
            <th>CHIAPAS</th>
            <td>2023</td>
        </tr>
        """
        response = HtmlResponse(url='https://www.buholegal.com', body=row_html, encoding='utf-8')
        row = response.xpath('//tr')[0]
        record = self.spider.extract_record(row)
        
        expected_record = {
            'cedula': '13569518',
            'tipo': 'C1',
            'nombre_completo': 'DIEGO JULIAN VAZQUEZ MONZON',
            'carrera': 'LICENCIATURA EN CONTADURÍA',
            'universidad': 'UNIVERSIDAD AUTÓNOMA DE CHIAPAS',
            'estado': 'CHIAPAS',
            'año': '2023'
        }
        
        self.assertEqual(record, expected_record)

    def test_extract_data(self):
        # Mock rows HTML content for testing
        rows_html = """
        <div class="table-responsive">
            <tbody>
                <tr>
                    <th><a>13569518</a></th>
                    <td>C1</td>
                    <td>DIEGO JULIAN VAZQUEZ MONZON</td>
                    <th>LICENCIATURA EN CONTADURÍA</th>
                    <td>UNIVERSIDAD AUTÓNOMA DE CHIAPAS</td>
                    <th>CHIAPAS</th>
                    <td>2023</td>
                </tr>
                <tr>
                    <th><a>13569519</a></th>
                    <td>C2</td>
                    <td>JUAN PEREZ</td>
                    <th>INGENIERÍA</th>
                    <td>UNIVERSIDAD NACIONAL</td>
                    <th>MÉXICO</th>
                    <td>2022</td>
                </tr>
            </tbody>
        </div>
        """
        response = HtmlResponse(url='https://www.buholegal.com', body=rows_html, encoding='utf-8')
        rows = response.xpath('//tr')
        records = self.spider.extract_data(rows)

        expected_records = {
            0: {
                'cedula': '13569518',
                'tipo': 'C1',
                'nombre_completo': 'DIEGO JULIAN VAZQUEZ MONZON',
                'carrera': 'LICENCIATURA EN CONTADURÍA',
                'universidad': 'UNIVERSIDAD AUTÓNOMA DE CHIAPAS',
                'estado': 'CHIAPAS',
                'año': '2023'
            },
            1: {
                'cedula': '13569519',
                'tipo': 'C2',
                'nombre_completo': 'JUAN PEREZ',
                'carrera': 'INGENIERÍA',
                'universidad': 'UNIVERSIDAD NACIONAL',
                'estado': 'MÉXICO',
                'año': '2022'
            }
        }

        self.assertEqual(records, expected_records)

    def test_save_results(self):
        self.spider.results = {
            0: {
                'cedula': '13569518',
                'tipo': 'C1',
                'nombre_completo': 'DIEGO JULIAN VAZQUEZ MONZON',
                'carrera': 'LICENCIATURA EN CONTADURÍA',
                'universidad': 'UNIVERSIDAD AUTÓNOMA DE CHIAPAS',
                'estado': 'CHIAPAS',
                'año': '2023'
            }
        }

        self.spider.save_results()

        with open('results.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        
        expected_content = (
            "Registro 1:\n"
            "Cedula: 13569518\n"
            "Tipo: C1\n"
            "Nombre_completo: DIEGO JULIAN VAZQUEZ MONZON\n"
            "Carrera: LICENCIATURA EN CONTADURÍA\n"
            "Universidad: UNIVERSIDAD AUTÓNOMA DE CHIAPAS\n"
            "Estado: CHIAPAS\n"
            "Año: 2023\n\n"
        )

        self.assertEqual(content, expected_content)

if __name__ == '__main__':
    unittest.main()
