
import requests
from lxml import html

from naotomori.cogs.source.source import Source


class _9Anime:
    """
    _9Anime: provides a minimal 9anime api.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.url = 'https://www8.9anime.ru/home'

    def __str__(self):
        """
        String representation.

        :return: Name of source/api.
        """
        return "9anime"

    def _findAnimeElements(self, tree):
        """
        Find all the anime elements in a html string.

        :param tree: The html string in form of a tree.
        :return: All the anime elements.
        """
        return tree.xpath("//div[contains(concat(' ', normalize-space(@class), ' '), ' content ')\
                                            and not(contains(concat(' ', @class, ' '), ' hidden '))]/*[1]/*[1]/*")

    def getRecent(self):
        """
        Get all the most recent anime chapters.

        :return: List of all the recent anime (Source objects) with the most recent ones at the front of the list.
        """
        animes = []

        # Get all the anime html elements from the 9anime homepage
        animeElements = []
        with requests.Session() as session:
            session.headers = {'User-Agent': 'Mozilla/5.0'}
            response = session.get(self.url)
            if response.status_code == 200:
                tree = html.fromstring(response.text)
                # Get all the recent anime's
                animeElements = self._findAnimeElements(tree)

        # Construct the Anime objects
        for animeElement in animeElements:
            # Get the title
            query = animeElement.xpath(
                "*[1]/a[contains(concat(' ', normalize-space(@class), ' '), ' name ')]/@data-jtitle")
            title = query[0] if len(query) > 0 else None
            query = animeElement.xpath(".//div[contains(concat(' ', normalize-space(@class), ' '), ' ep ')]")
            ep = query[0].text_content() if len(query) > 0 else None
            if title:
                link = animeElement.xpath("*[1]/a[contains(concat(' ', normalize-space(@class), ' '), ' name ')]/@href")[0]
                if link.startswith('/'):
                    # Relative path => prepend base url
                    link = self.url + link
                animes.append(Source(title=title, progress=ep, link=link))

        return animes   # should be <= 16
