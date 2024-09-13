import unittest
import goodscrape
import logging

class GRBookTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.maxDiff=5000
        cls.known_answers = [
            {
                "url": "https://www.goodreads.com/book/show/166997.Stoner",
                "title": "Stoner",
                "cover_image": "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1320600716i/166997.jpg",
                "author": "John  Williams",
                "author_link": "https://www.goodreads.com/author/show/51229.John_Williams",
                "rating": "4.34",
                "pages_format": "292 pages, Paperback",
                "publication_info": "First published January 1, 1965",
                "description": """William Stoner is born at the end of the nineteenth century into a dirt-poor Missouri farming family. Sent to the state university to study agronomy, he instead falls in love with English literature and embraces a scholar’s life, so different from the hardscrabble existence he has known. And yet as the years pass, Stoner encounters a succession of disappointments: marriage into a “proper” family estranges him from his parents; his career is stymied; his wife and daughter turn coldly away from him; a transforming experience of new love ends under threat of scandal. Driven ever deeper within himself, Stoner rediscovers the stoic silence of his forebears and confronts an essential solitude. John Williams’s luminous and deeply moving novel is a work of quiet perfection. William Stoner emerges from it not only as an archetypal American, but as an unlikely existential hero, standing, like a figure in a painting by Edward Hopper, in stark relief against an unforgiving world.""",
                "genres": ['Fiction', 'Historical Fiction', 'Literature', 'Novels', 'American', 'Literary Fiction', 'Classics']
            },
            {
                "url": "https://www.goodreads.com/book/show/40995.Sword_Citadel",
                "title": "Sword & Citadel",
                "cover_image": "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1543852974i/40995.jpg",
                "author": "Gene Wolfe",
                "author_link": "https://www.goodreads.com/author/show/23069.Gene_Wolfe",
                "rating": "4.34",
                "pages_format": "411 pages, Paperback",
                "publication_info": "First published October 15, 1994",
                "description": "The Book of the New Sun is unanimously acclaimed as Gene Wolfe's most remarkable work, hailed as \"a masterpiece of science fantasy comparable in importance to the major works of Tolkien and Lewis\" by Publishers Weekly , and \"one of the most ambitious works of speculative fiction in the twentieth century\" by The Magazine of Fantasy and Science Fiction . Sword & Citadel brings together the final two books of the tetralogy in one volume: The Sword of the Lictor is the third volume in Wolfe's remarkable epic, chronicling the odyssey of the wandering pilgrim called Severian, driven by a powerful and unfathomable destiny, as he carries out a dark mission far from his home. The Citadel of the Autarch brings The Book of the New Sun to its harrowing conclusion, as Severian clashes in a final reckoning with the dread Autarch, fulfilling an ancient prophecy that will forever alter the realm known as Urth.",
                "genres": ['Fantasy', 'Science Fiction', 'Fiction', 'Science Fiction Fantasy', 'Speculative Fiction', 'Dying Earth', 'Novels']
            }
        ]
        cls.books = [ goodscrape.GRBook(book["url"]) for book in cls.known_answers ]

    def test_get_title(self):
        for i, book in enumerate(self.books):
            title = book.get_title()
            self.assertEqual(title, self.known_answers[i]["title"])

    def test_get_cover_image(self):
        for i, book in enumerate(self.books):
            cover_image = book.get_cover_image()
            self.assertEqual(cover_image, self.known_answers[i]["cover_image"])

    def test_get_author(self):
        for i, book in enumerate(self.books):
            author = book.get_author()
            self.assertEqual(author, self.known_answers[i]["author"])

    def test_get_author_link(self):
        for i, book in enumerate(self.books):
            author_link = book.get_author_link()
            self.assertEqual(author_link, self.known_answers[i]["author_link"])

    def test_get_rating(self):
        for i, book in enumerate(self.books):
            rating = book.get_rating()
            self.assertEqual(rating, self.known_answers[i]["rating"])

    def test_get_pages_format(self):
        for i, book in enumerate(self.books):
            pages_format = book.get_pages_format()
            self.assertEqual(pages_format, self.known_answers[i]["pages_format"])

    def test_get_publication_info(self):
        for i, book in enumerate(self.books):
            publication_info = book.get_publication_info()
            self.assertEqual(publication_info, self.known_answers[i]["publication_info"])

    def test_get_description(self):
        for i, book in enumerate(self.books):
            description = book.get_description()
            self.assertEqual(description, self.known_answers[i]["description"])

    def test_get_genres(self):
        for i, book in enumerate(self.books):
            genres = book.get_genres()
            self.assertEqual(genres, self.known_answers[i]["genres"])

if __name__ == "__main__":
    unittest.main()