class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def open_file(self, filename):
        self.model.load_data(filename)

    def search(self, query):
        results = self.model.search(query)
        self.view.show_results(results)

    def get_header(self):
        return self.model.get_header()  # Kasutame getterit
