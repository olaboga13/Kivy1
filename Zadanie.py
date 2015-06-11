__author__ = 'Ania'
"""
Nalezy napisac dowolna gre na urzadzenia mobilne,
tematyka nawiazujaca do synchrotronu

->aplikacja oparta na podstawie gry Pong
"""


from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
"""
klasa reprezentujaca magnes (odpowiednik paletki w Pong)
"""
class Magnet(Widget):
    score = NumericProperty(0)

    def bounce_electron(self, electron):
        if self.collide_widget(electron):
            vx, vy = electron.velocity
            offset = (electron.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            electron.velocity = vel.x, vel.y + offset

"""
klasa reprezentujaca elektron (odpowiednik pilki w Pong
"""
class Electron(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos
"""
klasa zawierajaca metody wykorzystujace wczesniej utworzone obiekty
"""
class Game(Widget):
    electron = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def serve_electron(self, vel=(4, 0)):
        self.electron.center = self.center
        self.electron.velocity = vel

    def update(self, dt):
        self.electron.move()

        #bounce of paddles
        self.player1.bounce_electron(self.electron)
        self.player2.bounce_electron(self.electron)

        #bounce ball off bottom or top
        if (self.electron.y < self.y) or (self.electron.top > self.top):
            self.electron.velocity_y *= -1

        #went of to a side to score point?
        if self.electron.x < self.x:
            self.player2.score += 1
            self.serve_electron(vel=(4, 0))
        if self.electron.x > self.width:
            self.player1.score += 1
            self.serve_electron(vel=(-4, 0))

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y

"""
uruchomienie aplikacji
"""
class MagnesGraApp(App):
    def build(self):
        game = Game()
        game.serve_electron()
        Clock.schedule_interval(game.update, 1.0 / 360.0)
        return game


if __name__ == '__main__':
    MagnesGraApp().run()