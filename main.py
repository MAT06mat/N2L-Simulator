from kivy.app import App
from kivy.core.window import Window, WindowBase
from screen import ScreenSimulate

Window: WindowBase


class SimulatorApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        return ScreenSimulate()


if __name__ == '__main__':
    SimulatorApp().run()