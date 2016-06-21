from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


class LoginScreen(GridLayout):
    """Login screen widget."""

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        self.cols = 2
        self.add_widget(Label(text="Username"))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)
        self.add_widget(Label(text="password"))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)


class ClientApp(App):
    def build(self):
        return LoginScreen()


def main():
    """Entry point."""

    ClientApp().run()
