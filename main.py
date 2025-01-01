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
import tkinter

from kivy.uix.checkbox import CheckBox

from client import Client


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
    dialog = None
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_tables = None
        global contacts
        contacts = []
    def build(self):
        #Các màu chủ đề: ‘Red’, ‘Pink’, ‘Purple’, ‘DeepPurple’,
        # ‘Indigo’, ‘Blue’, ‘LightBlue’, ‘Cyan’, ‘Teal’, ‘Green’,
        # ‘LightGreen’, ‘Lime’, ‘Yellow’, ‘Amber’, ‘Orange’,
        # ‘DeepOrange’, ‘Brown’, ‘Gray’, ‘BlueGray’
        self.theme_cls.primary_palette = "Teal"
        #self.theme_cls.theme_style = "Dark"
        global sc
        sc = ScreenManager()
        sc.add_widget(Builder.load_file('Login.kv'))
        sc.add_widget(Builder.load_file('Menu.kv'))
        sc.add_widget(Builder.load_file('Profile.kv'))
        sc.add_widget(Builder.load_file('Upload.kv'))
        sc.add_widget(Builder.load_file('Appinfor.kv'))
        sc.add_widget(Builder.load_file('main.kv'))
        sc.add_widget(Builder.load_file('update.kv'))
        sc.add_widget(Builder.load_file('add.kv'))
        sc.add_widget(Builder.load_file('CreateAcc.kv'))
        sc.add_widget(Builder.load_file('timkiem.kv'))
        sc.add_widget(Builder.load_file('thongbao.kv'))
        return sc
    def go_to_add_datatable(self):
        sc.current = 'page'
        self.add_datatable()

    def add_datatable(self):
        import sqlite3
        vt = sqlite3.connect('Dancuxa.db')
        im = vt.cursor()
        im.execute("select * from person")
        data=im.fetchall()
        self.data_tables = MDDataTable(
            size_hint=(0.9, 0.6),
            use_pagination=True,
            check=True,
            column_data=[
                ("ID", dp(30)),
                ("Căn cước", dp(50)),
                ("Tên", dp(30)),
                ("Tuổi", dp(30)),
                ("Địa chỉ", dp(40)),
                ("Số điện thoại", dp(40)),
                ("Email", dp(40))
            ],
            row_data=[
                (
                i[:][0],
                i[:][1],
                i[:][2],
                i[:][3],
                i[:][4],
                i[:][5],
                i[:][6],

                )
                for i in data
            ],
        )
        self.data_tables.bind(on_check_press=self.on_check_press)
        sc.get_screen("page").ids.datatable.add_widget(self.data_tables)
    def on_start(self):
        pass
    def search(self,obj):
        if obj == '':
            pass
        else:
            self.search_datatable(obj)
            sc.current = "kiem"
    def search_datatable(self,obj):
        try:
            import sqlite3
            vt = sqlite3.connect('Dancuxa.db')
            im = vt.cursor()
            im.execute(f"select * from person where cccd={obj} ")
            data=im.fetchall()
            self.second_data_tables = MDDataTable(
                size_hint=(0.9, 0.5),
                use_pagination=True,
                check=True,
                column_data=[
                    ("ID", dp(30)),
                    ("Căn cước", dp(50)),
                    ("Tên", dp(30)),
                    ("Tuổi", dp(30)),
                    ("Địa chỉ", dp(40)),
                    ("Số điện thoại", dp(40)),
                    ("Email", dp(40))
                ],
                row_data=[
                    (
                    i[:][0],
                    i[:][1],
                    i[:][2],
                    i[:][3],
                    i[:][4],
                    i[:][5],
                    i[:][6],

                    )
                    for i in data
                ],
            )
            self.second_data_tables.bind(on_check_press=self.on_check_press)
            sc.get_screen("kiem").ids.datatable.add_widget(self.second_data_tables)
        except:
            self.show_dialog("Lỗi", "Có CCCD không hợp lệ.")

    def go_to_thongbao_datatable(self):
        sc.current = 'thong_bao'
        self.thongbao_datatable()
    def thongbao_datatable(self):
        import sqlite3
        vt = sqlite3.connect('Dancuxa.db')
        im = vt.cursor()
        im.execute("SELECT person_id,cccd,username FROM person")
        data=im.fetchall()
        print(data)
        self.data_tables = MDDataTable(
            size_hint=(0.48, 0.6),
            use_pagination=True,
            #rows_num=6,
            check=True,
            column_data=[
                ("ID", dp(30)),
                ("Căn cước", dp(50)),
                ("Tên", dp(30)),
            ],
            row_data=[
                (i[0], i[1], i[2]) for i in data if i is not None
            ],
        )
        self.data_tables.bind(on_check_press=self.on_check_press)
        datatable_id = sc.get_screen("thong_bao").ids.datatable
        datatable_id.clear_widgets()
        datatable_id.add_widget(self.data_tables)
    def clear_contacts_after_search(self):
        contacts.clear()

    def on_check_press(self, instance_stable, current_row):
        # Đảm bảo current_row không phải None
        if current_row[0] not in contacts:
            contacts.append(current_row[0])
        else:
            contacts.remove(current_row[0])
        print(contacts)


    def clear_ckeck_press_add_datatable(self):
        sc.get_screen("page").ids.datatable.remove_widget(self.data_tables)
    def clear_ckeck_press_thongbao_datatable(self):
        sc.get_screen("thong_bao").ids.datatable.remove_widget(self.data_tables)



    def delete(self):
        self.dialog = MDDialog(
            text = "Bạn xóa toàn bộ thông tin của tài khoản",
            buttons=[
                MDFlatButton(text = "đóng", on_release = self.close),
                MDRectangleFlatButton(text = "xóa", on_release = self.open)
            ],
        )
        self.dialog.open()

    def close(self,obj):
        self.dialog.dismiss()
        contacts.clear()
        sc.current = "page"
    def open(self,obj):
        for i in contacts:
            if i:
                import sqlite3
                vt = sqlite3.connect("Dancuxa.db")
                im = vt.cursor()
                im.execute(f"delete from person where person_id = {i}")
                vt.commit()
                sc.get_screen("page").ids.datatable.remove_widget(self.data_tables)
                self.add_datatable()
        self.dialog.dismiss()
        contacts.clear()

    def updatenewpage(self):
        for i in contacts:
            if i:
                import sqlite3
                vt=sqlite3.connect("Dancuxa.db")
                im=vt.cursor()
                im.execute(f"select * from person where person_id={i}")
                data=im.fetchall()
                for j in data:
                    sc.get_screen("upd").ids.cccd.text=j[1]
                    sc.get_screen("upd").ids.name.text=j[2]
                    sc.get_screen("upd").ids.age.text=j[3]
                    sc.get_screen("upd").ids.city.text=j[4]
                    sc.get_screen("upd").ids.sdt.text=j[5]
                    sc.get_screen("upd").ids.mk.text=j[6]

        sc.current = "upd"

    def addnewpage(self):
        sc.current = "add"
    def back(self, instance):
        sc.current = "page"
    def update(self,cccd,username,age,city,sdt,mk):
        for i in contacts:
            if i:
                import sqlite3
                vt = sqlite3.connect("Dancuxa.db")
                im = vt.cursor()
                im.execute("update person set cccd=?, username=?, age=?, city=?, sdt=?, mk=? where person_id=?",(cccd,username,age,city,sdt,mk,i))
                vt.commit()
                sc.get_screen("page").ids.datatable.remove_widget(self.data_tables)
                self.add_datatable()
        contacts.clear()
        sc.current = "page"
    def add(self,cccd,username,age,city,sdt,mk):
        import sqlite3
        vt = sqlite3.connect("Dancuxa.db")
        im = vt.cursor()
        im.execute("insert into person(cccd,username,age,city,sdt,mk) VALUES(?,?,?,?,?,?)",(cccd,username,age,city,sdt,mk))
        vt.commit()
        sc.get_screen("page").ids.datatable.remove_widget(self.data_tables)
        self.add_datatable()
        contacts.clear()
        sc.current = "page"



    def gmail(self,subject,body):
        import ssl
        import smtplib
        import sqlite3
        email_sender = "nguyenvanhai310805@gmail.com"
        email_pass = "zwgu qdul dljv gmwj"
        # email_receiver = "biennn97@gmail.com"
        #subject = self.root.get_screen('thong_bao').ids.subject.text
        #body = self.root.get_screen('thong_bao').ids.body.text
        try:
            print(contacts)
            for i in contacts:
                if i:
                    vt = sqlite3.connect('Dancuxa.db')
                    im = vt.cursor()
                    im.execute(f"select mk from person where person_id={i}")
                    data = im.fetchall()
                    for j in data:
                        print(j)
                        email_receiver = j
                        em = EmailMessage()
                        em['From'] = email_sender
                        em['To'] = email_receiver
                        em['Subject'] = subject
                        em.set_content(body)
                        context = ssl.create_default_context()
                        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                            smtp.login(email_sender, email_pass)
                            smtp.sendmail(email_sender, email_receiver, em.as_string())
        except:
            self.show_dialog("Lỗi", "Có Email không hợp lệ.")


    def register_user(self):
        # Lấy giá trị từ các trường nhập liệu
        username = self.root.get_screen('tao_tai_khoan').ids.new_user.text
        password = self.root.get_screen('tao_tai_khoan').ids.new_password.text
        password_confirm = self.root.get_screen('tao_tai_khoan').ids.password_confirm.text

        # Kiểm tra các trường thông tin
        if not username or not password or not password_confirm:
            self.show_dialog("Lỗi", "Vui lòng điền đầy đủ thông tin.")
            return

        if password != password_confirm:
            self.show_dialog("Lỗi", "Mật khẩu và xác nhận mật khẩu không khớp.")
            return

        # Thêm tài khoản vào cơ sở dữ liệu
        import sqlite3
        conn = sqlite3.connect("Canbo.db")
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO manageraccount (username, mk) VALUES (?, ?)
            """, (username, password))
            conn.commit()
            self.show_dialog("Thành công", "Tài khoản đã được tạo.")
            self.root.current = 'man_hinh_dang_nhap'
        except sqlite3.IntegrityError:
            self.show_dialog("Lỗi", "Tên tài khoản đã tồn tại.")
        finally:
            conn.close()

    def login_user(self):
        # Lấy dữ liệu từ các trường nhập liệu
        username = self.root.get_screen('man_hinh_dang_nhap').ids.user.text
        password = self.root.get_screen('man_hinh_dang_nhap').ids.password.text

        # Kiểm tra các trường thông tin
        if not username or not password:
            self.show_dialog("Lỗi", "Vui lòng điền đầy đủ thông tin.")
            return

        # Kiểm tra trong cơ sở dữ liệu
        import sqlite3
        conn = sqlite3.connect("Canbo.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM manageraccount WHERE username = ? AND mk = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            self.show_dialog("Thành công", f"Xin chào {username}!")
            self.root.current = "giao_dien_chinh"
        else:
            self.show_dialog("Lỗi", "Tên tài khoản hoặc mật khẩu không đúng, vui lòng đăng nhập lại!")

    def clearLogin(self):
        self.root.get_screen('man_hinh_dang_nhap').ids.quan_li.text = "QUẢN LÍ NHÂN KHẨU"
        self.root.get_screen('man_hinh_dang_nhap').ids.user.text = ""
        self.root.get_screen('man_hinh_dang_nhap').ids.password.text =""

    def clearRegister(self):
        self.root.get_screen('tao_tai_khoan').ids.new_user.text = ""
        self.root.get_screen('tao_tai_khoan').ids.new_password.text = ""
        self.root.get_screen('tao_tai_khoan').ids.password_confirm.text = ""

    def showdata(self, instance):
        if self.root.get_screen('man_hinh_dang_nhap').ids.user.text == "" or self.root.get_screen(
                'man_hinh_dang_nhap').ids.password.text == "":
            check_string = 'Vui lòng nhập tên tài khoản và mật khẩu'
        else:
            check_string = f"tên tài khoản: {self.root.get_screen('man_hinh_dang_nhap').ids.user.text} \nmật khẩu: {self.root.get_screen('man_hinh_dang_nhap').ids.password.text}"
        close_button = MDIconButton(icon='close', on_release=self.close_dialog)
        login_button = MDIconButton(icon='login', on_release=self.interface)
        self.dialog = MDDialog(
            title='Kiểm tra thông tin',
            text=check_string,

            buttons=[close_button, login_button]
        )
        self.dialog.open()
    def close_dialog(self, instance):
        # Đảm bảo nhận tham số instance
        self.dialog.dismiss()

    def interface(self, instance):
        self.dialog.dismiss()
        self.root.get_screen('man_hinh_dang_nhap').manager.current = 'giao_dien_chinh'

    def show_dialog(self, title, message):
        dialog = MDDialog(
            title=title,
            text=message,
            size_hint=(0.8, 0.8),
            buttons=[MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()
    def nhantin(self):
        try:
            import subprocess
            from client import Client
            # Lệnh CMD bạn muốn thực thi
            a = 'CánBộ'
            command = f'python client.py 127.0.0.1 -n {a}'


            # Thực thi lệnh CMD
            subprocess.run(command, shell=True)
            sc.current = 'giao_dien_chinh'

        except:
            sc.current = 'giao_dien_chinh'








if __name__ == '__main__':
    Quan_liApp().run()
