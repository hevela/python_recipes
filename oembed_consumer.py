# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup
from python_recipes import validate_url, get_url_domain

__author__ = 'velocidad'
from urllib2 import urlopen, URLError
from urlparse import urlsplit

# noinspection PyPackageRequirements

import oembed

FAILED_EXPECTATIONS = "One of the required parameters is not valid or is " \
                      "missing"

OEMBED_DATA_MISMATCH = "The returned oEmbed type is not the required type"

REMOTE_SERVER_ERROR = "The remote service has encountered an error"

OEMBED_ERRORS = {
    "failed_expectations": {
        "code": 2419,
        "message": FAILED_EXPECTATIONS,
        "type": "error"
    },
    "oembed_data_mismatch": {
        "code": 2420,
        "message": OEMBED_DATA_MISMATCH,
        "type": "error"
    },
    "remote_server_error": {
        "code": 2421,
        "message": REMOTE_SERVER_ERROR,
        "type": "error"
    }
}

IMAGE_EXT = ['jpg', 'png', 'jpeg', 'gif', 'bmp', 'svg']
VIDEO_EXT = ['mp4', 'ogg']
AUDIO_EXT = ['mp3', 'ogg', 'wav', 'aac', 'aiff']
PAGE_EXT = ['html', 'jsp', 'php', 'asp', 'aspx', 'htm', 'cgi', 'xhtml',
            'asx', 'do', 'jspx']

SHORT_URL_DOMAINS = [
    'tinyurl.com',
    'goo.gl',
    'bit.ly',
    't.co',
    'youtu.be',
    'vbly.us',
]

REGEX_PROVIDERS = [
    dict(hostname=('ifttt.com',),
         regex=['http://ifttt.com/recipes/*',
                'https://ifttt.com/recipes/*'],
         endpoint='http://www.ifttt.com/oembed/'),
    dict(hostname=('www.viddler.com',),
         regex=['http://www.viddler.com/v/*'],
         endpoint='http://www.viddler.com/oembed/'),
    dict(hostname=('www.jest.com',),
         regex=['http://www.jest.com/video/*',
                'http://www.jest.com/embed/*'],
         endpoint='http://www.jest.com/oembed.json'),
    dict(hostname=('deviantart.com',),
         regex=['http://*.deviantart.com/art/*',
                'http://*.deviantart.com/*#/d*',
                'http://deviantart.com/art/*',
                'http://deviantart.com/*#/d*',
                'http://fav.me/*',
                'http://sta.sh/*'],
         endpoint='http://backend.deviantart.com/oembed'),
    dict(hostname=('chirb.it',),
         regex=['http://chirb.it/*'],
         endpoint='http://chirb.it/oembed.json'),
    dict(hostname=('wordpress.com',),
         regex=['http://*.wordpress.com/*',
                'http://wordpress.com/*'],
         endpoint='http://public-api.wordpress.com/oembed/?for=me'),
    dict(hostname=('www.scribd.com',),
         regex=['http://www.scribd.com/doc/*'],
         endpoint='http://www.scribd.com/services/oembed/'),
    dict(hostname=('animoto.com',),
         regex=['http://animoto.com/play/*'],
         endpoint='http://animoto.com/oembeds/create/'),
    dict(hostname=('www.youtube.com',),
         regex=['http://youtube.com/watch*',
                'http://*.youtube.com/watch*',
                'https://youtube.com/watch*',
                'https://*.youtube.com/watch*',
                'http://youtube.com/v/*',
                'http://*.youtube.com/v/*',
                'https://youtube.com/v/*',
                'https://*.youtube.com/v/*',
                'http://youtu.be/*',
                'https://youtu.be/*',
                'http://youtube.com/user/*',
                'http://*.youtube.com/user/*',
                'https://youtube.com/user/*',
                'https://*.youtube.com/user/*',
                'http://youtube.com/*#*/*',
                'http://*.youtube.com/*#*/*',
                'https://youtube.com/*#*/*',
                'https://*.youtube.com/*#*/*',
                'http://m.youtube.com/index*',
                'https://m.youtube.com/index*',
                'http://youtube.com/profile*',
                'http://*.youtube.com/profile*',
                'https://youtube.com/profile*',
                'https://*.youtube.com/profile*',
                'http://youtube.com/view_play_list*',
                'http://*.youtube.com/view_play_list*',
                'https://youtube.com/view_play_list*',
                'https://*.youtube.com/view_play_list*',
                'http://youtube.com/playlist*',
                'http://*.youtube.com/playlist*',
                'https://youtube.com/playlist*',
                'https://*.youtube.com/playlist*'],
         endpoint='http://www.youtube.com/oembed'),
    dict(hostname=('www.flickr.com',),
         regex=['http://*.flickr.com/*',
                'http://flickr.com/*'],
         endpoint='http://www.flickr.com/services/oembed'),
    dict(hostname=('rdio.com',),
         regex=['http://*.rdio.com/artist/*',
                'http://*.rdio.com/people/*',
                'http://rdio.com/artist/*',
                'http://rdio.com/people/*'],
         endpoint='http://www.rdio.com/api/oembed/'),
    dict(hostname=('www.mixcloud.com',),
         regex=['http://www.mixcloud.com/*/*/'],
         endpoint='http://www.mixcloud.com/oembed/'),
    dict(hostname=('www.funnyordie.com',),
         regex=['http://www.funnyordie.com/videos/*'],
         endpoint='http://www.funnyordie.com/oembed.json/'),
    dict(hostname=('polldaddy.com',),
         regex=['http://polldaddy.com/s/*',
                'http://polldaddy.com/poll/*',
                'http://polldaddy.com/ratings/*',
                'http://*polldaddy.com/s/*',
                'http://*polldaddy.com/poll/*',
                'http://*polldaddy.com/ratings/*'],
         endpoint='http://polldaddy.com/oembed/'),
    dict(hostname=('ted.com',),
         regex=['http://ted.com/talks/*',
                'http://www.ted.com/talks/*',
                'https://ted.com/talks/*',
                'https://www.ted.com/talks/*',
                'http://ted.com/talks/lang/*/*',
                'http://www.ted.com/talks/lang/*/*',
                'https://ted.com/talks/lang/*/*',
                'https://www.ted.com/talks/lang/*/*',
                'http://ted.com/index.php/talks/*',
                'http://www.ted.com/index.php/talks/*',
                'https://ted.com/index.php/talks/*',
                'https://www.ted.com/index.php/talks/*',
                'http://ted.com/index.php/talks/lang/*/*',
                'http://www.ted.com/index.php/talks/lang/*/*',
                'https://ted.com/index.php/talks/lang/*/*',
                'https://www.ted.com/index.php/talks/lang/*/*'],
         endpoint='http://www.ted.com/talks/oembed.json'),
    dict(hostname=('www.videojug.com',),
         regex=['http://www.videojug.com/film/*',
                'http://www.videojug.com/interview/*'],
         endpoint='http://www.videojug.com/oembed.json/'),
    dict(hostname=('sapo.pt',),
         regex=['http://videos.sapo.pt/*'],
         endpoint='http://videos.sapo.pt/oembed'),
    dict(hostname=('justin.tv',),
         regex=['http://www.justin.tv/*'],
         endpoint='http://api.justin.tv/api/embed/from_url.json'),
    dict(hostname=('huffduffer.com',),
         regex=['http://huffduffer.com/*/*'],
         endpoint='http://huffduffer.com/oembed'),
    dict(hostname=('shoudio.com',),
         regex=['http://shoudio.com/*'],
         endpoint='http://shoudio.com/api/oembed'),
    dict(hostname=('www.mobypicture.com',),
         regex=['http://moby.to/*',
                'http://mobypicture.com/*'],
         endpoint='http://api.mobypicture.com/oEmbed'),
    dict(hostname=('cacoo.com',),
         regex=['http://cacoo.com/diagrams/*',
                'https://cacoo.com/diagrams/*'],
         endpoint='http://cacoo.com/oembed.json'),
    dict(hostname=('www.dipity.com',),
         regex=['http://www.dipity.com/*/*/'],
         endpoint='http://www.dipity.com/oembed/timeline/'),
    dict(hostname=('roomshare.jp',),
         regex=['http://roomshare.jp/post/*', 'http://roomshare.jp/en/post/*'],
         endpoint='http://roomshare.jp/en/oembed.json'),
    dict(hostname=('crowdranking.com',),
         regex=['http://crowdranking.com/*/*'],
         endpoint='http://crowdranking.com/api/oembed.json'),
    dict(hostname=('www.circuitlab.com',),
         regex=['https://www.circuitlab.com/circuit/*'],
         endpoint='https://www.circuitlab.com/circuit/oembed/'),
    dict(hostname=('geograph.org.uk', 'geograph.co.uk', 'geograph.ie'),
         regex=['http://*.geograph.org.uk/*',
                'http://*.geograph.co.uk/*',
                'http://*.geograph.ie/*'],
         endpoint='http://api.geograph.org.uk/api/oembed'),
    dict(hostname=('geo-en.hlipp.de', 'geo.hlipp.de', 'germany.geograph.org'),
         regex=['http://geo-en.hlipp.de/*',
                'http://geo.hlipp.de/*',
                'http://germany.geograph.org/*'],
         endpoint='http://geo.hlipp.de/restapi.php/api/oembed'),
    dict(hostname=('geograph.org.gg', 'geograph.org.je',
                   'channel-islands.geograph.org',
                   'channel-islands.geographs.org'),
         regex=['http://*.geograph.org.gg/*',
                'http://*.geograph.org.je/*',
                'http://channel-islands.geograph.org/*',
                'http://channel-islands.geographs.org/*',
                'http://*.channel.geographs.org/*'],
         endpoint='http://www.geograph.org.gg/api/oembed'),
    dict(hostname=('coub.com',),
         regex=['http://coub.com/view/*'],
         endpoint='http://coub.com/api/oembed.json/'),
    dict(hostname=('speakerdeck.com',),
         regex=['http://speakerdeck.com/*/*',
                'https://speakerdeck.com/*/*'],
         endpoint='https://speakerdeck.com/oembed.json'),
    dict(hostname=('app.net',),
         regex=['https://alpha.app.net/*/post/*',
                'https://photos.app.net/*/*'],
         endpoint='https://alpha-api.app.net/oembed'),
    dict(hostname=('yfrog.com',),
         regex=['http://yfrog.us/*',
                'http://*.yfrog.com/*',
                'http://yfrog.com/*'],
         endpoint='http://www.yfrog.com/api/oembed'),
    dict(hostname=('www.kickstarter.com',),
         regex=['http://www.kickstarter.com/projects/*'],
         endpoint='http://www.kickstarter.com/services/oembed'),
    dict(hostname=('ustream.tv', 'ustream.com'),
         regex=['http://*.ustream.tv/*',
                'http://*.ustream.com/*',
                'http://ustream.tv/*',
                'http://ustream.com/*'],
         endpoint='http://www.ustream.tv/oembed'),
    dict(hostname=('gmep.org',),
         regex=['https://gmep.org/media/*'],
         endpoint='https://gmep.org/oembed.json'),
    dict(hostname=('www.dailymile.com',),
         regex=['http://www.dailymile.com/people/*/entries/*'],
         endpoint='http://api.dailymile.com/oembed'),
    dict(hostname=('sketchfab.com',),
         regex=['http://sketchfab.com/show/*',
                'https://sketchfab.com/show/*'],
         endpoint='http://sketchfab.com/oembed'),
    dict(hostname=('meetup.com',),
         regex=['http://meetup.com/*',
                'http://meetu.ps/*',
                'http://*.meetup.com/*',
                'http://*.meetu.ps/*'],
         endpoint='https://api.meetup.com/oembed'),
    dict(hostname=('majorleaguegaming.com',),
         regex=['http://mlg.tv/*', 'http://tv.majorleaguegaming.com/*'],
         endpoint='http://tv.majorleaguegaming.com/oembed'),
    dict(hostname=('yandex.ru',),
         regex=['http://video.yandex.ru/users/*/view/*'],
         endpoint='http://video.yandex.ru/oembed.json'),
    dict(hostname=('revision3.com',),
         regex=['http://*revision3.com/*',
                'http://revision3.com/*'],
         endpoint='http://revision3.com/api/oembed/'),
    dict(hostname=('www.hulu.com',),
         regex=['http://www.hulu.com/watch/*'],
         endpoint='http://www.hulu.com/api/oembed.json'),
    dict(hostname=('vimeo.com',),
         regex=['http://vimeo.com/*',
                'http://www.vimeo.com/*',
                'https://vimeo.com/*',
                'https://www.vimeo.com/*',
                'http://player.vimeo.com/*',
                'https://player.vimeo.com/*'],
         endpoint='http://vimeo.com/api/oembed.json'),
    dict(hostname=('www.collegehumor.com',),
         regex=['http://www.collegehumor.com/video/*'],
         endpoint='http://www.collegehumor.com/oembed.json'),
    dict(hostname=('www.polleverywhere.com',),
         regex=['http://www.polleverywhere.com/polls/*',
                'http://www.polleverywhere.com/multiple_choice_polls/*',
                'http://www.polleverywhere.com/free_text_polls/*'],
         endpoint='http://www.polleverywhere.com/services/oembed/'),
    dict(hostname=('www.ifixit.com',),
         regex=['http://www.ifixit.com/*'],
         endpoint='http://www.ifixit.com/Embed'),
    dict(hostname=('smugmug.com', 'www.smugmug.com'),
         regex=['http://*.smugmug.com/*',
                'http://smugmug.com/*'],
         endpoint='http://api.smugmug.com/services/oembed/'),
    dict(hostname=('www.slideshare.net', 'fr.slideshare.net'),
         regex=['http://www.slideshare.net/*/*'],
         endpoint='http://www.slideshare.net/api/oembed/2'),
    dict(hostname=('www.23hq.com',),
         regex=['http://www.23hq.com/*/photo/*'],
         endpoint='http://www.23hq.com/23/oembed'),
    dict(hostname=('aol.com',),
         regex=['http://on.aol.com/video/*'],
         endpoint='http://on.aol.com/api'),
    dict(hostname=('twitter.com',),
         regex=['https://twitter.com/*/status*/*'],
         endpoint='https://api.twitter.com/1/statuses/oembed.json'),
    dict(hostname=('www.dailymotion.com',),
         regex=['http://www.dailymotion.com/video/*'],
         endpoint='http://www.dailymotion.com/services/oembed'),
    dict(hostname=('dotsub.com',),
         regex=['http://dotsub.com/view/*'],
         endpoint='http://dotsub.com/services/oembed'),
    dict(hostname=('blip.tv',),
         regex=['http://*.blip.tv/*',
                'http://blip.tv/*'],
         endpoint='http://blip.tv/oembed/'),
    dict(hostname=('official.fm',),
         regex=['http://official.fm/tracks/*',
                'http://official.fm/playlists/*'],
         endpoint='http://official.fm/services/oembed.json'),
    dict(hostname=('www.nfb.ca',),
         regex=['http://*.nfb.ca/film/*',
                'http://nfb.ca/film/*'],
         endpoint='http://www.nfb.ca/remote/services/oembed/'),
    dict(hostname=('instagr.am', 'instagram.com'),
         regex=['http://instagr.am/p/*', 'http://instagr.am/p/*',
                'http://instagram.com/p/'],
         endpoint='http://api.instagram.com/oembed'),
    dict(hostname=('wordpress.tv',),
         regex=['http://wordpress.tv/*'],
         endpoint='http://wordpress.tv/oembed/'),
    dict(hostname=('soundcloud.com', 'snd.sc'),
         regex=[
             'http://soundcloud.com/*', 'http://soundcloud.com/*/*',
             'http://soundcloud.com/*/sets/*', 'http://soundcloud.com/groups/*',
             'http://snd.sc/*', 'https://soundcloud.com/*'],
         endpoint='http://soundcloud.com/oembed'),
    dict(hostname=('www.screenr.com',),
         regex=['http://www.screenr.com/*', 'http://screenr.com/*'],
         endpoint='http://www.screenr.com/api/oembed.json')
]


class Consumer(object):
    def __init__(self):
        self.consumer = oembed.OEmbedConsumer()
        self.init_endpoints()

    def get_oembed(self, req_url, embed_type=""):
        """
        Takes an URL, queries the corresponding endpoint and return a tuple
        with the oembed data in a dict and a 200 code in case of a successful
        retrieval or a dict containing the error description and a 400 code

        @param req_url: The url to query
        @type req_url: str
        @param embed_type: the expected response type of the oEmbed
        @type embed_type: str
        @return: The oembed dict
        @rtype: dict
        """
        req_url = self.unshort_url(req_url)

        try:
            if "wordpress" in req_url:
                extra = {'for': 'me'}
                response = self.consumer.embed(req_url, opt=extra)
            else:
                response = self.consumer.embed(req_url)
        except oembed.OEmbedNoEndpoint:
            #No oembed provider

            #check if is a file url
            ext = req_url.split('.')
            #up to 4 letter ext
            ext = ext[-1].lower()
            if len(ext) < 5:
                _next = False
                if ext in AUDIO_EXT and embed_type == 'audio':
                    _next = True
                elif ext in VIDEO_EXT and embed_type == 'video':
                    _next = True
                elif ext in IMAGE_EXT and embed_type == 'photo':
                    _next = True
                elif embed_type == 'link' or embed_type == '':
                    _next = True
                    embed_type = 'link'

                if _next:
                    if ext in PAGE_EXT:
                        embed, code = self.crawl_page(req_url)
                        embed['type'] = embed_type
                        data = (self.validate_metadata(embed), code)
                    else:
                        #form json for file
                        data = self.json_for_link(req_url, embed_type)
                else:
                    data = (OEMBED_ERRORS['oembed_data_mismatch'], 400)

            else:
                if embed_type:
                    if embed_type != 'link':
                        data = (OEMBED_ERRORS['oembed_data_mismatch'], 400)
                        return data
                else:
                    embed_type = 'link'
                embed, code = self.crawl_page(req_url)
                embed['type'] = embed_type
                data = (self.validate_metadata(embed), code)
        else:
            embed = response.getData()
            if embed_type:
                if embed['type'] != embed_type:
                    data = (OEMBED_ERRORS['oembed_data_mismatch'], 400)
                    return data
            embed = self.validate_metadata(embed)
            data = (embed, 200)

        return data

    def init_endpoints(self):
        """
        Add all the endpoints to the OEmbedConsumer object
        """
        for provider in REGEX_PROVIDERS:
            endpoint_url = provider[u'endpoint']

            endpoint = oembed.OEmbedEndpoint(
                endpoint_url,
                provider[u'regex'])
            self.consumer.addEndpoint(endpoint)

    @staticmethod
    def unshort_url(geturl):
        """
        Open a shortened url and return the original url

        @param geturl: shortened url
        @type geturl: str
        @return: the unchortened url
        @rtype: str
        """
        host = urlsplit(geturl)[1]

        if host in SHORT_URL_DOMAINS:
            try:
                response = urlopen(geturl, )
                return response.url
            except URLError:
                pass

        return geturl

    def crawl_page(self, url):
        """
        Got to the url and tries to extract relevant data to form a response
        like oEmbed
        @param url: The url to extract info
        @type url: str
        @return: a tuple containing a dictionary with the basic oEmbed fields
        and a response code 200 for success, 400 for errors
        @rtype: tuple
        """
        req = urllib2.Request(url, headers={'User-Agent': "Magic Browser"})
        response = urllib2.urlopen(req)
        text = response.read()
        code = response.getcode()
        if 200 >= code < 400:
            soup = BeautifulSoup(text)
            title = soup.title.contents[0]
            try:
                subtitle = soup.h1.contents[0].text
            except AttributeError:
                subtitle = ""
            images = self.get_images(soup, url)
            description = self.get_description(soup)

            return dict(title=title, url=url, subtitle=subtitle, images=images,
                        description=description), 200

        else:
            return OEMBED_ERRORS['remote_server_error'], 400

    @staticmethod
    def get_images(soup, url):
        """ Takes a soup object and search for the relevant images in the
        document

        @param soup: A beautiful Soup HTML document object
        @type soup: BeautifulSoup
        @param url: the original url, used to form absolute links from
        relative urls
        @type url: str
        @return: a list of images
        @rtype: list
        """
        metas = [{'property': 'og:image'},
                 {'name': 'og:image'}]
        link = {'rel': 'image_src'}
        imgs = []

        for m_tag in metas:
            descr = soup.find_all('meta', attrs=m_tag)
            if descr:
                try:
                    descr_text = descr[0]['content']
                except IndexError:
                    continue
                else:
                    if not descr_text:
                        continue
                    else:
                        if descr_text.startswith('//'):
                            descr_text = descr_text.replace('//', 'http://')
                        imgs.append(descr_text)
        descr = soup.find_all('link', attrs=link)
        if descr:
            try:
                descr_text = descr[0]['href']
            except IndexError:
                pass
            else:
                if descr_text:
                    if descr_text.startswith('//'):
                            descr_text = descr_text.replace('//', 'http://')
                    imgs.append(descr_text)

        imgs_tags = soup.find_all('img')[:3]
        for img in imgs_tags:
            try:
                src = img['src']
            except KeyError:
                continue
            if not validate_url(src):
                if src[0] == '/':
                    src = get_url_domain(url) + src[1:]
                elif url[-1] == '/':
                    src = url + src
                else:
                    src = url + '/' + src
            if src.startswith('//'):
                src = src.replace('//', 'http://')
            imgs.append(src)
        return imgs

    def get_description(self, soup):
        """
        Takes a soup object and tries to extract the description of the page
        @param soup: a Beautiful Soup object
        @type soup: BeautifulSoup
        @return: the description of the page, if found
        @rtype: str
        """
        metas = [{'itemprop': 'description'},
                 {'name': 'description'},
                 {'property': 'og:description'},
                 {'name': 'og:description'}]
        for m_tag in metas:
            description = self.desc(m_tag, soup)
            if description:
                return description
        else:
            #No description found
            return ''

    @staticmethod
    def desc(meta, soup):
        """
        Search a soup object for a specific meta tag
        @param meta: the meta to search for
        @param soup: a Beautiful Soup object
        @type soup: BeautifulSoup
        @return:
        """
        descr = soup.find_all('meta', attrs=meta)
        if descr:
            try:
                descr_text = descr[0]['content']
            except IndexError:
                return False
            else:
                if not descr_text:
                    return False
                else:
                    return descr_text

    def json_for_link(self, url, _type):
        """
        forms a basic dict for a file url
        @param url: URL of a file
        @type url: str
        @param _type: file type
        @type _type: str
        @return: a tuple containing a dict and a response code
        @rtype: tuple
        """
        req = urllib2.Request(url, headers={'User-Agent': "Magic Browser"})
        response = urllib2.urlopen(req)
        text = response.read()
        code = response.getcode()
        if 200 >= code < 300 and text:
            title = url.split('/')[-1]
            response = dict(title=title, url=url, type=_type)
            if _type in ['photo', 'video']:
                response['width'] = 0
                response['height'] = 0
            return self.validate_metadata(response), 200
        else:
            return OEMBED_ERRORS['remote_server_error'], 400

    @staticmethod
    def validate_metadata(embed):
        """
        tries to standardize a oEmbed response, checks for fields named
        different, and adds requiered keys for a valid oEmbed response.
        If a key is not found, it's created with value 0, or empty.
        @param embed: a dictionary containing a oEmbed response,
        or similar response
        @return: a standarized oEmbed response
        """
        emb = embed.copy()
        if 'author_name' not in emb:
            emb['author_name'] = ''
        if 'title' not in emb:
            emb['title'] = ''
        if 'description' not in emb:
            if 'video_description' not in emb:
                emb['description'] = ''
            else:
                emb['description'] = emb['video_description']

        if 'thumbnail_url' not in emb:
            if 'thumbnail' not in emb:
                emb['thumbnail_url'] = ''
                emb['thumbnail_width'] = 0
                emb['thumbnail_height'] = 0
            else:
                emb['thumbnail_url'] = emb['thumbnail']
        if 'thumbnail_width' not in emb:
            emb['thumbnail_width'] = 0
        if 'thumbnail_height' not in emb:
            emb['thumbnail_height'] = 0
        emb['thumbnail_width'] = int(emb['thumbnail_width'])
        emb['thumbnail_height'] = int(emb['thumbnail_height'])

        if emb['thumbnail_url'].startswith('//'):
            emb['thumbnail_url'] = emb['thumbnail_url'].replace('//', 'http://')

        types_with_sizes = ['photo', 'video', 'rich']
        if emb['type'] in types_with_sizes:
            try:
                emb['width'] = int(emb['width'])
                emb['height'] = int(emb['height'])
            except ValueError:
                emb['width'] = 480
                emb['height'] = 270

        return emb


def test_this():
    consumer = Consumer()
    test_urls = [
        'https://ifttt.com/recipes/107745',
        'http://www.youtube.com/watch?v=-UUx10KOWIE',
        'http://flickr.com/photos/bees/2362225867/',
        'http://www.polleverywhere.com/multiple_choice_polls/LTIwNzM1NTczNTE',
        'http://www.viddler.com/v/1646c55',
        'http://revision3.com/diggnation/2008-04-17xsanned/',
        'http://www.hulu.com/watch/20807/late-night-with-conan-obrien-',
        'http://vimeo.com/7100569',
        'http://www.collegehumor.com/video/3922232/prank-war-7-the-half-million-dollar-shot',
        'http://www.jest.com/video/197394/paul-ryan-rap',
        'http://www.nfb.ca/film/aboriginality',
        'http://dotsub.com/view/665bd0d5-a9f4-4a07-9d9e-b31ba926ca78',
        'http://www.rdio.com/artist/The_Black_Keys/album/Brothers/',
        'http://www.ifixit.com/Teardown/iPhone-4-Teardown/3130/1',
        'http://www.smugmug.com/popular/all#125787395_hQSj9',
        'http://browse.deviantart.com/art/Vita-Brevis-379998342',
        'http://www.slideshare.net/haraldf/business-quotes-for-2011',
        'http://matt.wordpress.com/2011/07/14/clouds-over-new-york/',
        'http://chirb.it/OBnAr1',
        'http://animoto.com/play/JzwsBn5FRVxS0qoqcBP5zA',
        'http://www.mixcloud.com/TechnoLiveSets/jon_rundell-live-electrobeach-festival-benidorm-16-08-2013/',
        'http://screenr.com/3jns',
        'http://www.funnyordie.com/videos/a7311134ac/patton-oswalt-in-heavy-metal',
        'http://www.ted.com/talks/jill_bolte_taylor_s_powerful_stroke_of_insight.html',
        'http://www.videojug.com/film/how-to-tie-a-knot-braid',
        'http://videos.sapo.pt/dNbiosGa9YZHfLrhkA88',
        'http://www.justin.tv/deepellumonair',
        'http://official.fm/tracks/npTR',
        'http://huffduffer.com/jxpx777/125342',
        'http://shoudio.com/user/shoister/status/8122',
        'http://mobypicture.com/user/Henk_Voermans/view/15880044',
        'http://www.23hq.com/mprove/photo/13297717',
        'http://cacoo.com/diagrams/m9uZtizE5I2GkFR6/',
        'http://www.dipity.com/ragutier/Historia_de_la_Web/',
        'http://roomshare.jp/en/post/137167',
        'http://www.dailymotion.com/video/xoxulz_babysitter_animals',
        'http://crowdranking.com/rankings/t470g0--best-tea',
        'https://www.circuitlab.com/circuit/e38756/555-timer-as-astable-multivibrator-oscillator/',
        'http://s0.geograph.org.uk/geophotos/02/92/87/2928776_72cdbeab.jpg',
        'http://geo.hlipp.de/photos/02/02/020260_dcfdbf8e.jpg',
        'http://s1.channel.geographs.org/photos/00/07/000773_e1e23765_120x120.jpg',
        'https://speakerdeck.com/wallat/why-backbone',
        'https://alpha.app.net/breakingnews/post/9153521',
        'http://blip.tv/nostalgiacritic/nostalgia-critic-sailor-moon-6625851',
        'http://instagram.com/p/V8UMy0LjpX/',
        'https://soundcloud.com/devolverdigital/sets/hotline-miami-official',
        'http://on.aol.com/video/plans-to-clone-john-lennon-using-one-of-his-teeth-517906689',
        'http://www.kickstarter.com/projects/1115015686/help-support-the-kiggins-theatre-to-go-digital',
        'http://www.ustream.tv/channel/americatv2oficial',
        'https://gmep.org/media/14769',
        'http://www.dailymile.com/people/EddieJ3/entries/24776213',
        'https://sketchfab.com/show/b7LzIm8JrnPw4GBDOMBNGYc39qM',
        'http://www.meetup.com/PHPColMeetup/photos/',
        'http://video.yandex.ru/users/mumu-1/view/234/',
        'https://twitter.com/chuchoraw/status/440925264923471872',
        'http://wordpress.tv/2013/11/19/joe-dolson-accessibility-and-wordpress-developing-for-the-whole-world/'
    ]
    import pprint

    pp = pprint.PrettyPrinter(indent=4)
    for url in test_urls:
        print "\n________________________________"
        print url
        print "\n"
        embed = consumer.get_oembed(url)
        pp.pprint(embed)


if __name__ == "__main__":
    test_this()