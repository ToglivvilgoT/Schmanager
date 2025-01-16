from kivy.app import App, Widget


class MainMenu(Widget):
    pass


class SchmanagerApp(App):
    def build(self):
        return MainMenu()


if __name__ == '__main__':
    SchmanagerApp().run()