import requests
import bs4
from bs4 import BeautifulSoup
import re
import logging
logger = logging.getLogger(__name__)

def _scrape_page(url: str, input: str = None) -> BeautifulSoup:
    if input is None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
        }
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            raise RuntimeError(f"Bad status code ({r.status_code})!")
        else:
            page = r.text
    else:
        page = input

    return BeautifulSoup(page, "html.parser")

class GRProfile:
    def __init__(self, username: str, input: str = None):
        self.username = username
        url = f"https://www.goodreads.com/{username}"
        self.soup = _scrape_page(url, input)

    def get_pfp_url(self) -> str:
        pfp = self.soup.find("img", class_="profilePictureIcon")

        if pfp is None:
            return None

        if pfp.has_attr('src'):
            return pfp['src']
        else:
            return None

    def get_profile_name(self) -> str:
        profileName = self.soup.find("h1", class_="userProfileName")
        return list(profileName.strings)[0].strip()

    def get_num_ratings(self) -> str:
        ratings = self.soup.find("a", string=re.compile(r"\d+ ratings"))
        return ratings.string.strip() if ratings is not None else None

    def get_average_rating(self) -> str:
        average = self.soup.find("a", string=re.compile(r"\(\d+\.\d+ avg\)"))
        return average.string.strip() if average is not None else None

class GRBook:
    def __init__(self, url: str, input: str = None):
        self.soup = _scrape_page(url, input)

    def get_cover_image(self) -> str:
        coverDiv = self.soup.find("div", class_="BookCover__image")
        if coverDiv is None:
            return None

        coverImg = coverDiv.find("img")
        if coverImg is None:
            return None
        
        return coverImg.get('src')
    
    def get_title(self) -> str:
        title = self.soup.find("h1", class_="Text__title1")
        if title is None:
            return None

        return title.string.strip() if title.string else None
    
    def get_author(self) -> str:
        author = self.soup.find("span", class_="ContributorLink__name")
        if author is None:
            return None
        
        return author.string.strip() if author.string else None
    
    def get_author_link(self) -> str:
        authorLink = self.soup.find("a", class_="ContributorLink")
        if authorLink is None:
            return None
        
        return authorLink.get('href')
    
    def get_average_rating(self) -> str:
        rating = self.soup.find("div", class_="RatingStatistics__rating")
        if rating is None:
            return None
        
        return rating.string.strip() if rating.string else None

    def get_pages_format(self) -> str:
        pagesFormat = self.soup.find("p", attrs={"data-testid": "pagesFormat"})
        if pagesFormat is None:
            return None

        return pagesFormat.string.strip() if pagesFormat.string else None

    def get_publication_info(self) -> str:
        publicationInfo = self.soup.find("p", attrs={"data-testid": "publicationInfo"})
        if publicationInfo is None:
            return None
        
        return publicationInfo.string.strip() if publicationInfo.string else None

    def get_description(self) -> str:
        descriptionDiv = self.soup.find("div", attrs={"data-testid": "description"})
        if descriptionDiv is None:
            logger.error("Failed to find descrpiption div!")
            return None

        description = descriptionDiv.find("span", class_="Formatted")
        if description is None:
            logger.error(f"Failed to find description span! {description}")
            return None

        if description.stripped_strings is not None:
            return " ".join(s for s in description.stripped_strings)
        else:
            return None

    def get_genres(self) -> list[str]:
        genreDiv = self.soup.find("div", attrs={"data-testid": "genresList"})
        if genreDiv is None:
            return None
        
        genres = genreDiv.find_all("span", class_="Button__labelItem")
        if genres is None:
            return None
        
        return [ genre.string for genre in genres if genre.string != '...more']

    def get_num_ratings(self) -> str:
        numRatings = self.soup.find("span", attrs={"data-testid": "ratingsCount"})
        if numRatings is None:
            return None

        return next(numRatings.stripped_strings)

    def get_num_reviews(self) -> str:
        numReviews = self.soup.find("span", attrs={"data-testid": "reviewsCount"})
        if numReviews is None:
            return None

        return next(numReviews.stripped_strings)

if __name__ == "__main__":
    #output = request_goodreads("justinbird")
    #f = open('justinbird.html', 'r')
    #profile = GRProfile('justinbird', input=f.read())
    #print(profile.get_pfp_url())
    #print(profile.get_profile_name())
    #print(profile.get_num_ratings())
    #print(profile.get_average_rating())

    #f = open('sara.html', 'r')
    #profile = GRProfile('sara', input=f.read())
    #print(profile.get_pfp_url())
    #print(profile.get_profile_name())
    #print(profile.get_num_ratings())
    #print(profile.get_average_rating())

    #f = open('secrethistory.html', 'r')
    #book = GRBook(None, f.read())
    book = GRBook('https://www.goodreads.com/book/show/166997.Stoner')
    print(book.get_cover_image())
    print(book.get_title())
    print(book.get_author())
    print(book.get_author_link())
    print(book.get_average_rating())
    print(book.get_num_ratings())
    print(book.get_num_reviews())
    print(book.get_pages_format())
    print(book.get_publication_info())
    print(book.get_description())
    print(book.get_genres())