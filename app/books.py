import requests
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import ScrollView
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.imagelist import MDSmartTile
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.textfield import MDTextField
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.navigationdrawer import MDNavigationDrawerMenu
from kivymd.icon_definitions import md_icons
from kivymd.uix.list import OneLineIconListItem


# Sunucu URL'si
server_url = "http://127.0.0.1:2020/"

# Kitapları almak için fonksiyon


def get_books():
    response = requests.get(server_url + "v1.0/books/get_all_books")
    if response.status_code == 200:
        return response.json()  # JSON formatında kitap verilerini döndürür
    return []

# Kitap içeriğini almak için fonksiyon


def get_book_content_by_id(book_id):
    response = requests.get(server_url + "v1.0/book_contents/" + str(book_id))
    if response.status_code == 200:
        return response.json()  # JSON formatında içerik verisini döndürür
    return {}


KV = '''
BoxLayout:
    orientation: 'vertical'

    MDTopAppBar:
        id: top_app_bar
        title: "Kitap Kataloğu"
        md_bg_color: app.theme_cls.primary_color
        specific_text_color: 1, 1, 1, 1
        elevation: 10

    MDNavigationLayout:
        ScreenManager:
            id: screen_manager
            on_current: app.update_toolbar_buttons(self.current)

            # Login Screen
            Screen:
                name: 'login'
                BoxLayout:
                    orientation: 'vertical'
                    padding: "30dp"
                    spacing: "20dp"

                    MDLabel:
                        text: "Giriş Yap"
                        halign: "center"
                        theme_text_color: "Secondary"

                    MDTextField:
                        id: username
                        hint_text: "Kullanıcı Adı"
                        size_hint_y: None
                        height: "40dp"
                        pos_hint: {"center_x": 0.5}

                    MDTextField:
                        id: password
                        hint_text: "Şifre"
                        size_hint_y: None
                        height: "40dp"
                        password: True
                        pos_hint: {"center_x": 0.5}

                    MDRaisedButton:
                        text: "Giriş Yap"
                        size_hint_y: None
                        height: "50dp"
                        pos_hint: {"center_x": 0.5}
                        on_release: app.login()

                    MDRaisedButton:
                        text: "Kayıt Ol"
                        size_hint_y: None
                        height: "50dp"
                        pos_hint: {"center_x": 0.5}
                        on_release: app.go_to_register()

                    MDRaisedButton:
                        text: "Şifremi Unuttum"
                        size_hint_y: None
                        height: "50dp"
                        pos_hint: {"center_x": 0.5}
                        on_release: app.go_to_forgot_password()

            # Register Screen
            Screen:
                name: 'register'
                BoxLayout:
                    orientation: 'vertical'
                    padding: "30dp"
                    spacing: "20dp"

                    MDLabel:
                        text: "Kayıt Ol"
                        halign: "center"
                        theme_text_color: "Secondary"

                    MDTextField:
                        id: register_username
                        hint_text: "Kullanıcı Adı"
                        size_hint_y: None
                        height: "40dp"
                        pos_hint: {"center_x": 0.5}

                    MDTextField:
                        id: register_password
                        hint_text: "Şifre"
                        size_hint_y: None
                        height: "40dp"
                        password: True
                        pos_hint: {"center_x": 0.5}

                    MDTextField:
                        id: register_email
                        hint_text: "E-posta"
                        size_hint_y: None
                        height: "40dp"
                        pos_hint: {"center_x": 0.5}

                    MDRaisedButton:
                        text: "Kayıt Ol"
                        size_hint_y: None
                        height: "50dp"
                        pos_hint: {"center_x": 0.5}
                        on_release: app.register()

                    MDRaisedButton:
                        text: "Geri Gel"
                        size_hint_y: None
                        height: "50dp"
                        pos_hint: {"center_x": 0.5}
                        on_release: app.go_to_login()

            # Forgot Password Screen
            Screen:
                name: 'forgot_password'
                BoxLayout:
                    orientation: 'vertical'
                    padding: "30dp"
                    spacing: "20dp"

                    MDLabel:
                        text: "Şifremi Unuttum"
                        halign: "center"
                        theme_text_color: "Secondary"

                    MDTextField:
                        id: email
                        hint_text: "E-posta"
                        size_hint_y: None
                        height: "40dp"
                        pos_hint: {"center_x": 0.5}

                    MDRaisedButton:
                        text: "Şifreyi Sıfırla"
                        size_hint_y: None
                        height: "50dp"
                        pos_hint: {"center_x": 0.5}
                        on_release: app.reset_password()

                    MDRaisedButton:
                        text: "Geri Dön"
                        size_hint_y: None
                        height: "50dp"
                        pos_hint: {"center_x": 0.5}
                        on_release: app.go_to_login()

            # Books Screen
            Screen:
                id: books_screen

                name: 'books'

                BoxLayout:
                    orientation: 'vertical'

                    MDTopAppBar:
                        title: "Kitap Kataloğu"
                        md_bg_color: app.theme_cls.primary_color
                        specific_text_color: 1, 1, 1, 1
                        elevation: 10
                        left_action_items: [["menu", lambda x: app.open_nav_drawer()]]

                    ScrollView:
                        MDGridLayout:
                            cols: 2
                            spacing: "16dp"
                            padding: "20dp"
                            size_hint_y: None
                            height: self.minimum_height

                            MDCard:
                                size_hint: None, None
                                size: "120dp", "120dp"
                                BoxLayout:
                                    orientation: "vertical"
                                    MDLabel:
                                        text: "Kitap 1"
                                    MDRaisedButton:
                                        text: "Oku"

       

        MDNavigationDrawer:
            id: nav_drawer
            radius: 0, dp(16), dp(16), 0
            MDNavigationDrawerMenu:
                MDNavigationDrawerHeader:
                    text: "Profil sayfasına hoşgeldiniz"
                    padding: "20dp"
                MDNavigationDrawerLabel:
                    text: "Kullancı Adı"
                MDNavigationDrawerLabel:
                    text: "Kullancı Mail"
                MDNavigationDrawerItem:
                    text: "Favoriler"
                    icon: "heart"
                MDNavigationDrawerItem:
                    text: "Çıkış Yap"
                    icon: "exit-to-app"
                    on_release: app.logout(), app.close_nav_drawer()                                      
       
'''


class BookCatalogApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def update_toolbar_buttons(self, screen_name):
        top_app_bar = self.root.ids.top_app_bar
        if screen_name == 'books':
            top_app_bar.left_action_items = [
                ["menu", lambda x: self.open_nav_drawer()]]
        else:
            top_app_bar.left_action_items = []

    def open_nav_drawer(self):
        print("Nav Drawer açılmaya çalışılıyor...")
        try:
            deneme = self.root.ids.nav_drawer

            print(f"Books Screen: {deneme}")

            nav_drawer = self.root.ids.nav_drawer
            nav_drawer.set_state("open")
            print("Nav Drawer başarıyla açıldı.")
        except Exception as e:
            print(f"Nav Drawer açılırken bir hata oluştu: {e}")

    def close_nav_drawer(self):
        print("Nav Drawer kapatıldı")
        nav_drawer = self.root.ids.nav_drawer
        nav_drawer.set_state("close")

    def toggle_profile_menu(self):
        profile_menu = self.root.ids.profile_menu
        if profile_menu.height == 0:
            # Show profile menu (open it)
            profile_menu.height = "200dp"
        else:
            # Hide profile menu (close it)
            profile_menu.height = "0dp"

    # Toggle Menü Fonksiyonu
    def toggle_menu(self):
        nav_drawer = self.root.ids.nav_drawer
        if nav_drawer.state == "open":
            nav_drawer.set_state("close")
        else:
            nav_drawer.set_state("open")

    def logout(self):
        print("Çıkış yapıldı")
        self.root.ids.screen_manager.current = "login"  # Return to login screen

    def login(self):
        username = self.root.ids.username.text
        password = self.root.ids.password.text

        # Kullanıcı adı ve şifre kontrolü
        if username == "root" and password == "1234":
            # Kullanıcı adı ve şifre doğruysa, kitaplar sayfasına geçiş yap
            self.root.ids.screen_manager.current = "books"
            # Kitapları yükle
            self.load_books()
            return

        # Sunucuya giriş bilgilerini gönder
        login_url = server_url + "v1.0/auth/login"
        data = {
            "username": username,
            "password": password
        }
        response = requests.post(login_url, json=data)

        if response.status_code == 200:
            # Giriş başarılıysa kitap sayfasına geçiş yap
            self.root.ids.screen_manager.current = "books"
            # Kitapları yükle
            self.load_books()
        else:
            # Hata mesajı göster
            print("Giriş başarısız!")

    def load_books(self):
        books = get_books()
        book_cards = ""

        for book in books:
            # Her kitap için bir MDCard ekle
            book_id = book.get("book_id", 0)
            title = book.get("book_title", "Başlık Bilgisi Yok")
            image_url = book.get("cover_path")
            deneme = server_url + image_url

            book_cards += '''
MDCard:
    size_hint: None, None
    size: "180dp", "300dp"
    elevation: 5
    radius: [12,]
    orientation: "vertical"
    padding: "8dp"
    # Burada kartın sola hizalanmasını sağlıyoruz
    pos_hint: {"top": 1, "left": 0.1}  # Kartları sola hizalayın

    MDSmartTile:
        radius: 12
        box_radius: [0, 0, 12, 12]
        box_color: 1, 1, 1, .2
        source: "%s"
        size_hint: None, None
        size: "180dp", "240dp"
        pos_hint: {"center_x": .5}
        overlap: False
        lines: 2
        text: "%s"
        on_release: app.read_book( % d)  # Resme tıklama ile kitabı oku fonksiyonu

    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        height: "50dp"
        padding: "5dp"
        spacing: "10dp"

        MDIconButton:
            icon: "heart"
            on_release: app.add_to_favorites( % d)  # Favorilere ekle
            size_hint: None, None
            size: "40dp", "40dp"

        MDIconButton:
            icon: "bookmark-plus"
            on_release: app.add_to_read_later( % d)  # Okunacaklara ekle
            size_hint: None, None
            size: "40dp", "40dp"
''' % (deneme, title, book_id, book_id, book_id)
    # Kitap kartlarını dinamik olarak yükle
        self.root.ids.books_screen.clear_widgets()
        self.root.ids.books_screen.add_widget(Builder.load_string(book_cards))

    def read_book(self, book_id):
        book_content = get_book_content_by_id(book_id)
        print(f"Kitap İçeriği: {book_content}")

    def add_to_favorites(self, book_id):
        print(f"Kitap {book_id} favorilere eklendi!")

    def add_to_read_later(self, book_id):
        print(f"Kitap {book_id} okunacaklara eklendi!")

    def go_to_register(self):
        self.root.ids.screen_manager.current = "register"

    def go_to_forgot_password(self):
        self.root.ids.screen_manager.current = "forgot_password"

    def reset_password(self):
        # E-posta adresini al
        email = self.root.ids.email.text

        # Sunucuya e-posta adresi gönder
        reset_url = server_url + "v1.0/auth/reset_password"
        data = {"email": email}
        response = requests.post(reset_url, json=data)

        if response.status_code == 200:
            # Şifre sıfırlama başarılı
            print("Şifreniz sıfırlama talimatı gönderildi.")
            self.root.ids.screen_manager.current = "login"
        else:
            # Şifre sıfırlama başarısız
            print("Şifre sıfırlama başarısız!")

    def register(self):
        # Kayıt işlemi için veriyi al
        username = self.root.ids.register_username.text
        password = self.root.ids.register_password.text
        email = self.root.ids.register_email.text

        # Sunucuya kayıt bilgilerini gönder
        register_url = server_url + "v1.0/auth/register"
        data = {
            "username": username,
            "password": password,
            "email": email
        }
        response = requests.post(register_url, json=data)

        if response.status_code == 200:
            # Kayıt başarılıysa, login ekranına geri dön
            self.root.ids.screen_manager.current = "login"
        else:
            # Kayıt başarısızsa hata mesajı
            print("Kayıt başarısız!")

    def go_to_login(self):
        self.root.ids.screen_manager.current = "login"

    def on_start(self):
        self.set_theme()

    def set_theme(self):
        if self.theme_cls.theme_style == "Light":
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"

        if self.theme_cls.primary_palette == "Orange":
            self.theme_cls.primary_palette = "Green"
        else:
            self.theme_cls.primary_palette = "Orange"


BookCatalogApp().run()
