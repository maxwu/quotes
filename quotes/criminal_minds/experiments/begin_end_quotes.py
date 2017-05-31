#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The experiment to fetch quotes

 .. moduleauthor:: Max Wu <http://maxwu.me>
 
 .. References::
    **Web Resource**, https://agoldoffish.wordpress.com/criminal-minds-opening-and-closing-quotes/
    **Tumblr Resource**, http://cmbookendquotes.tumblr.com/
"""

import requests
import bs4
import itertools
import re
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def split_to_episodes(iterable, is_splitter):
    """
    Split iterable into sub-lists with func is_splitter
    :param iterable:     The collection to operate on.
    :param is_splitter:  This func is to tell whether the current element is a splitter. 
                         Splitter itself will be dropped and never show up in sub-lists.
    :return:             A list of sub-lists, each sub-list has two elements:
                         The first one is the episode information line
                         The send element holds all the quotes mentioned by this episode.
    """
    sentences = [list(g) for k, g in itertools.groupby(iterable, is_splitter) if not k]
    episodes = [x for x in iterable if is_splitter(x)]
    return zip(episodes, sentences[1:])


class WPCMparser:
    """
    WPCMparser: WordPress Criminal Minds page parser
    
        # some episodes have no em tag
        # some has quotation marks.
        # *Notes*: special attention to unicode quotation marks.
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
    
    """
    quotes_page = 'https://agoldoffish.wordpress.com/criminal-minds-opening-and-closing-quotes/'

    def __init__(self):
        self.resp = requests.get(WPCMparser.quotes_page)
        self.quote_list = list()

    def parse(self):
        """
        Parse the response page content into python objects.
        :return: dict of quotes
        """
        soup = bs4.BeautifulSoup(self.resp.text, 'html.parser')
        paragraphs = soup.select('div.entry-content p')
        episodes = split_to_episodes(paragraphs, lambda x: x.span)

        for e in episodes:
            # e[0] for location information
            # fetch the current level string only
            location = e[0].span.stripped_strings.next()
            # fetch string "Season 7 Episode 13"
            season = location.split()[1]
            episode = location.split()[3]

            if e[0].span.em:
                title = e[0].span.em.string

            elif e[0].em:
                # if there is only one sub-tag under "em", .string works fine also.
                title = e[0].em.string
            else:
                title_contents = ''.join(e[0].strings)
                title = re.search(ur'[“”"](.+)[“”"]', title_contents, re.UNICODE).group(0)

            # print(u"Season: {}, Episode: {}, Title:{}".format(season, episode, title))

            # e[1] for quotes as a split list
            for q in e[1]:
                speaker = q.strong.string
                script = q.get_text().split(':')[1].strip()
                # print(u"\tSpeaker: {}\tscript: {}".format(speaker, script))
                quote = dict(speaker=speaker, quote=script, season=season, episode=episode, title=title)
                self.quote_list.append(quote)
            return self.quote_list

    def dump(self, path=None):
        if not self.quote_list:
            if not self.parse():
                return

        if not path:
            print(yaml.dump(self.quote_list))
            return

        stream = file(path, 'w')
        yaml.dump(self.quote_list, stream)

if __name__ == "__main__":
    WPCMparser().dump()
