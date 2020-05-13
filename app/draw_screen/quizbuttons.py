from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.properties import ObjectProperty

Builder.load_file('app/draw_screen/quizbuttons.kv')

class ButtonText(Label):

    def __init__(self, **kwargs):
        super(ButtonText, self).__init__(**kwargs)

class QuizButtons(Widget):
    undo_button_press = ObjectProperty(None)
    clear_button_state = ObjectProperty('normal')

    def __init__(self, **kwargs):
        super(QuizButtons, self).__init__(**kwargs)


class QuizButtonsTest(App):

    def build(self):
        return QuizButtons()


if __name__ == '__main__':
    QuizButtonsTest().run()