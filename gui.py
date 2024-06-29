import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import shutil
import os
import pickle

from Instrument import Instrument  # Assuming Instrument class is defined in instrument.py

class InstrumentCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Instrument Creator")

        # Create Notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, expand=True)

        # Create frames for each tab
        self.create_tab = ttk.Frame(self.notebook)
        self.manage_tab = ttk.Frame(self.notebook)

        # Add frames to notebook
        self.notebook.add(self.create_tab, text='Create Instrument')
        self.notebook.add(self.manage_tab, text='Manage Instruments')

        # Variables for Instrument attributes
        self.name_var = tk.StringVar()
        self.file_var = tk.StringVar()
        self.position_var = tk.StringVar()
        self.volume_var = tk.StringVar(value="50")  # Default volume set to 50
        self.instrument_type_var = tk.StringVar(value="snare")  # Default instrument type

        # Options for instrument type
        self.instrument_types = ["snare", "tom", "kick", "cymbal", "hihat"]

        # Create GUI elements for Create Instrument tab
        self.create_instrument_tab()

        # Create GUI elements for Manage Instruments tab
        self.create_manage_instruments_tab()

    def create_instrument_tab(self):
        tk.Label(self.create_tab, text="Name:").grid(row=0, column=0, sticky='w', padx=10, pady=5)
        tk.Entry(self.create_tab, textvariable=self.name_var).grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.create_tab, text="File:").grid(row=1, column=0, sticky='w', padx=10, pady=5)
        tk.Entry(self.create_tab, textvariable=self.file_var, state='readonly').grid(row=1, column=1, padx=10, pady=5)
        tk.Button(self.create_tab, text="Browse", command=self.browse_file).grid(row=1, column=2, padx=10, pady=5)

        tk.Label(self.create_tab, text="Position:").grid(row=2, column=0, sticky='w', padx=10, pady=5)
        tk.Entry(self.create_tab, textvariable=self.position_var).grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.create_tab, text="Default Volume:").grid(row=3, column=0, sticky='w', padx=10, pady=5)
        tk.Entry(self.create_tab, textvariable=self.volume_var).grid(row=3, column=1, padx=10, pady=5)

        tk.Label(self.create_tab, text="Instrument Type:").grid(row=4, column=0, sticky='w', padx=10, pady=5)
        tk.OptionMenu(self.create_tab, self.instrument_type_var, *self.instrument_types).grid(row=4, column=1, padx=10, pady=5)

        tk.Button(self.create_tab, text="Create Instrument", command=self.create_instrument).grid(row=5, column=1, pady=10)

    def create_manage_instruments_tab(self):
        self.instruments_listbox = tk.Listbox(self.manage_tab)
        self.instruments_listbox.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')
        self.instruments_listbox.bind('<<ListboxSelect>>', self.load_instrument_details)

        self.manage_tab.columnconfigure(0, weight=1)
        self.manage_tab.rowconfigure(0, weight=1)

        tk.Button(self.manage_tab, text="Refresh List", command=self.load_instruments).grid(row=1, column=0, pady=10)
        tk.Button(self.manage_tab, text="Save Changes", command=self.save_instrument_changes).grid(row=1, column=1, pady=10)

        tk.Label(self.manage_tab, text="Name:").grid(row=2, column=0, sticky='w', padx=10, pady=5)
        self.manage_name_var = tk.StringVar()
        tk.Entry(self.manage_tab, textvariable=self.manage_name_var).grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.manage_tab, text="File:").grid(row=3, column=0, sticky='w', padx=10, pady=5)
        self.manage_file_var = tk.StringVar()
        tk.Entry(self.manage_tab, textvariable=self.manage_file_var, state='readonly').grid(row=3, column=1, padx=10, pady=5)

        tk.Label(self.manage_tab, text="Position:").grid(row=4, column=0, sticky='w', padx=10, pady=5)
        self.manage_position_var = tk.StringVar()
        tk.Entry(self.manage_tab, textvariable=self.manage_position_var).grid(row=4, column=1, padx=10, pady=5)

        tk.Label(self.manage_tab, text="Default Volume:").grid(row=5, column=0, sticky='w', padx=10, pady=5)
        self.manage_volume_var = tk.StringVar()
        tk.Entry(self.manage_tab, textvariable=self.manage_volume_var).grid(row=5, column=1, padx=10, pady=5)

        tk.Label(self.manage_tab, text="Instrument Type:").grid(row=6, column=0, sticky='w', padx=10, pady=5)
        self.manage_instrument_type_var = tk.StringVar()
        tk.OptionMenu(self.manage_tab, self.manage_instrument_type_var, *self.instrument_types).grid(row=6, column=1, padx=10, pady=5)

        self.load_instruments()

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

            _, file_extension = os.path.splitext(os.path.basename(file_path))
            dest_file_path = os.path.join(new_dir, name + file_extension)
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
            instrument = Instrument(name, dest_file_path, position, instrument_type, default_volume)

            directory = "instruments/"
            os.makedirs(directory, exist_ok=True)  # Create the directory if it doesn't exist

            # Define the file path
            file_path = os.path.join(directory, f"{name}.pickle")

            # Check if the file already exists
            if os.path.exists(file_path):
                overwrite = messagebox.askyesno("File Exists", f"File '{file_path}' already exists. Do you want to overwrite it?")
                if not overwrite:
                    messagebox.showinfo("File Not Saved", "File was not saved.")
                    return  # Exit the function or handle accordingly if user decides not to overwrite

            with open(file_path, "wb") as f:
                pickle.dump(instrument, f)
        except Exception as e:
            messagebox.showerror("Error", f"Error saving file: {str(e)}")

    def load_instruments(self):
        self.instruments_listbox.delete(0, tk.END)
        directory = "instruments/"
        if os.path.exists(directory):
            for filename in os.listdir(directory):
                if filename.endswith(".pickle"):
                    self.instruments_listbox.insert(tk.END, filename[:-7])

    def load_instrument_details(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            instrument_name = event.widget.get(index)
            file_path = os.path.join("instruments/", f"{instrument_name}.pickle")
            with open(file_path, "rb") as f:
                instrument = pickle.load(f)
                self.manage_name_var.set(instrument.name)
                self.manage_file_var.set(instrument.file)
                self.manage_position_var.set(instrument.position)
                self.manage_volume_var.set(instrument.default_volume)
                self.manage_instrument_type_var.set(instrument.instrument_type)

    def save_instrument_changes(self):
        name = self.manage_name_var.get()
        file_path = self.manage_file_var.get()
        position = self.manage_position_var.get()
        try:
            default_volume = int(self.manage_volume_var.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid default volume. Please enter a number.")
            return

        instrument_type = self.manage_instrument_type_var.get()

        try:
            instrument = Instrument(name, file_path, position, instrument_type, default_volume)

            directory = "instruments/"
            os.makedirs(directory, exist_ok=True)  # Create the directory if it doesn't exist

            file_path = os.path.join(directory, f"{name}.pickle")

            with open(file_path, "wb") as f:
                pickle.dump(instrument, f)
            messagebox.showinfo("Success", "Instrument updated successfully.")
            self.load_instruments()
        except Exception as e:
            messagebox.showerror("Error", f"Error saving file: {str(e)}")


# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    app = InstrumentCreatorApp(root)
    root.mainloop()
