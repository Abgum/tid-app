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
            spacing= dp(10),
            padding=[ dp(10), dp(10)],  # Sol ve sağ padding
            size_hint_y=None  # Yüksekliği içeriğe göre ayarla
        )
    col2_grid.bind(minimum_height=col2_grid.setter('height'))  # İçeriğe göre yüksekliği ayarla
    
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
                        id: old_password
                        hint_text: "Eski Şifre"
                        size_hint_y: None
                        height: "40dp"
                        password: True
                        pos_hint: {"center_x": 0.5}
                    MDTextField:
                        id: new_password
                        hint_text: "Yeni Şifre"
                        size_hint_y: None
                        height: "40dp"
                        password: True
                        pos_hint: {"center_x": 0.5}                    
                    MDTextField:
                        id: confirm_new_password
                        hint_text: "Yeni Şifreyi Tekrar Gir"
                        size_hint_y: None
                        password: True
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

                            MDLabel:
                                id: book_content
                                text: "Kitap İçeriği"
                                theme_text_color: "Secondary"

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
                        orientation: 'horizontal'
                        size_hint_y: None
                        height: "60dp"
                        spacing: "20dp"
                        padding: "130dp", "20dp", "130dp", "20dp"
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
            self.sentences = sorted(self.show_next_sentence, key=lambda x:x['nth_sentence'])
            self.current_sentence_index = 0
            self.show_next_sentence()  # İlk cümleyi göster

    def show_previous_sentence(self):
        current_sentence = self.root.ids.sentence_text.text
        sentences = self.get_current_sentences()

        if current_sentence not in sentences:
            current_index = 0
        else:
            current_index = sentences.index(current_sentence)

        if current_index > 0:
            previous_sentence = sentences[current_index - 1]
            self.root.ids.sentence_text.text = previous_sentence
            self.update_transcript(current_index - 1)

    def show_next_sentence(self):
        current_sentence = self.root.ids.sentence_text.text
        sentences = self.get_current_sentences()

        if current_sentence not in sentences:
            current_index = -1
        else:
            current_index = sentences.index(current_sentence)

        if current_index < len(sentences) - 1:
            next_sentence = sentences[current_index + 1]
            self.root.ids.sentence_text.text = next_sentence
            self.update_transcript(current_index + 1)

    def update_transcript(self, index):
        transcript = self.book_details[index].get('transcript', '')
        transcript_parts = transcript.split(',')

    # Clear the existing transcript parts in the UI
        self.root.ids.transcript_layout.clear_widgets()

    # Add each transcript part to the UI
        for part in transcript_parts:
            part_label = MDLabel(text=part, theme_text_color="Secondary")
            self.root.ids.transcript_layout.add_widget(part_label)

        print(f"Transcript parts: {transcript_parts}")
        self.root.ids.transcript_layout.height = len(
            transcript_parts) * 50  # Adjust the height as needed
        self.root.ids.transcript_layout.size_hint_y = None

    def get_current_sentences(self):
        # Check if book_details is set
        if not hasattr(self, 'book_details'):
            print("No book details available!")
            return []

    # Extract sentences from book details
        sentences = [detail.get('sentence', '')
                     for detail in self.book_details]
        return sentences

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
            # Giriş başarılıysa kitap sayfasına geçiş yap
            self.root.ids.screen_manager.current = "books"
            # Kitapları yükle
            self.load_books()
        else:
            # Hata mesajı göster
            print("Giriş başarısız!")

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
            available_width = screen_width - padding_left_right - spacing * (books_per_row - 1)
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
            book_grid.bind(minimum_height=book_grid.setter('height'))  # İçeriğe göre yüksekliği ayarla

            # Kitapları GridLayout'a ekliyoruz
            for book in books:
                book_id = book.get("book", 0)
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
            icon: "heart"
            on_release: app.add_to_favorites({book_id})
            size_hint: None, None
            size: "40dp", "40dp"

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
        print(f"Kitap İçeriğibuudur")

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
        password = self.root.ids.password.text
        new_password = self.root.ids.new_password.text
        confirm_password = self.root.ids.confirm_new_password.text
        # Şifre doğrulama
        if new_password != confirm_password:
            show_popup("Hata", "Yeni şifre ve tekrar girilen şifre aynı değil!")
            return

        # Sunucuya şifre sıfırlama isteği gönder
        reset_url = server_url + "api/users/get_all_users"
        data = {"email": email, "new_password": new_password}
        response = requests.get(reset_url, json=data)
        is_valid = check_user_credentials(response.json(), email, hash_password(password))
        print(f"pass: {password}, hashed {hash_password(password)}")
        if response.status_code == 200:
            # Şifre sıfırlama başarılı
            if(is_valid):
                print("Şifre sıfırlama başarılı.")
                self.root.ids.screen_manager.current = "login"
            else:
                show_popup("Hata", "Eski şifre bulunamadı!")
        else:
            # Şifre sıfırlama başarısız
            error_data = response.json()
            
            if error_data.get("error") == "old_password_not_found":
                show_popup("Hata", "Eski şifre bulunamadı!")
            elif error_data.get("error") == "password_mismatch":
                show_popup("Hata", "Yeni şifre ve tekrar girilen şifre aynı değil!")
            else:
                show_popup("Hata", "Şifre sıfırlama başarısız! Lütfen tekrar deneyin.")


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
