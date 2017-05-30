#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The experiment to fetch quotes

 .. moduleauthor:: Max Wu <http://maxwu.me>
 
 .. References::
    **Web Resource**, https://agoldoffish.wordpress.com/criminal-minds-opening-and-closing-quotes/
"""

import requests
import bs4
import itertools
import pprint


def split_to_episodes(iterable, is_splitter):
    sentences = [list(g) for k, g in itertools.groupby(iterable, is_splitter) if not k]
    episodes = [x for x in iterable if is_splitter(x)]
    return zip(episodes, sentences[1:])

class WPCMparser:
    """
    WPCMparser: WordPress Criminal Minds page parser
    """
    quotes_page = 'https://agoldoffish.wordpress.com/criminal-minds-opening-and-closing-quotes/'

    def __init__(self):
        self.resp = requests.get(WPCMparser.quotes_page)

    def parse(self):
        soup = bs4.BeautifulSoup(self.resp.text, 'html.parser')
        paragraphs = soup.select('div.entry-content p')
        episodes = split_to_episodes(paragraphs, lambda x: x.span)
        for e in episodes:
            location = e[0].span.stripped_strings.next()
            title = e[0].span.em.string
            # some episodes have no em tag
            # some has quotation marks.
            '''
            148 = {Tag} <p><span style="text-decoration:underline;">Season 7 Episode 13 </span><em><span style="text-decoration:underline;">Snake Eyes</span></em></p>
            149 = {Tag} <p><span style="text-decoration:underline;">Season 7 Episode 14 “Closing Time”</span></p>
            150 = {Tag} <p><span style="text-decoration:underline;">Season 7 Episode 15 “A Thin Line”</span></p>
            151 = {Tag} <p><span style="text-decoration:underline;">Season 7 Episode 16 “A Family Affair”</span></p>
            152 = {Tag} <p><span style="text-decoration:underline;">Season 7 Episode 17 “I Love You, Tommy Brown”</span></p>
            153 = {Tag} <p><span style="text-decoration:underline;">Season 7 Episode 18 “Foundation”</span></p>
            154 = {Tag} <p><span style="text-decoration:underline;">Season 7 Episode 19 “Heathridge Manor”</span></p>
            '''
            # some sentences are none.
            print(u"Location: {}, Title:{}".format(location, title))
            print e[1]
        pass

if __name__ == "__main__":
    WPCMparser().parse()