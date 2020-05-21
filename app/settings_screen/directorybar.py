import os
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from android import storage
from kivy.config import Config
from kivy.app import App


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
    dir_prefix = StringProperty(storage.primary_external_storage_path())

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

class DirectoryBar(Widget):
    full_filepath = StringProperty("Warning: Choose A Directory")
    file_prefix = StringProperty("")
    text_color = ListProperty([1, 0, 0, 1])

    def __init__(self, **kwargs):
        super(DirectoryBar, self).__init__(**kwargs)

    def dismiss_popup(self):
        self._popup.dismiss()

    def prompt_save(self):
        if self.full_filepath != "Warning: Choose A Directory":
            saver = SaveDialog(save=self.save, cancel=self.dismiss_popup, dir_prefix=self.full_filepath)
        else:
            saver = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Choose_directory and prefix", content=saver,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def save(self, path, name):
        self.full_filepath = path
        self.file_prefix = name
        self.dismiss_popup()
        self.text_color = [1, 1, 1, 1]
        config = App.get_running_app().config
        config.set('saving', 'filepath', self.full_filepath)
        config.set('saving', 'file_prefix', self.file_prefix)
        config.write()


class DirectoryBarTest(App):

    def build(self):
        return DirectoryBar()


if __name__ == '__main__':
    Builder.load_file('app/settings_screen/directorybar.kv')
    DirectoryBarTest().run()