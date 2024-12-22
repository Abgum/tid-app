from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivy.uix.label import Label


class LoginScreen(BoxLayout):
    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = screen_manager
        self.orientation = "vertical"
        self.padding = "20dp"
        self.spacing = "10dp"

        # Kullanıcı adı ve şifre alanları
        self.username = MDTextField(
            hint_text="Kullanıcı Adı", size_hint_y=None, height="40dp")
        self.password = MDTextField(
            hint_text="Şifre", password=True, size_hint_y=None, height="40dp")

        self.add_widget(self.username)
        self.add_widget(self.password)

        # Giriş butonu
        self.login_button = MDRaisedButton(
            text="Giriş Yap", size_hint_y=None, height="50dp")
        self.login_button.bind(on_release=self.login)
        self.add_widget(self.login_button)

    def login(self, instance):
        # Giriş işlemi burada yapılacak
        username = self.username.text
        password = self.password.text

        print(f"Kullanıcı adı: {username}, Şifre: {password}")

        # Kullanıcı adı ve şifreyi kontrol et
        if username == "root" and password == "1234":
            print("Giriş başarılı")
            self.screen_manager.current = "books"  # Kitaplar ekranına geçiş
        else:
            print("Hatalı giriş")
            # Hata mesajı gösterebilirsiniz
