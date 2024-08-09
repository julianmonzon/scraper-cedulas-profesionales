import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from cedulas_interface import Application 

class TestApplication(unittest.TestCase):
    def setUp(self):
        self.app = Application()

    def tearDown(self):
        self.app.destroy()

    def test_initial_state(self):
        self.assertFalse(self.app.is_scraping)
        self.assertTrue(self.app.is_searching)
        self.assertEqual(self.app.search_button.cget('text'), 'Buscar')

    def test_reset_fields(self):
        self.app.nombre_entry.insert(0, 'Diego')
        self.app.paterno_entry.insert(0, 'Vazquez')
        self.app.materno_entry.insert(0, 'Monzon')
        self.app.results_text.insert('1.0', 'Results')

        self.app.reset_fields()

        self.assertEqual(self.app.nombre_entry.get(), '')
        self.assertEqual(self.app.paterno_entry.get(), '')
        self.assertEqual(self.app.materno_entry.get(), '')
        self.assertEqual(self.app.results_text.get('1.0', tk.END).strip(), '')
        self.assertFalse(self.app.is_scraping)
        self.assertTrue(self.app.is_searching)
        self.assertEqual(self.app.search_button.cget('text'), 'Buscar')

    @patch('cedulas_interface.messagebox')
    def test_handle_search_button_when_scraping(self, mock_messagebox):
        self.app.is_scraping = True
        self.app.handle_search_button()
        mock_messagebox.showwarning.assert_called_once_with("Advertencia", "El scraper ya está en ejecución.")

    @patch('cedulas_interface.Application.read_results')
    def test_handle_search_button_show_results(self, mock_read_results):
        self.app.is_searching = False
        self.app.handle_search_button()
        mock_read_results.assert_called_once()

    @patch('cedulas_interface.CrawlerProcess')
    @patch('cedulas_interface.Process')
    def test_start_scraper(self, mock_Process, mock_CrawlerProcess):
        self.app.nombre_entry.insert(0, 'Diego')
        self.app.paterno_entry.insert(0, 'Vazquez')
        self.app.materno_entry.insert(0, 'Monzon')

        process_mock = MagicMock()
        mock_Process.return_value = process_mock

        self.app.start_scraper()

        self.assertEqual(self.app.search_button.cget('text'), 'Mostrar Resultados')
        self.assertFalse(self.app.is_searching)
        process_mock.start.assert_called_once()

    @patch('cedulas_interface.os.path.exists', return_value=True)
    @patch('cedulas_interface.open', new_callable=unittest.mock.mock_open, read_data='Mocked results')
    def test_read_results_file_exists(self, mock_open, mock_exists):
        self.app.read_results()
        self.assertEqual(self.app.results_text.get('1.0', tk.END).strip(), 'Mocked results')

    @patch('cedulas_interface.os.path.exists', return_value=False)
    def test_read_results_file_not_exists(self, mock_exists):
        self.app.read_results()
        self.assertEqual(self.app.results_text.get('1.0', tk.END).strip(), 'No se encontraron resultados.')

if __name__ == '__main__':
    unittest.main()
