__author__ = 'Ania'
"""
Nalezy napisac gre Pong na urzadzenie mobilne
"""
#:kivy 1.9.0
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, Clock, \
        ObjectProperty
from kivy.vector import Vector

"""
klasa reprezentujaca pilke (jej ruch)
"""
class Pilka(Widget):

    # predkosc pilki na osiach x i y
    predkosc_x = NumericProperty(10000)
    predkosc_y = NumericProperty(10000)
    predkosc = ReferenceListProperty(predkosc_x, predkosc_y)

    def ruch(self):
        self.pos = Vector(*self.predkosc) + self.pos
"""
klasa reprezentujaca paletke tenisowa
"""
class Paletka(Widget):

    wynik = NumericProperty(0)

    def odbicie_pilki(self, pilka):
        if self.collide_widget(pilka):
            px, py = pilka.predkosc
            offset = (pilka.center_y - self.center_y) / (self.height / 2)
            odbicie = Vector(-1 * px,py)
            pred = odbicie * 1.1
            pilka.predkosc = pred.x, pred.y + offset
"""
klasa przedstawiajaca gre
"""
class GraPong(Widget):
    pilka = ObjectProperty(None)
    gracz1 = ObjectProperty(None)
    gracz2 = ObjectProperty(None)

    def serw_pilki(self, pred = (4,0)):
        self.pilka.center = self.center
        self.pilka.predkosc = pred

    def odswiez(self, dt):
        self.pilka.ruch()

        # ruch paletek
        self.gracz1.odbicie_pilki(self.pilka)
        self.gracz2.odbicie_pilki(self.pilka)

        # ruch pilki gora-dol
        if(self.pilka.y< self.y) or (self.pilka.top > self.top):
            self.pilka.predkosc_y *= -1

        # zdobycie punktu
        if self.pilka.x < self.x:
            self.gracz2.wynik += 1
            self.serw_pilki(pred=(4, 0))
        if self.pilka.x > self.width:
            self.gracz1.wynik += 1
            self.serw_pilki(pred=(-4, 0))

    #poruszanie paletkami przez uzytkownika
    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.gracz1.center_y = touch.y
        if touch.x > self.width - self.width /3:
            self.gracz2.center_y = touch.y

"""
aplikacja
"""
class PongApp(App):
    def build(self):
        gra = GraPong()
        gra.serw_pilki()
        Clock.schedule_interval(gra.odswiez, 1.0/60.0)
        return gra
"""
uruchomienie gry
"""
if __name__ == '__main__':
    PongApp().run()