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
from kivy.metrics import dp
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.utils import platform
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
import hashlib
from kivymd.uix.snackbar import MDSnackbar


if platform == 'android' or platform == 'ios':
    # Mobil cihazlar için tam ekran
    Window.fullscreen = True
else:
    # Masaüstü için belirli bir boyut
    Window.size = (360, 640)
# Sunucu URL'si
server_url = "http://127.0.0.1:2020/"

# Kitapları almak için fonksiyon


def hash_password(password):
    hashlib.sha512(password.encode("utf-8")).hexdigest(),


def get_books():
    response = requests.get(server_url + "api/books/get_all_books")
    if response.status_code == 200:
        return response.json()  # JSON formatında kitap verilerini döndürür
    return []

# Kitap içeriğini almak için fonksiyon


def show_popup(title, message):
    popup_content = BoxLayout(orientation='vertical', spacing=10, padding=10)
    popup_content.add_widget(Label(text=message))

    close_button = Button(text="Tamam", size_hint=(1, 0.3))
    popup_content.add_widget(close_button)

    popup = Popup(title=title,
                  content=popup_content,
                  size_hint=(0.8, 0.4),
                  auto_dismiss=False)

    close_button.bind(on_release=popup.dismiss)
    popup.open()

# Şifre ve kullanıcı adı kontrol fonksiyonu


def check_user_credentials(users, username, password):
    print(f"mail {username}, password {password}")
    for user in users:
        print(f"user {user}")
        if user.get('email') == username and user.get('password') == password:
            return True
    return False

# Şifreyi ya da kullanıcı adını almak için bir fonksiyon


def get_user_info(users, key, value, field):
    for user in users:
        if user.get(key) == value:
            return user.get(field)
    return None


def load_book_content(self, book_id):
    # Set the current book ID
    # Initialize current_book_id here if not done already
    self.current_book_id = book_id
    print

    # Load book content from the API
    book_content = get_book_content_by_id(book_id)
    if book_content:
        # Listenin ilk öğesini alıyoruz (örneğin, kitap içeriği)
        book_details = book_content[0]  # Liste ise ilk öğeye erişim
        title = book_details.get("book_title", "Başlık Bilgisi Yok")
        content = book_details.get("sentence", "İçerik bulunamadı.")
        self.root.ids.book_title.text = title
        self.root.ids.book_content.text = content


def get_book_content_by_id(book_id):
    response = requests.get(server_url + "api/book_contents/" + str(book_id))
    col2_grid = GridLayout(
        cols=2,
        spacing=dp(10),
        padding=[dp(10), dp(10)],  # Sol ve sağ padding
        size_hint_y=None  # Yüksekliği içeriğe göre ayarla
    )
    col2_grid.bind(minimum_height=col2_grid.setter(
        'height'))  # İçeriğe göre yüksekliği ayarla

    if response.status_code == 200:
        return response.json()  # JSON formatında içerik verisini döndürür
    return {}


KV = '''
BoxLayout:
    orientation: 'vertical'

    MDTopAppBar:
        id: top_app_bar
        title: "Sessizce Oku"
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
                    padding: "50dp"
                    spacing: "20dp"

                    MDLabel:
                        text: "Giriş Yap"
                        halign: "center"
                        theme_text_color: "Secondary"

                    MDTextField:
                        id: login_username
                        hint_text: "Email"
                        size_hint_y: None
                        height: "0dp"
                        pos_hint: {"center_x": 0.5}

                    MDTextField:
                        id: password
                        hint_text: "Şifre"
                        size_hint_y: None
                        height: "0dp"
                        password: True
                        pos_hint: {"center_x": 0.5}
                    BoxLayout:
                        orientation: "horizontal"
                        spacing: "10dp"
                        size_hint_y: None
                        height: "50dp"
                        size_hint_x: 1
                        pos_hint: {"center_x": 0.5}

                        MDRaisedButton:
                            text: "Giriş Yap"
                            size_hint_x: 1
                            on_release: app.login()

                        MDRaisedButton:
                            text: "Kayıt Ol"
                            size_hint_x: 1
                            on_release: app.go_to_register()

                    BoxLayout:
                        orientation: "horizontal"
                        size_hint_y: None
                        height: "50dp"
                        size_hint_x: 1
                        pos_hint: {"center_x": 0.5}

                        MDRaisedButton:
                            text: "Şifremi Unuttum"
                            size_hint_x: 1
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
                        hint_text: "Ceyda Gül"
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
                        hint_text: "ceyda@gsü.edu.tr"
                        size_hint_y: None
                        height: "40dp"
                        pos_hint: {"center_x": 0.5}

                    # Yeni BoxLayout ile butonları hizalayalım
                    BoxLayout:
                        orientation: "horizontal"
                        spacing: "10dp"
                        size_hint_y: None
                        height: "50dp"
                        size_hint_x: 1
                        pos_hint: {"center_x": 0.5}

                        MDRaisedButton:
                            text: "Kayıt Ol"
                            size_hint_x: 1
                            on_release: app.register()

                        MDRaisedButton:
                            text: "Giriş Yap"
                            size_hint_x: 1
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
                    MDTextField:
                        id: new_password
                        hint_text: "Yeni Şifre"
                        size_hint_y: None
                        height: "40dp"
                        password: True
                        pos_hint: {"center_x": 0.5}                    

                    # Yeni BoxLayout ile butonları hizalayalım
                    BoxLayout:
                        orientation: "horizontal"
                        spacing: "10dp"
                        size_hint_y: None
                        height: "50dp"
                        size_hint_x: 1
                        pos_hint: {"center_x": 0.5}

                        MDRaisedButton:
                            text: "Şifreyi Değiştir"
                            size_hint_x: 1
                            on_release: app.reset_password()

                        MDRaisedButton:
                            text: "Giriş Yap"
                            size_hint_x: 1
                            on_release: app.go_to_login()


            # Books Screen
            Screen:
                id: books_screen

                name: 'books'

                BoxLayout:
                    orientation: 'vertical'

                MDTopAppBar:
                    title: "Sessizce Oku"
                    md_bg_color: app.theme_cls.primary_color
                    specific_text_color: 1, 1, 1, 1
                    elevation: 10
                    left_action_items: [["menu", lambda x: app.open_nav_drawer()]]

                ScrollView:
                    MDGridLayout:
                        adaptive_size: True
                        adaptive_height: True
                        spacing: "16dp"
                        padding: "20dp"

                        MDCard:
                            size_hint: 1, 1
                            BoxLayout:
                                orientation: "vertical"
                                MDLabel:
                                    text: "Kitap 1"
                                MDRaisedButton:
                                    text: "Oku"

            Screen:
                name:"read_book"
                id:read_book_screen
                BoxLayout:
                    orientation: 'vertical'

                    MDTopAppBar:
                        title: "Kitap İçeriği"
                        md_bg_color: app.theme_cls.primary_color
                        specific_text_color: 1, 1, 1, 1
                        elevation: 10
                        left_action_items: [["arrow-left", lambda x: app.go_to_books_screen()]]

                    ScrollView:
                        MDGridLayout:
                            cols: 1
                            spacing: "16dp"
                            padding: "20dp"
                            size_hint_y: None
                            height: self.minimum_height
                            

                            MDLabel:
                                id: book_title
                                text: "Kitap Başlığı"
                                theme_text_color: "Secondary"
                                halign: "center"

                            

                            # Cümlelerin ve videoların kaydırılabilir kısmı
                            ScrollView:
                                GridLayout:
                                    size_hint_y: None
                                    height: self.minimum_height
                                    MDLabel:
                                        id: sentence_text
                                        text: "Cümleler ve içerik"
                                        theme_text_color: "Secondary"
                                    # GIF veya video eklemek için buraya dinamik içerikler eklenebilir
                                    BoxLayout:
                                        id: transcript_layout
                                        orientation: 'vertical'
                                        size_hint_y: None
                                        height: self.minimum_height
                    BoxLayout:
                        orientation: 'vertical'
                        size_hint_y: None
                        height: "60dp"
                        spacing: "20dp"
                        MDLabel:
                            id: book_content
                            text: "Kitap İçeriği"
                            theme_text_color: "Secondary"
                            halign: "center"
                            size_hint_y: None
                            height: "50dp"
                            size_hint_x: 1
                            size_hint_y: None
                            position_hint: {"center_x": 0.5, "center_y": 0.5}
                    BoxLayout:
                        orientation: 'horizontal'
                        size_hint_y: None
                        height: "60dp"
                        spacing: "20dp"
                        padding: "90dp", "20dp", "90dp", "20dp"
                        pos_hint: {"center_y": 0.1}

                        MDRaisedButton:
                            text: "Önceki"
                            size_hint_y: None
                            height: "50dp"
                            on_release: app.show_previous_sentence()

                        MDRaisedButton:
                            text: "Sonraki"
                            size_hint_y: None
                            height: "50dp"
                            on_release: app.show_next_sentence()       
            Screen:
                name:"favorites"
                id:favorites_screen
                BoxLayout:
                    orientation: 'vertical'

                    MDTopAppBar:
                        title: "Favori Kitaplar"
                        md_bg_color: app.theme_cls.primary_color
                        specific_text_color: 1, 1, 1, 1
                        elevation: 10
                        left_action_items: [["arrow-left", lambda x: app.go_to_books_screen()]]

                    ScrollView:
                        GridLayout:
                            cols: 1
                            spacing: "16dp"
                            padding: "20dp"
                            size_hint_y: None
                            height: self.minimum_height
                            

                    

        MDNavigationDrawer:
            id: nav_drawer
            radius: 0, dp(16), dp(16), 0
            width: "200dp"
            MDNavigationDrawerMenu:
                MDNavigationDrawerHeader:
                    text: "Profil sayfası"
                    padding: "30dp"
                MDNavigationDrawerLabel:
                    text: "Ceyda Gül"
                MDNavigationDrawerLabel:
                    text: "ceydagul@gmail.com"
                MDNavigationDrawerItem:
                    id: favorites
                    text: "Favoriler"
                    icon: "heart"
                    on_release: app.go_to_favorites()
                MDNavigationDrawerItem:
                    text: "Çıkış Yap"
                    icon: "exit-to-app"
                    on_release: app.logout(), app.close_nav_drawer()                                      
       
'''


class BookCatalogApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def go_to_favorites(self):
        self.get_favorite_books()
        self.root.ids.screen_manager.current = "favorites"

    def get_favorite_books(self):
        favorite_url = server_url + "api/books/get_user_favorite_books/1"

        response = requests.get(favorite_url)
        print(f"Response: {response.text}")
        if response.status_code == 200:
            favorite_books = response.json()
            self.display_favorite_books(favorite_books)
        else:
            print(
                f"Favori kitaplar alınamadı! Durum Kodu: {response.status_code}")
            print(f"Response: {response.text}")

    def add_to_favorites(self, button):
        if hasattr(button, 'is_favorited') and button.is_favorited:
            favorite_url = server_url + "api/books/remove_favorite_book"
            data = {
                "user_id": "1",
                "book_id": "2"
            }
            response = requests.post(favorite_url, json=data)
            if response.status_code != 200:
                print(
                    f"Kitap favorilerden çıkarılamadı! Durum Kodu: {response.status_code}")
                print(f"Response: {response.text}")
                return
            else:
                button.is_favorited = False
                button.text_color = (1, 1, 1, 1)  # Change color to white
                MDSnackbar(
                    MDLabel(
                        text="Favorilerden çıkarıldı!",
                        text_color="#393231",
                    ),
                ).open()
        else:
            favorite_url = server_url + "api/books/add_favorite_book"
            data = {
                "user_id": "1",
                "book_id": "2"
            }
            print(f"Sending data: {data} to {favorite_url}")
            response = requests.post(favorite_url, json=data)
            if response.status_code != 200:
                print(
                    f"Kitap favorilere eklenemedi! Durum Kodu: {response.status_code}")
                print(f"Response: {response.text}")
                return
            else:
                button.is_favorited = True
                button.text_color = (1, 0, 0, 1)  # Change color to red
                MDSnackbar(
                    MDLabel(
                        text="Favorilere eklendi!",
                        text_color="#393231",
                    ),
                ).open()

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

    def go_to_books_screen(self):
        self.root.ids.screen_manager.current = "books"

    def go_to_read_book_screen(self, book_id):
        # Set the current book ID
        self.current_book_id = book_id  # Initialize current_book_id here

        print(f"Kitap okunuyor...")

        self.root.ids.screen_manager.current = "read_book"
        print(f"Kitap okundu sanki")
        self.load_book_content(book_id)

    def load_book_content(self, book_id):
        print(f"Kitap içeriği yükleniyor...")
        book_content = get_book_content_by_id(book_id)

        if book_content:
            # Listenin tüm öğelerini alıyoruz (örneğin, kitap içeriği)
            self.book_details = book_content
            print(f"Kitap detayları: {self.book_details}")
            title = self.book_details[0].get(
                "title", "Başlık Bilgisi Yok")

            self.root.ids.book_title.text = title
            self.sentences = sorted(
                self.show_next_sentence, key=lambda x: x['nth_sentence'])
            self.current_sentence_index = 0
            self.show_next_sentence()  # İlk cümleyi göster

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
        email = self.root.ids.login_username.text
        password = self.root.ids.password.text
        print(f"Kullanıcı adı: {email}, Şifre: {password}")
        # Kullanıcı adı ve şifre kontrolü
        if email == "root" and password == "1234":
            # Kullanıcı adı ve şifre doğruysa, kitaplar sayfasına geçiş yap
            self.root.ids.screen_manager.current = "books"
            # Kitapları yükle
            self.load_books()
            return

        # Sunucuya giriş bilgilerini gönder
        login_url = server_url + "api/users/login"
        data = {
            "email": email,
            "password": password
        }
        response = requests.post(login_url, json=data)

        if response.status_code == 200:
            self.root.ids.screen_manager.current = "books"
            self.load_books()
        else:
            print(f"Giriş başarısız! Durum Kodu: {response.status_code}")

    def display_favorite_books(self, favorite_books):
        screen_width = Window.width
        screen_height = Window.height
        print("Width:", Window.width)
        print("Height:", Window.height)
        # Başlangıçta her satırda 2 kitap olacak
        books_per_row = 2

        # Ekran genişliğine göre kitap sayısını ayarlıyoruz
        if screen_width > 900:
            books_per_row = 4
        elif screen_width > 600:
            books_per_row = 3

        # Ekran genişliğine göre kitap kartı boyutlarını ayarlıyoruz
        # Boşlukları hesaba katarak boyut hesaplaması yapıyoruz
        padding_left_right = dp(20)  # Sol ve sağ boşluklar
        spacing = dp(10)  # Kitaplar arasındaki boşluk

        # Her kitap kartı arasındaki boşluğu ve padding'i hesaba katarak kitap kartının genişliğini hesaplıyoruz
        available_width = screen_width - \
            padding_left_right - spacing * (books_per_row - 1)
        book_width = available_width / books_per_row
        print(screen_width)
        # Kitap kartlarının yüksekliği, genişliğe orantılı olacak şekilde ayarlanır
        book_height = book_width * 1.5  # Yükseklik genişliğin 1.5 katı olacak

        # GridLayout'u dinamik yükseklikle ayarlıyoruz
        book_grid = GridLayout(
            cols=books_per_row,
            spacing=spacing,
            padding=[padding_left_right / 2, dp(10)],  # Sol ve sağ padding
            size_hint_y=None  # Yüksekliği içeriğe göre ayarla
        )
        book_grid.bind(minimum_height=book_grid.setter(
            'height'))  # İçeriğe göre yüksekliği ayarla

        all_books = get_books()
        # Kitapları GridLayout'a ekliyoruz
        for all_book in all_books:
            all_book_id = all_book.get("id")
            all_book_cover = all_book.get("cover")
            for book in favorite_books:
                book_id = book.get("book_id")
                if all_book_id == book_id:
                    title = book.get("title", "Başlık Bilgisi Yok")
                    image_url_full = server_url + "static/covers/" + all_book_cover

                    # Kitap kartını orantılayarak oluşturuyoruz
                    print(book_width, book_height)
                    book_card = Builder.load_string(f'''
MDCard:
    size_hint: None, None
    size: "{book_width*0.8}dp", "{book_height}dp"  # Kitap kartı boyutlarını burada orantılı olarak ayarlıyoruz
    elevation: 5
    radius: [12,]
    orientation: "vertical"
    padding: "8dp"

    MDSmartTile:
        radius: 12
        box_radius: [0, 0, 12, 12]
        box_color: 1, 1, 1, .2
        source: "{image_url_full}"
        size_hint: None, None
        size: "{book_width*0.8}dp", "{book_height * 0.8}dp"  # Görsel boyutlarını orantılı olarak ayarlıyoruz
        pos_hint: {{"center_x": .5}}
        overlap: False
        lines: 2
        text: "{title}"
        on_release: app.read_book({book_id})

    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        height: "50dp"
        padding: "5dp"
        spacing: "10dp"

        MDIconButton:
            id: favorite_button
            icon: "heart"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            on_release: app.add_to_favorites(self)
            size_hint: None, None
            size: "40dp", "40dp"
            is_favorited: False

            ''')
                    book_grid.add_widget(book_card)

        # ScrollView içine GridLayout'u yerleştiriyoruz
        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(book_grid)

        # Favori kitap ekranını temizleyip ScrollView'u ekliyoruz
        self.root.ids.favorites_screen.add_widget(scroll_view)

    def load_books(self):
        books = get_books()
        screen_width = Window.width
        screen_height = Window.height
        print("Width:", Window.width)
        print("Height:", Window.height)
        # Başlangıçta her satırda 2 kitap olacak
        books_per_row = 2

        # Ekran genişliğine göre kitap sayısını ayarlıyoruz
        if screen_width > 900:
            books_per_row = 4
        elif screen_width > 600:
            books_per_row = 3

        # Ekran genişliğine göre kitap kartı boyutlarını ayarlıyoruz
        # Boşlukları hesaba katarak boyut hesaplaması yapıyoruz
        padding_left_right = dp(20)  # Sol ve sağ boşluklar
        spacing = dp(10)  # Kitaplar arasındaki boşluk

        # Her kitap kartı arasındaki boşluğu ve padding'i hesaba katarak kitap kartının genişliğini hesaplıyoruz
        available_width = screen_width - \
            padding_left_right - spacing * (books_per_row - 1)
        book_width = available_width / books_per_row
        print(screen_width)
        # Kitap kartlarının yüksekliği, genişliğe orantılı olacak şekilde ayarlanır
        book_height = book_width * 1.5  # Yükseklik genişliğin 1.5 katı olacak

        # GridLayout'u dinamik yükseklikle ayarlıyoruz
        book_grid = GridLayout(
            cols=books_per_row,
            spacing=spacing,
            padding=[padding_left_right / 2, dp(10)],  # Sol ve sağ padding
            size_hint_y=None  # Yüksekliği içeriğe göre ayarla
        )
        book_grid.bind(minimum_height=book_grid.setter(
            'height'))  # İçeriğe göre yüksekliği ayarla

        # Kitapları GridLayout'a ekliyoruz
        for book in books:
            book_id = book.get("id")
            title = book.get("title", "Başlık Bilgisi Yok")
            image_url = book.get("cover")
            image_url_full = server_url + "static/covers/" + image_url

            # Kitap kartını orantılayarak oluşturuyoruz
            print(book_width, book_height)
            book_card = Builder.load_string(f'''
MDCard:
    size_hint: None, None
    size: "{book_width*0.8}dp", "{book_height}dp"  # Kitap kartı boyutlarını burada orantılı olarak ayarlıyoruz
    elevation: 5
    radius: [12,]
    orientation: "vertical"
    padding: "8dp"

    MDSmartTile:
        radius: 12
        box_radius: [0, 0, 12, 12]
        box_color: 1, 1, 1, .2
        source: "{image_url_full}"
        size_hint: None, None
        size: "{book_width*0.8}dp", "{book_height * 0.8}dp"  # Görsel boyutlarını orantılı olarak ayarlıyoruz
        pos_hint: {{"center_x": .5}}
        overlap: False
        lines: 2
        text: "{title}"
        on_release: app.read_book({book_id})

    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        height: "50dp"
        padding: "5dp"
        spacing: "10dp"

        MDIconButton:
            id: favorite_button
            icon: "heart"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            on_release: app.add_to_favorites(self)
            size_hint: None, None
            size: "40dp", "40dp"
            is_favorited: False

            ''')
            book_grid.add_widget(book_card)

        # ScrollView içine GridLayout'u yerleştiriyoruz
        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(book_grid)

        # Kitap ekranını temizleyip ScrollView'u ekliyoruz
        self.root.ids.books_screen.clear_widgets()
        self.root.ids.books_screen.add_widget(scroll_view)

    def read_book(self, book_id):
        print(f"Kitap {book_id} okunuyor...")
        book_content = get_book_content_by_id(book_id)
        print(f"Kitap İçeriği: {book_content}")
        self.root.ids.screen_manager.current = "read_book"
        self.sentences = sorted(book_content, key=lambda x: x['nth_sentence'])
        self.current_sentence_index = 0
        self.show_next_sentence()  # İlk cümleyi göster

        # İlk cümleyi göstermek için döngüyü kaldırıyoruz
        if self.sentences:
            first_sentence = self.sentences[0]
            print(f"Kitap İçeriği: {first_sentence.get('sentence')}")
            self.root.ids.book_content.text = first_sentence.get('sentence')

    def show_next_sentence(self):
        if self.current_sentence_index < len(self.sentences) - 1:
            self.current_sentence_index += 1
            next_sentence = self.sentences[self.current_sentence_index]
            self.root.ids.book_content.text = next_sentence.get('sentence')
            print(f"Sonraki Cümle: {next_sentence.get('sentence')}")
        else:
            print("Sonraki cümle yok.")

    def show_previous_sentence(self):
        if self.current_sentence_index > 0:
            self.current_sentence_index -= 1
            previous_sentence = self.sentences[self.current_sentence_index]
            self.root.ids.book_content.text = previous_sentence.get('sentence')
            print(f"Önceki Cümle: {previous_sentence.get('sentence')}")
        else:
            print("Önceki cümle yok.")

    def add_to_read_later(self, book_id):
        print(f"Kitap {book_id} okunacaklara eklendi!")

    def go_to_register(self):
        self.root.ids.screen_manager.current = "register"

    def go_to_forgot_password(self):
        self.root.ids.screen_manager.current = "forgot_password"

    def register(self):
        username = self.root.ids.register_username.text
        password = self.root.ids.register_password.text
        email = self.root.ids.register_email.text

        register_url = server_url + "api/users/register"
        print(f"Kayıt URL'si: {register_url}")
        print(
            f"Kullanıcı adı: {username}, Şifre: {password}, E-posta: {email}")
        data = {
            "user_name": username,
            "email": email,
            "password": password
        }

        try:
            response = requests.post(register_url, json=data)

            if response.status_code == 201:
                self.root.ids.screen_manager.current = "login"
            else:
                print(
                    f"Kayıt başarısız! Hata: {response.json().get('error', 'Bilinmeyen bir hata')}")

        except requests.exceptions.RequestException as e:
            print(f"Sunucu hatası: {str(e)}")

    def go_to_login(self):
        self.root.ids.screen_manager.current = "login"

    def on_start(self):
        self.set_theme()

    def set_theme(self):
        # Arka plan rengini ekru (#FFF4E6) olarak ayarla
        self.theme_cls.primary_hue = "300"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Purple"  # Lila

        # Renk paletlerini isteğe göre ayarla
        if self.theme_cls.primary_palette == "Purple":
            self.theme_cls.primary_palette = "Purple"  # Alternatif
            self.theme_cls.accent_palette = "Gray"

    # Seçilecek renkler öncelikli  eşleşen bilği net olur sonra opsiyon dondurtular


BookCatalogApp().run()
