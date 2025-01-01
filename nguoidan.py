from kivy.app import App
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class MyApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        # Danh sách chứa các checkbox
        self.checkboxes = []
        self.checkbox_vars = []

        # Tạo 12 checkbox (bạn có thể thay đổi số lượng tùy ý)
        for i in range(12):  # Thử với 12 checkbox
            var = CheckBox(active=False)
            self.checkboxes.append(var)
            self.checkbox_vars.append(var)
            self.layout.add_widget(var)

        # Nút "Select All"
        select_all_button = Button(text="Select All")
        select_all_button.bind(on_press=self.toggle_select_all)
        self.layout.add_widget(select_all_button)

        # Label để hiển thị số lượng checkbox được chọn
        self.label = Label(text="Số lượng checkbox được chọn: 0")
        self.layout.add_widget(self.label)

        return self.layout

    def toggle_select_all(self, instance):
        # Kiểm tra nếu có hơn 10 checkbox
        if len(self.checkboxes) > 10:
            # Kiểm tra xem có tất cả checkbox đang được chọn không
            select_all = all(var.active for var in self.checkbox_vars)
            # Đảo trạng thái của tất cả checkbox
            for var in self.checkbox_vars:
                var.active = not select_all
            self.update_label()

    def update_label(self):
        # Cập nhật số lượng checkbox được chọn
        selected_count = sum(1 for var in self.checkbox_vars if var.active)
        self.label.text = f"Số lượng checkbox được chọn: {selected_count}"


if __name__ == "__main__":
    MyApp().run()
