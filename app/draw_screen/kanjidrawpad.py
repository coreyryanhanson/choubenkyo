import numpy as np
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Line
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import ObjectProperty, NumericProperty

Builder.load_file('app/draw_screen/kanjidrawpad.kv')

class KanjiDrawPad(Widget):
    drawing = ObjectProperty(None)
    x_canv_cent, y_canv_cent = NumericProperty(0), NumericProperty(0)
    canvas_denom = NumericProperty(0)

    def __init__(self, **kwargs):
        super(KanjiDrawPad, self).__init__(**kwargs)
        self.stroke_count = 0
        self.strokes = {}
        self.history = []

    def on_touch_down(self, touch):
        with self.children[0].children[1].canvas:
            if self.children[0].children[0].collide_point(*touch.pos):
                touch.grab(self)
                color = (1, 0, 1)
                Color(*color, mode='hsv')
                self.stroke_count += 1
                touch.ud['line'] = Line(points=(touch.x, touch.y), width=3)
                return True

    def on_touch_move(self, touch):
        if self.children[0].children[0].collide_point(*touch.pos) and touch.grab_current is self:
            touch.ud['line'].points += [touch.x, touch.y]
            return True

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            new_points_array = np.array(list(zip(touch.ud['line'].points[0::2], touch.ud['line'].points[1::2])))
            self.strokes[self.stroke_count] = (new_points_array - [self.x_canv_cent, self.y_canv_cent])/self.canvas_denom
            self.history.append(touch.ud['line'])
            print(self.strokes)
            touch.ungrab(self)
            return True

    def clear_canvas(self, obj):
        self.children[0].children[1].canvas.clear()
        self.stroke_count = 0
        self.strokes ={}

    def undo(self, obj):
        if self.stroke_count > 0:
            self.children[0].children[1].canvas.children.remove(self.history.pop(-1))
            del self.strokes[self.stroke_count]
            self.stroke_count -= 1


class KanjiDrawPadTest(App):

    def build(self):
        parent = BoxLayout()
        self.painter = KanjiDrawPad()
        clearbtn = Button(text='Clear')
        undobtn = Button(text='undo')
        clearbtn.bind(on_release=self.painter.clear_canvas)
        undobtn.bind(on_release=self.painter.undo)
        parent.add_widget(self.painter)
        parent.add_widget(clearbtn)
        parent.add_widget(undobtn)
        return parent


if __name__ == '__main__':
    KanjiDrawPadTest().run()