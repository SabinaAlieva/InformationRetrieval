from bs4 import BeautifulSoup
import codecs
import re
import datetime
import pandas as pd
import os
import string

def open_html(file_name):
    '''open html file by name'''
    f = codecs.open(file_name, 'r', 'utf-8')
    document = BeautifulSoup(f.read())
    return document


def clean(text):
    '''clear text from punctuation and indentation'''
    text = re.sub("^\s+|\n|\r|\t|\s+$", '', text)
    table = str.maketrans({key: None for key in string.punctuation})
    text = text.translate(table).lower()
    return text


def text(page):
    '''returns soup(page) article text'''
    try:
        t = page.find('div', {'class': 'story__content-inner'}).text
        t = clean(t)
        # t = t.split(" ")
        return t
    except:
        return None


def title(page):
    '''returns soup(page) title'''
    try:
        t = page.find('h2', {'class': 'story__title'}).text
        t = clean(t)
        return t.lower()
    except:
        return None


def tags(page):
    '''returns soup(page) tags'''
    try:
        text = page.find('div', {'class': 'story__tags tags'}).text
        # text = re.sub("^\s+|\n|\r|\s+$", '', text)
        text = clean(text)
        text = text.split(" ")
        # text = [str(t).lower() for t in text]
        return text
    except:
        return None


def amount_comments(page):
    '''returns amount of soup(page) comments by users'''
    try:
        t = page.find('span', {'class': 'story__comments-link-count'}).text
        return t
    except:
        return None


def rating(page):
    '''returns soup(page) rating'''
    try:
        t = page.find('div', {'class': 'story__rating-count'}).text
        return t
    except:
        return None


def author(page):
    '''returns soup(page) author'''
    try:
        t = page.find('div', {'class': 'user__info-item'}).text
        return t
    except:
        return None


def link(page):
    '''returns soup(page) link in web'''
    try:
        t = [item['href'] for item in page.select('h2 a')]
        return t[0]
    except:
        return None


def article_id(page):
    '''returns soup(page) article id'''
    try:
        t = [item['data-story-id'] for item in page.select('article')]
        return t[0]
    except:
        return None


def views(page):
    '''returns soup(page) views by users'''
    try:
        t = page.find('div', {'class': 'story__views hint'}).text
        t = re.sub("^\s+|\n|\r|\t|\s+$", '', t)
        t = t.split(" ")
        if (str(t[0])[-1] == 'K'):
            t = float(str(t[0])[:-1:]) * 1000
        return int(t)
    except:
        return None


def page_date(page):
    '''returns soup(page) date creation'''
    try:
        s = [item['datetime'] for item in page.select('time')]
        s = str(s[0])[:10]
        s = s.split("-")
        d = datetime.date(int(s[0]), int(s[1]), int(s[2]))
        return d
    except:
        return None
