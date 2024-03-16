import csv
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import ttk
import time


class View:
    def __init__(self, controller):
        self.top_frame = None
        self.label_log = None
        self.btn_search = None
        self.entry_search = None
        self.label_search = None
        self.btn_open_file = None
        self.bottom_frame = None
        self.log_text = None
        self.controller = controller
        self.root = Tk()
        self.root.title("Failist otsimine")
        self.center_window(500, 300)
        self.initialize()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        if messagebox.askokcancel("Kinnitage sulgemine", "Olete kindel, et soovite programmi sulgeda?"):
            self.root.destroy()

    def initialize(self):
        # Ülemine raam
        self.top_frame = Frame(self.root, padx=20, pady=20)
        self.top_frame.pack(expand=True, fill=BOTH)

        # Ava fail
        self.btn_open_file = Button(self.top_frame, text="Ava fail", command=self.open_file_dialog)
        self.btn_open_file.pack(expand=True, fill=BOTH)

        # Otsingu silt
        self.label_search = Label(self.top_frame, text="Otsingusõna:")
        self.label_search.pack(expand=True, fill=BOTH)

        # Otsingulahter
        self.entry_search = Entry(self.top_frame, state='disabled')  # Alguses disabled
        self.entry_search.pack(expand=True, fill="x")

        # Otsi nupp
        self.btn_search = Button(self.top_frame, text="Otsi", command=self.search, state='disabled')  # Alguses disabled
        self.btn_search.pack(expand=True, fill=BOTH)

        # Alumine raam:
        self.bottom_frame = Frame(self.root, padx=20, pady=20)
        self.bottom_frame.pack(expand=True, fill=BOTH)

        # Logikastike
        self.label_log = Label(self.bottom_frame, text="Logi:")
        self.label_log.pack()
        self.log_text = Label(self.bottom_frame, borderwidth=1, relief="sunken", anchor="nw", justify="left",
                              font=("Courier", 10))
        self.log_text.pack(side=LEFT, expand=True, fill=BOTH)

    # Keskendame akna
    def center_window(self, width, height):
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def open_file_dialog(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if filename:
            self.controller.open_file(filename)
            self.log_text.config(text=f"Avatud fail: {filename}\n")  # Paneb logisse kirja

            # Avame Otsi nupu ja Otsingulahtri
            self.entry_search.config(state='normal')
            self.btn_search.config(state='normal')

    def search(self):
        query = self.entry_search.get()
        if query:
            self.controller.search(query)
            self.log_text.config(text=f"{self.log_text['text']}Otsitud sõna: {query}\n")  # Läheb logisse kirja
        else:
            messagebox.showwarning("Tühiväli", "Sisestage otsingusõna!")

    def show_results(self, results):
        if results:
            start_time = time.time()  # Alustame ajamõõtmisega
            # Loome tulemuste akna
            result_window = Toplevel(self.root)
            result_window.title("Otsingutulemused")

            # Keskistame akna
            width = 800
            height = 500
            x = (self.root.winfo_screenwidth() - width) // 2
            y = (self.root.winfo_screenheight() - height) // 2
            result_window.geometry(f"{width}x{height}+{x}+{y}")

            # Loome tabeli
            tree = ttk.Treeview(result_window, style="Treeview")  # Anname talle stiili kaasa
            tree.pack(expand=True, fill="both", side="left")

            # Salvesta nupp tulemuste salvestamiseks
            btn_save = Button(result_window, text="Salvesta", command=lambda: self.save_results(result_window, results))
            btn_save.pack(side=TOP, anchor=NE, padx=10, pady=10)

            # Määrame päise vastavalt mudelist
            header = self.controller.get_header()
            tree["columns"] = header
            # Paneme Verdana fondi
            style = ttk.Style()
            style.configure("Treeview", font=("Verdana", 10))  # Loome tabelile stiili
            style.configure("Treeview.Heading", font=("Verdana", 10))  # Määrame veergudele stiili

            # Lisame vertikaalse kerimisriba
            scrollbar = ttk.Scrollbar(result_window, orient="vertical", command=tree.yview)
            scrollbar.pack(side="right", fill="y")
            tree.configure(yscrollcommand=scrollbar.set)

            # Määrame tulemusteakna laiuse vastavalt päiseveergude arvule
            width = sum(tree.column(col, "width") for col in header)
            result_window.geometry(f"{width + 20}x{height}+{x}+{y}")  # Paneme polstrit juurde

            # Lisame veergude päised
            for col in header:
                tree.heading(col, text=col, anchor="w")  # Veerupäis vasakule joondatuna
                tree.column(col, width=100, anchor="w")  # Veeru laius ja joondus vasakule
                tree.column("#0", width=40, anchor="w")  # Teeme järjekorra veeru väiksemaks

            # Kuvame andmed
            for i, row in enumerate(results, start=1):
                tree.insert("", "end", text=str(i), values=row)

            # Lisame Tulemused
            result_label = Label(result_window, text="Tulemused:")
            result_label.pack(side=TOP, anchor="w", padx=10, pady=(10, 0))

            end_time = time.time()  # Lõpetame ajamõõtmise

            # Arvutame aja ja kirjete arvu
            elapsed_time = end_time - start_time  # Kulunud aeg sekundites
            total_rows = len(results)  # Kirjete arv

            # Lisame info tekstikast
            info_text = f"Aeg: {elapsed_time:.2f} s | Kokku: {total_rows} kirjet"
            info_label = Label(result_window, text=info_text)
            info_label.pack(side=TOP, anchor="w", padx=10, pady=(0, 10))

        else:
            messagebox.showinfo("Tulemused", "Tulemusi ei leitud!")

    def run(self):
        self.root.mainloop()

    # Salvestamisvõimalus
    def save_results(self, result_window, results):
        filename = filedialog.asksaveasfilename(defaultextension=".csv",
                                                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if filename:
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(self.controller.get_header())
                for row in results:
                    writer.writerow(row)  # Salvestame iga rea
            self.log_text.config(text=f"{self.log_text['text']}Salvestatud nimega: {filename}\n")  # Logisse ka
            messagebox.showinfo("Salvestamine", "Tulemused on edukalt salvestatud!")  # Anname teada
            result_window.destroy()  # Lööb akna kinni
