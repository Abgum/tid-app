from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from login import LoginScreen
from books import BookCatalogApp
from books_page import BooksPage
from book_content_page import BookContentPage
from kivy.core.window import Window
from kivymd.app import MDApp


class BookApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        self.title = "TiD Çocuk Kitapları"
        screen_manager = ScreenManager()

        # main_page = MainPage(screen_manager)
        # main_screen = Screen(name=MainPage.page_name)
        # main_screen.add_widget(main_page)
        # screen_manager.add_widget(main_screen)

        # books_page = BooksPage(screen_manager)
        # books_screen = Screen(name=BooksPage.page_name)
        # books_screen.add_widget(books_page)
        # screen_manager.add_widget(books_screen)

        login_screen = LoginScreen(screen_manager)
        login_screen_instance = Screen(name="login")
        login_screen_instance.add_widget(login_screen)
        screen_manager.add_widget(login_screen_instance)

        books = BookCatalogApp(screen_manager)
        books_screen = Screen(name=BookCatalogApp.page_name)
        books_screen.add_widget(books)
        screen_manager.add_widget(books_screen)

        book_content_page = BookContentPage(screen_manager)
        book_content_screen = Screen(name=BookContentPage.page_name)
        book_content_screen.add_widget(book_content_page)
        screen_manager.add_widget(book_content_screen)

        screen_manager.current = LoginScreen.page_name

        return screen_manager


if __name__ == "__main__":
    BookApp().run()
