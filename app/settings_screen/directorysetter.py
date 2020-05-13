from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Line
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty

from android.storage import primary_external_storage_path
sd = primary_external_storage_path()


class SaveDialog(FloatLayout):
    cancel = ObjectProperty(None)
    text_input = ObjectProperty(None)
    save = ObjectProperty(None)
    dir_prefix = StringProperty("")

    def __init__(self, **kwargs):
        super(SaveDialog, self).__init__(**kwargs)

class DirectorySetter(Widget):
    def __init__(self, **kwargs):
        super(DirectorySetter, self).__init__(**kwargs)

    def dismiss_popup(self):
        self._popup.dismiss()

    def prompt_save(self):
        saver = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Choose_directory and prefix", content=saver,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def save(self, test, test2):
        pass


class DirectorySetterTest(App):

    def build(self):
        return DirectorySetter()


if __name__ == '__main__':
    Builder.load_file('app/settings_screen/directorysetter.kv')
    DirectorySetterTest().run()