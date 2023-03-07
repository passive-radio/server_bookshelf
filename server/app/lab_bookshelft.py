import csv
from dataclasses import dataclass
import re

@dataclass
class BookInfo:
    isbn: int = None
    internal_id: int = None
    title: str = None
    author: str = None
    publisher: str = None
    category: str = None

class Bookshelf:
    def __init__(self, bookshelf_path: str) -> None:
        self.BOOKSHELF_PATH = bookshelf_path
        self.books: list[BookInfo] = []
        
        try: 
            with open(self.BOOKSHELF_PATH, mode='r', encoding='utf-8', newline='') as buf:
                reader = csv.reader(buf, delimiter=',')
                i = 0
                for row in reader:
                    if i > 0:
                        self.load_book(row[0], row[1], row[2], row[3], row[4], row[5])
                    i += 1
            print("loading bookshelf completed!")
        except:
            with open(self.BOOKSHELF_PATH, mode='w', encoding='utf-8', newline='') as buf:
                writer = csv.writer(buf, delimiter=',')
                writer.writerow(["isbn", "internal_id", "title", "author", "publisher", "category"])
            print("new bookshelf csv created!")
    
    def add_book(self, isbn: int, internal_id: int, title: str, author: str, publisher: str, category: str):
        if not self.is_in_bookshelf_internal_id(int(internal_id)):
            
            self.books.append(BookInfo(isbn, int(internal_id), title, author, publisher, category))
            self._update_bookshelf(isbn, internal_id, title, author, publisher, category)
        else:
            pass
    
    def load_book(self, isbn: int, internal_id: int, title: str, author: str, publisher: str, category: str):
        if not self.is_in_bookshelf_internal_id(int(internal_id)):
            self.books.append(BookInfo(isbn, int(internal_id), title, author, publisher, category))
        else:
            pass
    
    def _update_bookshelf(self, isbn, internal_id, title, author, publisher, category):
        with open(self.BOOKSHELF_PATH, mode='a', encoding='utf-8', newline='') as buf:
            writer = csv.writer(buf, delimiter=',')
            writer.writerow([isbn, internal_id, title, author, publisher, category])
        
    def _get_isbn_list(self):
        _isbn_list = []
        
        if len(self.books) < 1:
            return _isbn_list
        
        for book in self.books:
            _isbn_list.append(book.isbn)
        return _isbn_list
    
    def _get_internal_id_list(self):
        _internal_id_list = []

        if len(self.books) < 1:
            return _internal_id_list
        
        for book in self.books:
            _internal_id_list.append(book.internal_id)
        return _internal_id_list
    
    def is_in_bookshelf(self, isbn: int):
        return int(isbn) in self._get_isbn_list()
    
    def is_in_bookshelf_internal_id(self, internal_id: int):
        return int(internal_id) in self._get_internal_id_list()