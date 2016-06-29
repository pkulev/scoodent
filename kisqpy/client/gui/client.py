from kivy.app import App
from kivy.uix.gridlayout import GridLayout


class LoginScreen(GridLayout):
    """Login screen widget."""

    def __init__(self, **kwargs):
#        f_username =
        super(LoginScreen, self).__init__(**kwargs)


class ClientApp(App):
    def build(self):
        return LoginScreen()
