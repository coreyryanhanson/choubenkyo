from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from .view import MainWindow
from .draw_screen import *
from kivy.uix.screenmanager import ScreenManager, Screen


from kivy.lang import Builder
Builder.load_file('app/main.kv')

class KanaScreen(Screen):
    def __init__(self, **kwargs):
        super(KanaScreen, self).__init__(**kwargs)

class Choubenkyo(App):
    def __init__(self, **kwargs):
        super(Choubenkyo, self).__init__(**kwargs)
    def build(self):
        main_app = KanaScreen()
        main_widgets = main_app.children[0].children
        main_canvas = main_widgets[0]
        char_box = main_widgets[2]
        draw_buttons = main_widgets[1].children[0].children
        draw_buttons[1].bind(on_release=char_box.update_char)
        draw_buttons[2].bind(on_release=main_canvas.clear_canvas)
        draw_buttons[3].bind(on_release=main_canvas.undo)
        return main_app