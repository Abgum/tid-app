import requests
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import ScrollView
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.imagelist import MDSmartTile
# Import MDToolbar from kivymd.uix.toolbar
# Use MDTopAppBar instead of MDToolbar
from kivymd.uix.toolbar import MDTopAppBar


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
        title: "Kitap Kataloğu"
        md_bg_color: app.theme_cls.primary_color
        specific_text_color: 1, 1, 1, 1
        elevation: 10


    ScrollView:
        MDGridLayout:
            padding: "8dp"
            spacing: "16dp"
            cols: 2
            size_hint_y: None
            height: self.minimum_height
'''


class BookCatalogApp(MDApp):
    def build(self):
        # Kitapları sunucudan çek
        books = get_books()
        # Kitap kartlarını oluştur
        book_cards = ""

        for book in books:
            # Her kitap için bir MDCard ekle
            # Eğer book_id None ise 0 olarak al
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

                MDRaisedButton:
                    text: "Kitabı Oku"
                    size_hint: None, None
                    size: "140dp", "40dp"
                    pos_hint: {"center_x": .5}
                    on_release: app.read_book(%d)
            ''' % (deneme, title, book_id)

        # Kitap kartlarını dinamik olarak yükle
        return Builder.load_string(KV + book_cards)

    def read_book(self, book_id):
        book_content = get_book_content_by_id(book_id)
        print(f"Kitap İçeriği: {book_content}")

    def on_start(self):
        # Başlangıçta tema seçim fonksiyonu
        self.set_theme()

    def set_theme(self):
        # Tema stilini değiştir
        if self.theme_cls.theme_style == "Light":
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"

        # Renk paletini değiştirme
        if self.theme_cls.primary_palette == "Orange":
            self.theme_cls.primary_palette = "Green"
        else:
            self.theme_cls.primary_palette = "Orange"


BookCatalogApp().run()
