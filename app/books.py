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

# Sunucu URL'si
server_url = "http://127.0.0.1:2020/"

# Kitapları almak için fonksiyon


def get_books():
    response = requests.get(server_url + "api/books/get_all_books")
    if response.status_code == 200:
        return response.json()  # JSON formatında kitap verilerini döndürür
    return []

# Kitap içeriğini almak için fonksiyon


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
    response = requests.get(server_url + "/book_contents/" + str(book_id))
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
                    GridLayout:
                        cols: 3
                        size_hint_y: None
                        height: "50dp"
                        spacing: "60dp"
                        pos_hint: {"center_x": 0.5}
                        MDRaisedButton:
                            text: "Giriş Yap"
                            size_hint_y: None
                            height: "50dp"
                            width: "120dp"
                            padding: "10dp", "10dp", "10dp", "10dp"
                            spacing: "40dp"
                            pos_hint: {"center_x": 0.5}
                            on_release: app.login()

                        MDRaisedButton:
                            text: "Kayıt Ol"
                            size_hint_y: None
                            height: "50dp"
                            spacing: "40dp"
                            width: "120dp"
                            padding: "10dp", "10dp", "10dp", "10dp"
                            pos_hint: {"center_x": 0.5}
                            on_release: app.go_to_register()

                        MDRaisedButton:
                            text: "Şifremi Unuttum"
                            size_hint_y: None
                            height: "50dp"
                            width: "120dp"
                            spacing: "40dp"
                            padding: "10dp", "10dp", "10dp", "10dp"
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
                    GridLayout:
                        cols: 2
                        size_hint_y: None
                        height: "50dp"
                        spacing: "225dp"
                        pos_hint: {"center_x": 0.5}
                        MDRaisedButton:
                            text: "Kayıt Ol"
                            size_hint_y: None
                            height: "50dp"
                            pos_hint: {"center_x": 0.5}
                            on_release: app.register()

                        MDRaisedButton:
                            text: "Giriş Yap"
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
                    GridLayout:
                        cols: 2
                        size_hint_y: None
                        height: "50dp"
                        spacing: "225dp"
                        pos_hint: {"center_x": 0.5}
                        MDRaisedButton:
                            text: "Şifreyi Sıfırla"
                            size_hint_y: None
                            height: "50dp"
                            pos_hint: {"center_x": 0.5}
                            on_release: app.reset_password()

                        MDRaisedButton:
                            text: "Giriş Yap"
                            size_hint_y: None
                            height: "75dp"
                            pos_hint: {"center_x": 0.5}
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
                "book_title", "Başlık Bilgisi Yok")
            self.root.ids.book_title.text = title
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

        # ScrollView içinde bir GridLayout oluşturuyoruz
        book_grid = GridLayout(
            cols=2,  # Her satırda 2 sütun
            spacing=dp(10),
            padding=dp(10),
            size_hint_y=None  # Dinamik olarak yüksekliği ayarlamak için
        )
        book_grid.bind(minimum_height=book_grid.setter(
            'height'))  # İçeriğe göre yüksekliği ayarla

        # Kitapları GridLayout'a ekliyoruz
        for book in books:
            book_id = book.get("book", 0)
            title = book.get("title", "Başlık Bilgisi Yok")
            image_url = book.get("cover")
            deneme = server_url + "static/covers/"+image_url

            book_card = Builder.load_string(f'''
MDCard:
    size_hint: None, None
    size: "180dp", "300dp"
    elevation: 5
    radius: [12,]
    orientation: "vertical"
    padding: "8dp"

    MDSmartTile:
        radius: 12
        box_radius: [0, 0, 12, 12]
        box_color: 1, 1, 1, .2
        source: "{deneme}"
        size_hint: None, None
        size: "180dp", "240dp"
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

        MDIconButton:
            icon: "bookmark-plus"
            on_release: app.add_to_read_later({book_id})
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
