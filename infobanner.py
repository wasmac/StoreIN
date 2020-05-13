from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
import kivy.utils

class InfoBanner(GridLayout):
    def __init__(self, description, image, source, **kwargs):
        self.description = description
        self.image = image
        self.rows = 1
        self.source = source
        super(InfoBanner, self).__init__(**kwargs)
        with self.canvas.before:
            Color(rgba=(kivy.utils.get_color_from_hex("#FFFFFF"))[:3] + [.5])
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect, size=self.update_rect)
        
        #instruction (description + image)
        instruction = FloatLayout()
        instruction_label = Label(text=self.description,
                                  color = (0,0,0,1),
                                  size_hint=(1, .2),
                                  pos_hint={"top": .95, "right": 1})
        instruction_image = Image(source=self.source + self.image,
                                  size_hint=(1, 0.5),
                                  pos_hint={"top": .70, "right": 1})
        instruction.add_widget(instruction_image)
        instruction.add_widget(instruction_label)
        self.add_widget(instruction)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        
