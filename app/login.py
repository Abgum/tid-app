import kivy
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.app import MDApp
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.label import MDLabel

# LoginScreen sınıfı


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        self.username = MDTextField(
            hint_text="Kullanıcı Adı",
            size_hint=(0.8, 0.1),
            pos_hint={"center_x": 0.5, "center_y": 0.7},
        )

        self.password = MDTextField(
            hint_text="Şifre",
            size_hint=(0.8, 0.1),
            pos_hint={"center_x": 0.5, "center_y": 0.6},
            password=True,
        )

        self.login_button = MDRectangleFlatButton(
            text="Giriş",
            size_hint=(0.8, 0.1),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            md_bg_color=(79 / 255, 79 / 255, 79 / 255, 1),  # Background color
            text_color=(1, 1, 1, 1),  # Text color
            on_release=self.check_credentials,  # Butona tıklama olayı
        )

        self.add_widget(self.username)
        self.add_widget(self.password)
        self.add_widget(self.login_button)

    def check_credentials(self, instance):
        # Kullanıcı adı ve şifreyi al
        username_input = self.username.text
        password_input = self.password.text

        # Kullanıcı adı ve şifreyi kontrol et
        if username_input == "root" and password_input == "1234":
            # Ekran geçişi yap
            self.manager.current = "book_catalog_screen"
        else:
            MDSnackbar(text="Başarısız giriş").open()  # Hatalı giriş mesajı


# Kitap Kataloğu Ekranı
class BookCatalogScreen(Screen):
    def __init__(self, **kwargs):
        super(BookCatalogScreen, self).__init__(**kwargs)
        # Kitap Kataloğu ekranını burada ekleyebilirsiniz.
        # Örneğin, bir başlık eklemek için:
        self.add_widget(MDLabel(
            text="Kitap Kataloğu",
            halign="center",
            pos_hint={"center_y": 0.5, "center_x": 0.5}
        ))

# Ana Uygulama


class MyApp(MDApp):
    def build(self):
        # ScreenManager ile ekranlar arası geçiş
        sm = ScreenManager()

        sm.add_widget(LoginScreen(name="login_screen"))
        sm.add_widget(BookCatalogScreen(name="book_catalog_screen"))

        return sm


if __name__ == "__main__":
    MyApp().run()
