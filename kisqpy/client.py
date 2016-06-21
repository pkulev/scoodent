from kivy.app import App
from kivy.uix.label import Label


class ClientApp(App):
    def build(self):
        return Label(text="Ima label")


def main():
    """Entry point."""

    ClientApp().run()
