import os
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Line
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty

class NewFolderDialog(FloatLayout):
    cancel = ObjectProperty(None)
    text_input = ObjectProperty(None)
    create = ObjectProperty(None)
    path = StringProperty("")

    def __init__(self, **kwargs):
        super(NewFolderDialog, self).__init__(**kwargs)

class SaveDialog(FloatLayout):
    cancel = ObjectProperty(None)
    text_input = ObjectProperty(None)
    save = ObjectProperty(None)
    create_dir = ObjectProperty(None)
    dir_prefix = StringProperty("/storage/emulated/0/")

    def __init__(self, **kwargs):
        super(SaveDialog, self).__init__(**kwargs)

    def cancel_folder(self):
        self._popup.dismiss()

    def create_folder(self, path):
        os.mkdir(path)
        self.dir_prefix = path
        self.cancel_folder()

    def prompt_folder(self, path):
        option = NewFolderDialog(create=self.create_folder, cancel=self.cancel_folder, path=path)
        self._popup = Popup(title="New Folder", content=option,
                            size_hint=(1, .3))
        self._popup.open()

class DirectorySetter(Widget):
    full_filepath = StringProperty("No directory")

    def __init__(self, **kwargs):
        super(DirectorySetter, self).__init__(**kwargs)

    def dismiss_popup(self):
        self._popup.dismiss()

    def prompt_save(self):
        saver = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Choose_directory and prefix", content=saver,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def save(self, path, name):
        self.full_filepath = f"{path}/{name}"
        self.dismiss_popup()


class DirectorySetterTest(App):

    def build(self):
        return DirectorySetter()


if __name__ == '__main__':
    Builder.load_file('app/settings_screen/directorysetter.kv')
    DirectorySetterTest().run()