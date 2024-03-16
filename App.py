from Model import Model
from View import View
from Controller import Controller


class App:
    def __init__(self):
        self.model = Model()
        self.view = View(Controller(self.model, self))
        self.controller = Controller(self.model, self.view)
        self.view.controller = self.controller
        self.view.run()


if __name__ == "__main__":
    app = App()
