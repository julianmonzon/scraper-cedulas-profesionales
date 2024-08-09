import os
import tkinter as tk
from tkinter import messagebox
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from multiprocessing import Process
from cedulas_profesionales.spiders.cedulas_profesionales import CedulasProfesionalesSpider

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Búsqueda de Cédulas Profesionales")
        self.geometry("600x400")

        self.create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.is_scraping = False
        self.is_searching = True  # Flag to track if we are searching or showing results

    def create_widgets(self):
        """Create widgets for user input and search button."""
        tk.Label(self, text="Nombre").grid(row=0, column=0, padx=10, pady=10)
        self.nombre_entry = tk.Entry(self)
        self.nombre_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self, text="Apellido Paterno").grid(row=1, column=0, padx=10, pady=10)
        self.paterno_entry = tk.Entry(self)
        self.paterno_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self, text="Apellido Materno").grid(row=2, column=0, padx=10, pady=10)
        self.materno_entry = tk.Entry(self)
        self.materno_entry.grid(row=2, column=1, padx=10, pady=10)

        self.search_button = tk.Button(self, text="Buscar", command=self.handle_search_button)
        self.search_button.grid(row=3, column=0, columnspan=2, pady=20)

        self.reset_button = tk.Button(self, text="Reset", command=self.reset_fields)
        self.reset_button.grid(row=3, column=1, pady=20)

        self.results_text = tk.Text(self, wrap=tk.WORD, width=70, height=10)
        self.results_text.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def handle_search_button(self):
        """Handle the action for the search button based on the current mode."""
        if self.is_searching:
            self.start_scraper()
        else:
            self.read_results()

    def start_scraper(self):
        """Start the Scrapy spider to search for records."""
        if self.is_scraping:
            messagebox.showwarning("Advertencia", "El scraper ya está en ejecución.")
            return

        try:
            nombre = self.nombre_entry.get()
            paterno = self.paterno_entry.get()
            materno = self.materno_entry.get()

            def run_spider():
                self.is_scraping = True
                settings = get_project_settings()
                process = CrawlerProcess(settings=settings)
                process.crawl(CedulasProfesionalesSpider, nombre=nombre, paterno=paterno, materno=materno)
                process.start(stop_after_crawl=True)
                self.is_scraping = False

            process = Process(target=run_spider)
            process.start()

            # Cambia el texto del botón a "Mostrar Resultados" después de iniciar el scraper
            self.search_button.config(text="Mostrar Resultados")
            self.is_searching = False

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def read_results(self):
        """Read the results from the text file and display them in the Text widget."""
        results_path = os.path.join(os.getcwd(), 'results.txt')
        if os.path.exists(results_path):
            with open(results_path, 'r', encoding='utf-8') as f:
                self.results_text.delete("1.0", tk.END)
                self.results_text.insert(tk.END, f.read())
        else:
            self.results_text.delete("1.0", tk.END)
            self.results_text.insert(tk.END, "No se encontraron resultados.")

    def reset_fields(self):
        """Reset the input fields and results."""
        self.nombre_entry.delete(0, tk.END)
        self.paterno_entry.delete(0, tk.END)
        self.materno_entry.delete(0, tk.END)
        self.results_text.delete("1.0", tk.END)
        # Restablecer el estado de scraping
        self.is_scraping = False
        self.is_searching = True
        self.search_button.config(text="Buscar")  # Cambia el texto del botón a "Buscar"

    def on_closing(self):
        """Handle the closing of the window."""
        self.destroy()

if __name__ == "__main__":
    app = Application()
    app.mainloop()
