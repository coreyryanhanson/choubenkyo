import json
import numpy as np
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.graphics import Color, Rectangle
from kivy.properties import DictProperty, StringProperty


class KanaViewer(Widget):

    character = DictProperty(None)
    strokes = DictProperty({})
    path = StringProperty("")

    def __init__(self, **kwargs):
        super(KanaViewer, self).__init__(**kwargs)
        self.characters = self.parse_json('app/draw_screen/characters/hiragana.json')

        # Removing two outdated characters
        self.characters.pop(44)
        self.characters.pop(44)

        self.character = np.random.choice(self.characters)


    def update_char(self, obj):
        self.character = np.random.choice(self.characters)

    def parse_json(self, path):
        with open(path) as f:
          return json.load(f)


class KanaViewerTest(App):

    def build(self):
        return KanaViewer()


if __name__ == '__main__':
    Builder.load_file('app/draw_screen/kanaviewer.kv')
    KanaViewerTest().run()