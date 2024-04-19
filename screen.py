from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from kivy.core.window import Window, WindowBase
from kivy.metrics import dp
from kivy.properties import StringProperty, NumericProperty
Window: WindowBase
from kivy.clock import Clock


FRAMES = 1/40


class ScreenSimulate(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        
        self.g = -9.81          # N/kg
        self.m = 80             # kg
        self.vi = 4   # m/s
        
        self.v = 0
        self.Em = 0
        self.Epp = 0
        self.Ec = 0
        
        self.homer = Homer()
        self.simulator = Simulator()
        self.form = Form(parent=self)
        self.simulator.add_widget(self.homer)
        self.add_widget(self.simulator)
        self.add_widget(self.form)
        
        Clock.schedule_interval(self.loop, FRAMES)
    
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
    
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'spacebar':
            if self.homer.y == 0:
                self.v = self.vi
                #self.Em = self.m / 2 * self.v**2
    
    def loop(self, *args):
        self.homer.center_x = self.simulator.center_x
        
        """Epp = self.m * self.g * self.homer.y
        
        Ec = self.Em - Epp
        
        self.v = (abs(Ec) / self.m * 2)**0.5
        
        if Ec < 0:
            self.v = -self.v"""
        
        self.v += self.g * FRAMES
        
        self.homer.y += self.v * FRAMES * 100
        
        if self.homer.y < 0:
            self.homer.y = 0
            self.v = 0


class Simulator(RelativeLayout):
    pass


class Form(BoxLayout):
    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(FormItem(title='Gravité (N/kg)', name='g', coef=-1, parent=parent))
        self.add_widget(FormItem(title='Masse (kg)', name='m', parent=parent))
        self.add_widget(FormItem(title='Vitesse initiale (m/s)', name='vi', parent=parent))


class FormItem(BoxLayout):
    title = StringProperty('')
    name = StringProperty('')
    coef = NumericProperty(1)
    
    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)
        self.ids['text_input'].text = str(abs(parent.__getattribute__(self.name)))
    
    def on_release(self, *args):
        try:
            value = int(self.ids['text_input'].text) * self.coef
            print(value)
            self.parent.parent.__setattr__(self.name, value)
            print("Validé")
        except Exception as e:
            print(f"Erreur: {e}")


class Homer(Image):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (175, 195)
        self.source = 'homer.png'
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and self.y == 0:
            self.parent.parent.v = self.parent.parent.vi
        return super().on_touch_down(touch)