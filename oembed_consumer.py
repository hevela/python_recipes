__author__ = 'velocidad'
from urllib2 import urlopen, URLError
from urlparse import urlsplit

import oembed

SHORT_URL_DOMAINS = [
    'tinyurl.com',
    'goo.gl',
    'bit.ly',
    't.co',
    'youtu.be',
    'vbly.us',
]

REGEX_PROVIDERS = [
    dict(hostname=('www.youtube.com',), regex=[
        'regex:.*youtube\.com/watch.*',
        'regex:.*youtube\.com/playlist.*'
    ], endpoint='http://www.youtube.com/oembed'),
    dict(hostname=('www.flickr.com',), regex=['http://*.flickr.com/*'],
         endpoint='http://www.flickr.com/services/oembed'),
    dict(hostname=('qik.com',),
         regex=['http://qik.com/video/*', 'http://qik.com/*'],
         endpoint='http://qik.com/api/oembed.%s'),
    dict(hostname=('revision3.com',), regex=['http://*revision3.com/*'],
         endpoint='http://revision3.com/api/oembed/'),
    dict(hostname=('www.hulu.com',), regex=['http://www.hulu.com/watch/*'],
         endpoint='http://www.hulu.com/api/oembed.%s'),
    dict(hostname=('vimeo.com',),
         regex=['http://vimeo.com/*', 'https://vimeo.com/*'],
         endpoint='http://vimeo.com/api/oembed.%s'),
    dict(hostname=('www.collegehumor.com',),
         regex=['http://www.collegehumor.com/video/*'],
         endpoint='http://www.collegehumor.com/oembed.%s'),
    dict(hostname=('www.polleverywhere.com',),
         regex=['http://www.polleverywhere.com/polls/*',
                'http://www.polleverywhere.com/multiple_choice_polls/*',
                'http://www.polleverywhere.com/free_text_polls/*'],
         endpoint='http://www.polleverywhere.com/services/oembed/'),
    dict(hostname=('www.ifixit.com',), regex=['http://www.ifixit.com/*'],
         endpoint='http://www.ifixit.com/Embed'),
    dict(hostname=('smugmug.com', 'www.smugmug.com'),
         regex=['http://*.smugmug.com/*'],
         endpoint='http://api.smugmug.com/services/oembed/'),
    dict(hostname=('www.slideshare.net', 'fr.slideshare.net'),
         regex=['http://www.slideshare.net/*/*'],
         endpoint='http://www.slideshare.net/api/oembed/2'),
    dict(hostname=('www.23hq.com',), regex=['http://www.23hq.com/*/photo/*'],
         endpoint='http://www.23hq.com/23/oembed'),
    dict(hostname=('www.5min.com',), regex=['http://www.5min.com/Video/*'],
         endpoint='http://api.5min.com/oembed.%s'),
    dict(hostname=('twitter.com',), regex=['https://twitter.com/*/status*/*'],
         endpoint='https://api.twitter.com/1/statuses/oembed.%s'),
    dict(hostname=('photobucket.com', 'img.photobucket.com'),
         regex=['regex:.*photobucket\\.com/(albums|groups)/.+$'],
         endpoint='http://photobucket.com/oembed'),
    dict(hostname=('www.dailymotion.com',),
         regex=['http://www.dailymotion.com/video/*'],
         endpoint='http://www.dailymotion.com/services/oembed'),
    dict(hostname=('clikthrough.com', 'www.clikthrough.com'),
         regex=['http://*.clikthrough.com/theater/video/*'],
         endpoint='http://clikthrough.com/services/oembed'),
    dict(hostname=('dotsub.com',), regex=['http://dotsub.com/view/*'],
         endpoint='http://dotsub.com/services/oembed'),
    dict(hostname=('blip.tv',), regex=['http://*blip.tv/*'],
         endpoint='http://blip.tv/oembed/'),
    dict(hostname=('official.fm',), regex=[
        'http://official.fm/tracks/*',
        'http://official.fm/playlists/*'
    ], endpoint='http://official.fm/services/oembed.%s'),
    dict(hostname=('vhx.tv',), regex=['http://vhx.tv/*'],
         endpoint='http://vhx.tv/services/oembed.%s'),
    dict(hostname=('www.nfb.ca',), regex=['http://*.nfb.ca/film/*'],
         endpoint='http://www.nfb.ca/remote/services/oembed/'),
    dict(hostname=('instagr.am', 'instagram.com'),
         regex=['http://instagr.am/p/*', 'http://instagr.am/p/*',
                'http://instagram.com/p/'],
         endpoint='http://api.instagram.com/oembed'),
    dict(hostname=('wordpress.tv',), regex=['http://wordpress.tv/*'],
         endpoint='http://wordpress.tv/oembed/'),
    dict(hostname=('soundcloud.com', 'snd.sc'), regex=[
        'http://soundcloud.com/*', 'http://soundcloud.com/*/*',
        'http://soundcloud.com/*/sets/*', 'http://soundcloud.com/groups/*',
        'http://snd.sc/*', 'https://soundcloud.com/*'
    ], endpoint='http://soundcloud.com/oembed'),
    dict(hostname=('www.screenr.com',),
         regex=['http://www.screenr.com/*', 'http://screenr.com/*'],
         endpoint='http://www.screenr.com/api/oembed.%s'),
]


class Consumer():
    def __init__(self, req_format="json"):
        self.format = req_format
        self.consumer = oembed.OEmbedConsumer()
        self.init_endpoints(self.consumer, self.format)

    def get_oembed(self, req_url):
        """
        Takes an URL, queries the corresponding endpoint and return a dict
        with the oembed data

        @param req_url: The url to query
        @type req_url: str
        @return: The oembed dict
        @rtype: dict
        """
        req_url = self.unshort_url(req_url)
        response = self.consumer.embed(req_url)
        return response.getData()

    @staticmethod
    def init_endpoints(selfconsumer, req_format):
        """
        Add all the endpoints to the OEmbedConsumer object

        @param selfconsumer: the OEmbedConsumer object
        @type selfconsumer: object
        @param req_format: request format, currently only JSON
        @type req_format: str
        """
        for provider in REGEX_PROVIDERS:
            try:
                endpoint_url = provider[u'endpoint'] % req_format
            except TypeError:
                endpoint_url = provider[u'endpoint']

            endpoint = oembed.OEmbedEndpoint(
                endpoint_url,
                provider[u'regex'])
            selfconsumer.addEndpoint(endpoint)

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

if __name__ == "__main__":
    consumer = Consumer()
    test_urls = [
        'https://www.youtube.com/watch?v=KdWUZ_49-Ck',
        'https://www.youtube.com/watch?v=V_ho5Y-Yw8g',
        'http://www.flickr.com/photos/hsf6525/12222676506/in/explore-2014-01-30',
        'http://www.flickr.com/photos/hsf6525/11859492884/in/photostream/',
        'http://instagram.com/p/jztoJ7hoRM/',
        'http://instagram.com/p/j2E_SloqDA/',
        'http://www.dailymotion.com/video/x1amn6h_mega-resena-mega-man-10_videogames',
        'http://www.dailymotion.com/video/x1a92ug_video-resena-robocop-arcadia-nes-pc_videogames',
        'https://twitter.com/Kotaku/status/429336310625869824',
        'https://twitter.com/PlayStation/status/429336310856560640',
        'https://soundcloud.com/devolverdigital/sets/hotline-miami-official'
    ]
    for url in test_urls:
        print "\n________________________________"
        print url
        print "\n________________________________"
        embed = consumer.get_oembed(url)
        print embed, "\n\n=================================\n\n"