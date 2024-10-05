import numpy as np

class Display:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.widgets = []
        self.buffer = np.zeros((height, width))

    def add_widget(self, widget, offset_x, offset_y):
        # TODO: implement checks for widget overlap
        assert offset_x + widget.width < self.width
        assert offset_y + widget.height < self.height
        self.widgets.append((widget, offset_x, offset_y))

    def update(self):
        for (w, x, y) in self.widgets:
            self.buffer[y:(y+w.height), x:(x+w.width)] = w.update()
        return self.buffer


class Widget:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.buffer = np.ones([height, width])

    def update(self):
        return self.buffer

class GraphWidget(Widget):
    def __init__(self, color, interpolate=True):
        super().__init__(self)


    def plot(x, y):
        assert len(x) == len(y), "Arrays X and Y must be of same length."

    def _scale(Y):
        np.linspace

class TextWidget(Widget):
    def __init__(self, text, font, color):

        super().__init__(self)
