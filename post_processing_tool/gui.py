import os
import tkinter as tk
from tkinter import filedialog


class FileProcessorApp:
    def __init__(self, root, callback_function):
        self.root = root
        self.callback_function = callback_function

        self.root.title("CRECE Post Processor Tool")

        self.input_file_path = tk.StringVar()
        self.output_directory_path = tk.StringVar()

        self.input_file_label = tk.Label(root, text="CSV de Mailchimp:")
        self.input_file_label.pack(pady=10)

        self.input_file_button = tk.Button(
            root, text="Selecciona CSV", command=self.get_input_file
        )
        self.input_file_button.pack(pady=5)

        self.post_process_button = tk.Button(
            root, text="Limpiar datos", command=self.post_process, bg="lightBlue"
        )
        self.post_process_button.pack(pady=10)

        self.completition_label = tk.Label(
            root, text="", wraplength=200, justify="center"
        )
        self.completition_label.pack(pady=10)

    def get_input_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Input File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )
        if file_path:
            self.input_file_path.set(file_path)
            self.input_file_label.config(text=f"Input File: {file_path}")

    def post_process(self):
        filename = self.input_file_path.get()
        out_dir = os.path.dirname(filename)
        try:
            _, output = self.callback_function(filename, out_dir)
        except Exception as e:
            print(e)
            self.completition_label.config(
                text=f"Algo salio muy mal! Error en ingles: {str(e)}", fg="red"
            )
            return
        self.completition_label.config(
            text=f"Completado. Se guardo el archivo en la misma carpeta con nombre: {output}",
            fg="green",
        )


def create_tk_root():
    root = tk.Tk()
    root.geometry("400x400")

    return root
