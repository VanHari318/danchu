from docutils.nodes import contact
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable


class userLoginScreen(Screen):
    pass
class userRegisterScreen(Screen):
    pass

class Nguoi_dan(MDApp):
    dialog = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_tables = None
        global contacts
        contacts = []

    def build(self):
        # Các màu chủ đề: ‘Red’, ‘Pink’, ‘Purple’, ‘DeepPurple’,
        # ‘Indigo’, ‘Blue’, ‘LightBlue’, ‘Cyan’, ‘Teal’, ‘Green’,
        # ‘LightGreen’, ‘Lime’, ‘Yellow’, ‘Amber’, ‘Orange’,
        # ‘DeepOrange’, ‘Brown’, ‘Gray’, ‘BlueGray’
        self.theme_cls.primary_palette = "Teal"
        # self.theme_cls.theme_style = "Dark"
        global sc
        sc = ScreenManager()
        sc.add_widget(Builder.load_file('userLogin.kv'))
        sc.add_widget(Builder.load_file('userRegister.kv'))
        sc.add_widget(Builder.load_file('Danchu.kv'))
        sc.add_widget(Builder.load_file('nguoidan.kv'))
        sc.add_widget(Builder.load_file('thong_tin_tai_khoan.kv'))
        return sc

    def infor_user(self):
        # Lấy giá trị từ các trường nhập liệu
        username = self.root.get_screen('tao_tai_khoan_nguoi_dung').ids.username.text.strip()
        age = self.root.get_screen('tao_tai_khoan_nguoi_dung').ids.age.text.strip()
        city = self.root.get_screen('tao_tai_khoan_nguoi_dung').ids.city.text.strip()
        cccd = self.root.get_screen('tao_tai_khoan_nguoi_dung').ids.cccd.text.strip()
        sdt = self.root.get_screen('tao_tai_khoan_nguoi_dung').ids.sdt.text.strip()
        mk = self.root.get_screen('tao_tai_khoan_nguoi_dung').ids.mk.text.strip()

        # Kiểm tra các trường thông tin
        if not username or not age or not city or not cccd or not sdt or not mk:
            self.show_dialog("Lỗi", "Vui lòng điền đầy đủ thông tin.")
            return

        # Kiểm tra độ tuổi có phải là số hay không
        if not age.isdigit() or int(age) <= 0 or int(age) >= 150:
            self.show_dialog("Lỗi", "Độ tuổi không hợp lệ.")
            return

        # Kiểm tra định dạng số điện thoại
        if not sdt.isdigit() or len(sdt) != 10:
            self.show_dialog("Lỗi", "Số điện thoại không hợp lệ.")
            return

        # Kiểm tra định dạng số CCCD
        if not cccd.isdigit() or len(cccd) != 12:
            self.show_dialog("Lỗi", "Số CCCD không hợp lệ.")
            return

        # Kiểm tra định dạng email
        import re
        email_pattern = r"^[a-zA-Z0-9._%+-]+@gmail\.com$"
        if not re.match(email_pattern, mk):
            self.show_dialog("Lỗi", "Địa chỉ email không hợp lệ. Vui lòng nhập email dạng @gmail.com.")
            return

        # Kết nối cơ sở dữ liệu và kiểm tra trùng lặp
        import sqlite3
        conn = sqlite3.connect("Dancuxa.db")
        cursor = conn.cursor()
        try:
            # Kiểm tra nếu tất cả các trường dữ liệu đã tồn tại
            cursor.execute("""
                SELECT 1 FROM person 
                WHERE cccd = ? AND username = ? AND age = ? AND city = ? AND sdt = ? AND mk = ?
            """, (cccd, username, age, city, sdt, mk))

            if cursor.fetchone():
                self.show_dialog("Lỗi", "Tài khoản với thông tin này đã tồn tại.")
                return

            # Thực hiện chèn dữ liệu nếu không trùng lặp
            cursor.execute("""
                INSERT INTO person (cccd, username, age, city, sdt, mk) VALUES (?, ?, ?, ?, ?, ?)
            """, (cccd, username, age, city, sdt, mk))
            conn.commit()

            self.show_dialog("Thành công", "Thông tin đã được ghi nhận.")
            self.root.current = 'man_hinh_dang_nhap_nguoi_dung'


        except sqlite3.IntegrityError:
            self.show_dialog("Lỗi", "Tên tài khoản đã tồn tại.")

        finally:
            conn.close()
    def capnhat(self, user):
        if user:
            self.root.get_screen('thong_tin_tai_khoan_k').ids.cccd.secondary_text = str(user[1])
            self.root.get_screen('thong_tin_tai_khoan_k').ids.ten.secondary_text = str(user[2])
            self.root.get_screen('thong_tin_tai_khoan_k').ids.tuoi.secondary_text = str(user[3])
            self.root.get_screen('thong_tin_tai_khoan_k').ids.dia_chi.secondary_text = str(user[4])
            self.root.get_screen('thong_tin_tai_khoan_k').ids.sdt.secondary_text = str(user[5])
            self.root.get_screen('thong_tin_tai_khoan_k').ids.email.secondary_text = str(user[6])
    def login_user(self):
        # Lấy dữ liệu từ các trường nhập liệu
        username = self.root.get_screen('man_hinh_dang_nhap_nguoi_dung').ids.username.text
        cccd = self.root.get_screen('man_hinh_dang_nhap_nguoi_dung').ids.cccd.text

        # Kiểm tra các trường thông tin
        if not username or not cccd:
            self.show_dialog("Lỗi", "Vui lòng điền đầy đủ thông tin.")
            return

        # Kiểm tra trong cơ sở dữ liệu
        import sqlite3
        conn = sqlite3.connect("Dancuxa.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM person WHERE username = ? AND cccd = ?", (username, cccd))
        user = cursor.fetchone()
        self.capnhat(user)
        print(user)
        conn.close()

        if user:
            self.show_dialog("Thành công", f"Xin chào {username}!")
            self.root.current = "giao_dien_chinh"
            self.add_datatable()
        else:
            self.show_dialog("Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng, vui lòng đăng nhập lại!")

    def clearLogin(self):
        self.root.get_screen('man_hinh_dang_nhap_nguoi_dung').ids.quan_li.text = "QUẢN LÍ NHÂN KHẨU"
        self.root.get_screen('man_hinh_dang_nhap_nguoi_dung').ids.username.text = ""
        self.root.get_screen('man_hinh_dang_nhap_nguoi_dung').ids.cccd.text = ""

    def clearRegister(self):
        self.root.get_screen('tao_tai_khoan_nguoi_dung').ids.username.text = ""
        self.root.get_screen('tao_tai_khoan_nguoi_dung').ids.age.text = ""
        self.root.get_screen('tao_tai_khoan_nguoi_dung').ids.city.text = ""
        self.root.get_screen('tao_tai_khoan_nguoi_dung').ids.cccd.text = ""
        self.root.get_screen('tao_tai_khoan_nguoi_dung').ids.sdt.text = ""
        self.root.get_screen('tao_tai_khoan_nguoi_dung').ids.mk.text = ""



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
            a = 'Dân'
            command = f'python client.py 127.0.0.1 -n {a}'


            # Thực thi lệnh CMD
            subprocess.run(command, shell=True)
            sc.current = 'giao_dien_chinh'
        except:
            sc.current = 'giao_dien_chinh'
    def add_datatable(self):
        import sqlite3
        vt = sqlite3.connect('Dancuxa.db')
        im = vt.cursor()
        im.execute("select * from person")
        data=im.fetchall()
        self.data_tables = MDDataTable(
            size_hint=(0.9, 0.6),
            use_pagination=True,
            check=False,
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
    def on_start(self):
        pass

        #self.add_datatable(username, cccd)
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
                check=False,
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
        except:
            self.show_dialog("Lỗi", "Có CCCD không hợp lệ.")




if __name__ == '__main__':
    Nguoi_dan().run()
