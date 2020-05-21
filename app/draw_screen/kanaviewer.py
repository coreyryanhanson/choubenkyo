import json
import pickle
import numpy as np
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.graphics import Color, Rectangle, Line
from kivy.properties import DictProperty, StringProperty, ListProperty, NumericProperty

from kivy.clock import Clock

class KanaViewer(Widget):

    character = DictProperty(None)
    strokes = DictProperty({})
    path = StringProperty("")
    charbox_pos = ListProperty([0, 0])
    charbox_width = NumericProperty(0)
    charbox_height = NumericProperty(0)
    character_color = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super(KanaViewer, self).__init__(**kwargs)
        self.characters = self.parse_json('app/draw_screen/characters/hiragana.json')

        # Removing two outdated characters
        self.characters.pop(44)
        self.characters.pop(44)

        self.character = np.random.choice(self.characters)

        self.charclock = Clock.schedule_once(self.do_nothing, .1)
        self.lineclock = Clock.schedule_once(self.do_nothing, .1)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.clear_writing()
            self.character_color = [1, 1, 1, 0]
            x, y = self.charbox_pos[0], self.charbox_pos[1]
            width, height = self.charbox_width, self.charbox_height
            strokes = self.unpack_line_data(f"app/draw_screen/characters/hiragana/{self.character['char_id']}.pickle", (x,x+width), (y,y+height))
            self.animate_character(strokes)

    def animate_character(self, points):
        self.charclock.cancel()
        self.lineclock.cancel()
        self.charclock = Clock.schedule_interval(self.new_stroke, .9)
        self.drawlines = []

    def do_nothing(self, *args):
        pass

    def new_stroke(self, *args):
        if len(self.points_queue) == 0:
            self.charclock.cancel()
            self.clear_writing()
            self.character_color = [1, 1, 1, 1]
            return
        with self.canvas:
            self.drawlines.append(Line(points=[], width=3))
            timing = .4 / len(self.points_queue[0]) if len(self.points_queue[0]) > 0 else 1
            self.lineclock = Clock.schedule_interval(self.anim_line, timing)
            self.anim_line()

    def anim_line(self, *args):
        if len(self.points_queue[0]) == 0:
            self.lineclock.cancel()
            self.points_queue.pop(0)
            return
        x = self.points_queue[0].pop(0)
        y = self.points_queue[0].pop(0)
        self.drawlines[-1].points += [x, y]

    def load_pickle(self, path):
        with open(path, "rb") as f:
            return pickle.load(f)

    def clear_writing(self):
        #self.children[0].children[1].canvas.clear()
        del self.canvas.children[2:]


    def rescale_line_coords(self, point_list, x_range, y_range):
        stacked = np.vstack(point_list)
        x_min, x_max = stacked.T[0].min(), stacked.T[0].max()
        y_min, y_max = stacked.T[1].min(), stacked.T[1].max()
        x_span, y_span = x_max - x_min, y_max - y_min
        x_cent, y_cent = (x_min + x_max) / 2, (y_min + y_max) / 2
        h_point_ratio = x_span / y_span
        h_screen_ratio = (x_range[1] - x_range[0]) / (y_range[1]- y_range[0])
        if h_point_ratio > h_screen_ratio:
            new_span = y_span / h_screen_ratio * h_point_ratio
            y_min, y_max = y_cent - new_span / 2, y_cent + new_span / 2
        else:
            new_span = x_span / h_point_ratio * h_screen_ratio
            x_min, x_max = x_cent - new_span / 2, x_cent + new_span / 2
        scaled_x = [np.interp(points.T[0], (x_min, x_max), x_range) for points in point_list]
        scaled_y = [np.interp(points.T[1], (y_min, y_max), y_range) for points in point_list]
        new_points = [np.stack((x, y)).T.reshape(-1).tolist() for x, y in list(zip(scaled_x, scaled_y))]
        self.points_queue = new_points
        return new_points

    def unpack_line_data(self, path, x_range, y_range):
        raw = self.load_pickle(path)
        unpacked = [value for key, value in sorted(raw.items())]
        scaled = self.rescale_line_coords(unpacked, x_range, y_range)
        return scaled

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