from tkinter.tix import Select

from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
#from kivymd.uix.list import OneLineListItem, MDList, TwoLineListItem
from kivymd.uix.screen import MDScreen
#from kivymd.uix.label import MDLabel
from kivy.core.window import Window
from kivymd.uix.button import MDIconButton, MDTextButton
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.dialog import MDDialog
#from kivymd.uix.card import MDCard
from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable,ScrollView
from kivymd.uix.textfield import MDTextField
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from docutils.nodes import contact
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton
from kivymd.app import MDApp
from email.message import EmailMessage

from kivy.uix.checkbox import CheckBox



class LoginScreen(Screen):
    pass
class CreateAccScreen(Screen):
    pass
class MenuScreen(Screen):
    pass
class ProfileScreen(Screen):
    pass
class UploadScreen(Screen):
    pass
class HelpScreen(Screen):
    pass
class FindScreen(Screen):
    pass




class Quan_liApp(MDApp):
    def build(self):
        #Các màu chủ đề: ‘Red’, ‘Pink’, ‘Purple’, ‘DeepPurple’,
        # ‘Indigo’, ‘Blue’, ‘LightBlue’, ‘Cyan’, ‘Teal’, ‘Green’,
        # ‘LightGreen’, ‘Lime’, ‘Yellow’, ‘Amber’, ‘Orange’,
        # ‘DeepOrange’, ‘Brown’, ‘Gray’, ‘BlueGray’
        self.theme_cls.primary_palette = "Teal"
        #self.theme_cls.theme_style = "Dark"
        global sc
        sc = ScreenManager()
        ##sc.add_widget(Builder.load_file('Login.kv'))
        sc.add_widget(Builder.load_file('Danchu.kv'))
        return sc





    def interface(self, instance):
        sc.current = 'giao_dien_chinh'




if __name__ == '__main__':
    Quan_liApp().run()
