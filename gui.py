import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import os
import pickle

from Instrument import Instrument  # Assuming Instrument class is defined in instrument.py

class InstrumentCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Instrument Creator")

        # Variables for Instrument attributes
        self.name_var = tk.StringVar()
        self.file_var = tk.StringVar()
        self.position_var = tk.StringVar()
        self.volume_var = tk.StringVar(value="50")  # Default volume set to 50
        self.instrument_type_var = tk.StringVar(value="snare")  # Default instrument type
        
        # Options for instrument type
        self.instrument_types = ["snare", "tom", "kick", "cymbal", "hihat"]

        # Create GUI elements
        tk.Label(root, text="Name:").grid(row=0, column=0, sticky='w', padx=10, pady=5)
        tk.Entry(root, textvariable=self.name_var).grid(row=0, column=1, padx=10, pady=5)

        tk.Label(root, text="File:").grid(row=1, column=0, sticky='w', padx=10, pady=5)
        tk.Entry(root, textvariable=self.file_var, state='readonly').grid(row=1, column=1, padx=10, pady=5)
        tk.Button(root, text="Browse", command=self.browse_file).grid(row=1, column=2, padx=10, pady=5)

        tk.Label(root, text="Position:").grid(row=2, column=0, sticky='w', padx=10, pady=5)
        tk.Entry(root, textvariable=self.position_var).grid(row=2, column=1, padx=10, pady=5)

        tk.Label(root, text="Default Volume:").grid(row=3, column=0, sticky='w', padx=10, pady=5)
        tk.Entry(root, textvariable=self.volume_var).grid(row=3, column=1, padx=10, pady=5)

        tk.Label(root, text="Instrument Type:").grid(row=4, column=0, sticky='w', padx=10, pady=5)
        tk.OptionMenu(root, self.instrument_type_var, *self.instrument_types).grid(row=4, column=1, padx=10, pady=5)

        tk.Button(root, text="Create Instrument", command=self.create_instrument).grid(row=5, column=1, pady=10)

    def browse_file(self):
        file_path = filedialog.askopenfilename(initialdir="/", title="Select File",
                                               filetypes=(("WAV files", "*.wav"), ("All files", "*.*")))
        if file_path:
            self.file_var.set(file_path)

    def create_instrument(self):
        name = self.name_var.get()
        file_path = self.file_var.get()
        position = self.position_var.get()
        try:
            default_volume = int(self.volume_var.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid default volume. Please enter a number.")
            return
        
        instrument_type = self.instrument_type_var.get()

        # Save file to new directory
        try:
            new_dir = "samples/"
            os.makedirs(new_dir, exist_ok=True)

            dest_file_path = os.path.join(new_dir, name)
            if os.path.exists(dest_file_path):
                overwrite = messagebox.askyesno("File Exists", f"File '{os.path.basename(file_path)}' already exists in '{new_dir}'. Do you want to overwrite it?")
                if not overwrite:
                    messagebox.showinfo("File Not Saved", "File was not saved.")
                    return  # Exit the function or handle accordingly if user decides not to overwrite

            shutil.copy(file_path, dest_file_path)
            messagebox.showinfo("File Saved", f"File '{os.path.basename(file_path)}' saved to '{new_dir}'")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving file: {str(e)}")

        # Create Instrument object
        try:
            instrument = Instrument(name, file_path, position, instrument_type, default_volume)

            directory = "instruments/"
            os.makedirs(directory, exist_ok=True)  # Create the directory if it doesn't exist

            # Define the file path
            file_path = os.path.join(directory, f"{name}.pickle")

            # Check if the file already exists
            if os.path.exists(file_path):
                overwrite = input(f"File '{file_path}' already exists. Do you want to overwrite it? (y/n): ").strip().lower()
                if overwrite != 'y':
                    print("File not saved.")
                    exit()  # Exit the program or handle accordingly if user decides not to overwrite

            with open(file_path, "wb") as f:
                pickle.dump(instrument, f)
        except Exception as e:
            messagebox.showerror("Error", f"Error saving file: {str(e)}")
        
# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    app = InstrumentCreatorApp(root)
    root.mainloop()
