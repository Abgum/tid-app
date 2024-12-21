from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.pagelayout import PageLayout
from kivy.uix.relativelayout import RelativeLayout
from data_requests import get_books, get_book_content_by_id, server_url
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import RoundedRectangle


story = [
    {
        "sentence": "The boy is running asdadaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbb.",
        "gifs": [
            "static/book1.jpg",
            "static/book2.jpg",
            "static/book1.jpg",
            "static/book2.jpg",
            "static/book1.jpg",
            "static/book2.jpg",
            "static/book1.jpg",
            "static/book2.jpg",
            "static/book2.jpg",
        ],
    },
    {
        "sentence": "The girl is reading a book.",
        "gifs": ["read1.gif", "read2.gif", "read3.gif"],
    },
    {"sentence": "The dog is barking.", "gifs": ["bark1.gif", "bark2.gif"]},
]

books = get_books()
print("book2", books)


Window.clearcolor = (0.8, 0.9, 1, 1)  # Pastel mavi tonu


class HoverButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_enter=self.on_hover)
        self.bind(on_leave=self.on_leave)

    def on_hover(self, instance):
        # Change background color on hover
        self.background_color = (0.9, 0.6, 0.2, 1)  # Hover color (e.g., gold)

    def on_leave(self, instance):
        # Reset the background color when the mouse leaves
        self.background_color = (0.8, 0.7, 0.2, 1)  # Original color


class BooksPage(BoxLayout):
    page_name = "books"
    readable_name = "Kitaplar"
    icon_path = "static/book.png"

    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.screen_manager = screen_manager
        self.current_page = 0
        self.books_per_page = 1  # Bir sayfada gösterilecek kitap sayısı
        self.font_name = 'Roboto'  # Modern bir font kullanabilirsiniz

        # Search bar at the top
        search_layout = BoxLayout(
            size_hint=(1, 0.1), spacing=10, padding=[10, 10, 10, 10]
        )
        self.search_input = TextInput(
            hint_text="Search for a book...",
            size_hint=(1, 1),
            multiline=False,
            # Antrasit arka plan (#2C2C2C)
            background_color=(0.7, 0.85, 1, 1),  # Mavi pastel
            foreground_color=(0, 0, 0, 1),  # Siyah yazı
            cursor_color=(1, 1, 1, 1),  # Beyaz imleç
        )
        self.search_input.bind(text=self.filter_books)
        search_layout.add_widget(self.search_input)

        self.clear_search_button = HoverButton(
            text="Clear",
            size_hint=(0.2, 1),
            background_color=(0.8, 0.7, 0.2, 1),
            color=(1, 1, 1, 1),  # Beyaz yazı
        )
        self.clear_search_button.bind(on_press=self.clear_search)
        search_layout.add_widget(self.clear_search_button)

        self.add_widget(search_layout)

        # Scrollable layout for books
        self.scroll_view = ScrollView(do_scroll_x=True, do_scroll_y=False)
        self.scroll_layout = BoxLayout(
            orientation="horizontal", size_hint=(None, 1)
        )
        self.scroll_layout.size_hint_x = None
        self.scroll_layout.width = self.width * 1.5
        self.scroll_view.add_widget(self.scroll_layout)
        self.add_widget(self.scroll_view)

        self.displayed_books = books[:]  # Start with the full list of books

        # Add navigation buttons at the bottom
        nav_buttons_layout = BoxLayout(size_hint=(1, 0.1), spacing=10)

        self.previous_button = Button(
            text="Önceki",
            size_hint=(0.5, 1),
            background_color=(79 / 255, 79 / 255, 79 / 255, 1),
            color=(1, 1, 1, 1),
        )
        self.previous_button.bind(on_press=self.go_to_previous_page)
        nav_buttons_layout.add_widget(self.previous_button)

        self.next_button = Button(
            text="Sonraki",
            size_hint=(0.5, 1),
            background_color=(79 / 255, 79 / 255, 79 / 255, 1),
            color=(1, 1, 1, 1),
        )
        self.next_button.bind(on_press=self.go_to_next_page)
        nav_buttons_layout.add_widget(self.next_button)

        self.add_widget(nav_buttons_layout)

        self.load_books()

    def load_books(self):
        self.scroll_layout.clear_widgets()
        self.scroll_layout.width = len(
            self.displayed_books) * (self.width / self.books_per_page)

        start_index = self.current_page * self.books_per_page
        end_index = start_index + self.books_per_page
        books_to_display = self.displayed_books[start_index:end_index]

        for book in books_to_display:
            book_layout = BoxLayout(
                orientation="vertical",
                size_hint=(None, None),
                width=self.width / self.books_per_page,
                height=self.height * 0.8,
                pos_hint={"center_x": 0.5, "center_y": 0.5},
            )

            relative_layout = RelativeLayout(size_hint=(1, 0.8))
            cover = AsyncImage(
                source=(server_url + book["cover_path"]),
                size_hint=(1, 1),
                allow_stretch=True,
            )
            relative_layout.add_widget(cover)

            title_label = Button(
                text=book["title"],
                size_hint=(1, None),
                height=40,
                background_color=(1, 0.6, 0.6, 0.7),
                color=(0, 0, 0, 1),
                halign="center",
                valign="middle",
            )
            relative_layout.add_widget(title_label)
            book_layout.add_widget(BoxLayout(size_hint=(1, None), height=10))
            book_layout.add_widget(relative_layout)

            read_button = Button(
                text="Kitabı Oku",
                size_hint=(1, 0.2),
                pos_hint={"center_x": 0.5},
                # Altın sarısı (#FFD700)
                background_color=(1, 1, 0.8, 1),
                color=(18 / 255, 18 / 255, 18 / 255, 1),  # Koyu yazı rengi
            )
            read_button.bind(on_press=lambda instance,
                             book=book: self.open_book(book))
            book_layout.add_widget(read_button)

            self.scroll_layout.add_widget(book_layout)

        self.previous_button.disabled = self.current_page == 0
        self.next_button.disabled = (
            self.current_page + 1) * self.books_per_page >= len(self.displayed_books)

    def filter_books(self, instance, text):
        # Filter books based on search input
        search_query = text.lower()
        self.displayed_books = [
            book for book in books if search_query in book["title"].lower()
        ]
        self.current_page = 0  # Reset to the first page after filtering
        self.load_books()

    def clear_search(self, instance):
        # Clear the search input and reset the displayed books
        self.search_input.text = ""
        self.displayed_books = books[:]
        self.current_page = 0  # Reset to the first page
        self.load_books()

    def open_book(self, book):
        book_content_screen = self.screen_manager.get_screen("book_content")
        book_content_page = book_content_screen.children[0]
        book_content_page.update_content(
            get_book_content_by_id(book["book_id"]), book["title"]
        )
        self.screen_manager.transition.direction = "left"
        self.screen_manager.current = "book_content"

    def go_to_next_page(self, instance):
        if (self.current_page + 1) * self.books_per_page < len(self.displayed_books):
            self.current_page += 1
            self.load_books()

    def go_to_previous_page(self, instance):
        if self.current_page > 0:
            self.current_page -= 1
            self.load_books()
