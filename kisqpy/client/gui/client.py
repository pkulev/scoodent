from kivy.app import App
from kivy.uix.gridlayout import GridLayout


class LoginScreen(GridLayout):
    """Login screen widget."""

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2


class ClientApp(App):
    def build(self):
        return LoginScreen()


def main():
    """Entry point."""

    ClientApp().run()
