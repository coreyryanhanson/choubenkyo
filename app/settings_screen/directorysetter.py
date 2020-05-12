from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Line
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder

Builder.load_file('app/settings_screen/directorysetter.kv')

class SaveDialogue(Popup):
    def __init__(self, **kwargs):
        super(SaveDialogue, self).__init__(**kwargs)

class DirectorySetter(Widget):
    def __init__(self, **kwargs):
        super(DirectorySetter, self).__init__(**kwargs)

    def prompt_save(self, obj):
        show = SaveDialogue


class DirectorySetterTest(App):

    def build(self):
        return DirectorySetter()


if __name__ == '__main__':
    DirectorySetterTest().run()