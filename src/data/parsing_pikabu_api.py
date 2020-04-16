import codecs
import re
import datetime
import string
from bs4 import BeautifulSoup


def open_html(file_name):
    """open html file by name"""
    file = codecs.open(file_name, "r", "utf-8")
    document = BeautifulSoup(file.read())
    return document


def clean(text_):
    """clear text from punctuation and indentation"""
    text_ = re.sub(r"^\s+|\n|\r|\t|\s+$", "", text_)
    table = str.maketrans({key: None for key in string.punctuation})
    text_ = text_.translate(table).lower()
    return text_


def text(page):
    """returns soup(page) article text"""
    try:
        text_ = page.find("div", {"class": "story__content-inner"}).text
        text_ = clean(text_)
        return text_
    except:
        return None


def title(page):
    """returns soup(page) title"""
    try:
        title_ = page.find("h2", {"class": "story__title"}).text
        title_ = clean(title_)
        return title_.lower()
    except:
        return None


def tags(page):
    """returns soup(page) tags"""
    try:
        text_ = page.find("div", {"class": "story__tags tags"}).text
        text_ = clean(text_)
        text_ = text_.split(" ")
        return text_
    except:
        return None


def amount_comments(page):
    """returns amount of soup(page) comments by users"""
    try:
        amount = page.find("span", {"class": "story__comments-link-count"}).text
        return amount
    except:
        return None


def rating(page):
    """returns soup(page) rating"""
    try:
        rat = page.find("div", {"class": "story__rating-count"}).text
        return rat
    except:
        return None


def author(page):
    """returns soup(page) author"""
    try:
        author_ = page.find("div", {"class": "user__info-item"}).text
        return author_
    except:
        return None


def link(page):
    """returns soup(page) link in web"""
    try:
        link_ = [item["href"] for item in page.select("h2 a")]
        return link_[0]
    except:
        return None


def article_id(page):
    """returns soup(page) article id"""
    try:
        id = [item["data-story-id"] for item in page.select("article")]
        return id[0]
    except:
        return None


def views(page):
    """returns soup(page) views by users"""
    try:
        view_ = page.find("div", {"class": "story__views hint"}).text
        view_ = re.sub(r"^\s+|\n|\r|\t|\s+$", "", view_)
        view_ = view_.split(" ")
        if str(view_[0])[-1] == "K":
            view_ = float(str(view_[0])[:-1:]) * 1000
        return int(view_)
    except:
        return None


def page_date(page):
    """returns soup(page) date creation"""
    try:
        date_ = [item["datetime"] for item in page.select("time")]
        date_ = str(date_[0])[:10]
        date_ = date_.split("-")
        d = datetime.date(int(date_[0]), int(date_[1]), int(date_[2]))
        return d
    except:
        return None
