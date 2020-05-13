from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.core.image import Image

Builder.load_string("""
<ExampleApp>:
    orientation: "vertical"
    FloatLayout:
        MDLabel:
            pos_hint: {"center_x": .5, "center_y": .9}
            text: "Influence of anim_delay parameter on Gif speed."
            halign: "center"
            font_style: "H6"
    Image:
        source: "loading_bar.gif"
        anim_delay: year_slider.value
        allow_stretch: False
        anim_loop: 0

    FloatLayout:
        MDSlider:
            pos_hint: {"center_x": .5, "center_y": .4}
            id: year_slider
            hint: True
            min: 0
            max: 1
            value: 0
        MDLabel:
            pos_hint: {"center_x": .5, "center_y": .3}
            text: "Value of anim_delay: {}".format(round(year_slider.value,3))
            theme_text_color: "Primary"
            halign: "center"
        
        
""")

class ExampleApp(MDApp, BoxLayout):
    def build(self):
        return self

if __name__ == "__main__":
    ExampleApp().run()
    
    
    


#from kivy.clock import Clock
#from kivy.lang import Builder
#
#from kivymd.app import MDApp
#from kivymd.uix.menu import MDDropdownMenu
#
#KV = '''
#Screen
#
#    MDTextField:
#        id: field
#        pos_hint: {'center_x': .5, 'center_y': .5}
#        size_hint_x: None
#        width: "200dp"
#        hint_text: "Password"
#        on_focus: if self.focus: app.menu.open()
#'''
#
#
#class Test(MDApp):
#    def set_item(self, instance):
#        def set_item(interval):
#            self.screen.ids.field.text = instance.text
#
#        Clock.schedule_once(set_item, 0.5)
#
#    def build(self):
#        self.screen = Builder.load_string(KV)
#        menu_items = [{"icon": "git", "text": f"Item {i}"} for i in range(5)]
#        self.menu = MDDropdownMenu(
#            caller=self.screen.ids.field,
#            items=menu_items,
#            position="bottom",
#            callback=self.set_item,
#            width_mult=4,)
#        return self.screen
#
#
#Test().run()
# FloatLayout:
#                GridLayout:
#                    cols: 1
#                    pos_hint: {"top": 0.3, "left": 1}
#                    size_hint: .1, .1
#                    canvas:
#                        Color:
#                            rgb: utils.get_color_from_hex("#FFFFFF")
#                        Rectangle:
#                            source: 'temp.png'
#                            size: self.size
#                            pos: self.pos
#            BoxLayout:
#                MDLabel:
#                    text: "  Storein"
#                    halign: "center"
#                    font_style: "H6"
#            FloatLayout:
#                GridLayout:
#                    cols: 1
#                    pos_hint: {"top": 0.3, "left": 1}
#                    size_hint: .1, .1
#                    canvas:
#                        Color:
#                            rgb: utils.get_color_from_hex("#FFFFFF")
#                        Rectangle:
#                            source: 'temp.png'
#                            size: self.size
#                            pos: self.pos