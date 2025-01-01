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

class Nhantin(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def build(self):
        global manag
        manag = ScreenManager()
        manag.add_widget(Builder.load_file('Appinfor.kv'))
        return manag
    def sendmess(self):
        manag.current = 'thong_tin_ung_dung'



Nhantin().run()
