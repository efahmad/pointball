from kivy.app import App
from PointBall import PlayGroundWidget


class MyPaintApp(App):
    def build(self):
        play_ground_widget = PlayGroundWidget()
        play_ground_widget.draw()
        return play_ground_widget


if __name__ == '__main__':
    MyPaintApp().run()
