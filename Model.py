import csv


class Model:
    def __init__(self):
        self._header = []  # Ootame päist
        self._data = []  # Ootame sisu

    # GETTERID ja SETTERID
    def get_header(self):
        return self._header

    def set_header(self, header):
        self._header = header

    def get_data(self):
        return self._data

    def set_data(self, data):
        self._data = data

    def load_data(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file:  # Vormindame utf-8 ja avame read-onlyna
                reader = csv.reader(file, delimiter=';')  # Eraldajaks ";"
                rows = list(reader)  # Loeme kõik read
                self.set_header(rows[0])  # Esimene rida on päis
                self.set_data(rows[1:])  # Järgmised read on andmed
            return True
        except FileNotFoundError:  # Probleemid
            print("Faili avamine ebaõnnestus. Faili ei leitud.")
            return False

    def search(self, query):  # Otsingu funktsioon
        results = []  # Paneme tulemused listi
        for row in self.get_data():
            for item in row:
                if query.lower().strip() in str(item).lower():  # Muundame otsingut, et erroreid ei tuleks
                    results.append(row)
                    break
        return results
