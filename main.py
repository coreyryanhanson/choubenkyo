from app import Choubenkyo
#from kivy.garden.iconfonts import register
from os.path import dirname, join

__version__ = "0.0.0"




if __name__ == '__main__':
#    register('Maticons', join(dirname(__file__), 'app/assets/fonts/Material-Design-Iconic-Font.ttf'), join(dirname(__file__), 'app/assets/fonts/zmd.fontd'))
    # register('Notoreg', join(dirname(__file__), 'app/assets/fonts/NotoSerifJP-Regular.otf'))

    Choubenkyo().run()

