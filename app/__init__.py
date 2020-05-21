import os
import pickle

from kivy.app import App
from .view import MainWindow
from .draw_screen import *
from .settings_screen import *
from kivy.uix.screenmanager import ScreenManager, Screen, SwapTransition


from kivy.lang import Builder
Builder.load_file('app/main.kv')

class KanaScreen(Screen):
    def __init__(self, **kwargs):
        super(KanaScreen, self).__init__(**kwargs)

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)

class AllScreens(ScreenManager):
    def __init__(self, **kwargs):
        super(AllScreens, self).__init__(**kwargs)

class Choubenkyo(App):
    def __init__(self, **kwargs):
        super(Choubenkyo, self).__init__(**kwargs)

    def save_press(self, obj):
        path, usr_prefix = self.dir_chooser.full_filepath, self.dir_chooser.file_prefix
        char_prefix = self.char_box.character["char_id"]
        instance_name = f"{char_prefix}-{usr_prefix}"
        strokes = self.main_canvas.strokes
        if len(strokes) > 0 and path != "Warning: Choose A Directory":
            count = len([item for item in os.listdir(path) if item.startswith(instance_name)])
            full_filename = f"{path}/{instance_name}_{count:04d}"
            self.save_pickle(strokes, full_filename)
            self.main_canvas.clear_canvas(obj)
            self.char_box.update_char(obj)
            print(f"Saved {full_filename}")

    def save_pickle(self, data, path):
        with open(path, "wb") as f:
            pickle.dump(data, f)

    def remember_settings(self):
        config = self.config
        self.dir_chooser.full_filepath = config.get('saving', 'filepath')
        self.dir_chooser.file_prefix = config.get('saving', 'file_prefix')
        if self.dir_chooser.full_filepath != "Warning: Choose A Directory":
            self.dir_chooser.text_color = [1, 1, 1, 1]


    def build_config(self, config):
        config.setdefaults('saving', {
            'filepath': "Warning: Choose A Directory",
            'file_prefix': ''
        })

    def build(self):
        main_app = KanaScreen()
        main_widgets = main_app.children[0].children
        self.main_canvas = main_widgets[0]
        self.dir_chooser = main_widgets[3]
        self.char_box = main_widgets[2]

        self.remember_settings()

        draw_buttons = main_widgets[1].children[0].children

        draw_buttons[0].bind(on_release=self.save_press)
        draw_buttons[1].bind(on_release=self.char_box.update_char)
        draw_buttons[2].bind(on_release=self.main_canvas.clear_canvas)
        draw_buttons[3].bind(on_release=self.main_canvas.undo)
        return main_app
