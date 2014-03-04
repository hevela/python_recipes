__author__ = 'velocidad'
from urllib2 import urlopen, URLError
from urlparse import urlsplit

# noinspection PyPackageRequirements
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
    dict(hostname=('ifttt.com',),
         regex=['http://ifttt.com/recipes/*'],
         endpoint='http://www.ifttt.com/oembed/'),
    dict(hostname=('www.viddler.com',),
         regex=['http://www.viddler.com/v/*'],
         endpoint='http://www.viddler.com/oembed/'),
    dict(hostname=('www.jest.com',),
         regex=['http://www.jest.com/video/*',
                'http://www.jest.com/embed/*'],
         endpoint='http://www.jest.com/oembed.%s'),
    dict(hostname=('deviantart.com',),
         regex=['http://*.deviantart.com/art/*',
                'http://*.deviantart.com/*#/d*',
                'http://fav.me/*',
                'http://sta.sh/*'],
         endpoint='http://backend.deviantart.com/oembed?format=%s'),
    dict(hostname=('chirb.it',),
         regex=['http://chirb.it/*'],
         endpoint='http://chirb.it/oembed.%s'),
    dict(hostname=('wordpress.com',),
         regex=['http://*.wordpress.com/*'],
         endpoint='http://public-api.wordpress.com/oembed/?format=.%s'),
    dict(hostname=('www.scribd.com',),
         regex=['http://www.scribd.com/doc/*'],
         endpoint='http://www.scribd.com/services/oembed/?format=%s'),
    dict(hostname=('animoto.com',),
         regex=['http://animoto.com/play/*'],
         endpoint='http://animoto.com/oembeds/create/?format=%s'),
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
         regex=['http://*.flickr.com/*'],
         endpoint='http://www.flickr.com/services/oembed'),
    dict(hostname=('rdio.com',),
         regex=['http://*.rdio.com/artist/*',
                'http://*.rdio.com/people/*'],
         endpoint='http://www.rdio.com/api/oembed/?format=%s'),
    dict(hostname=('www.mixcloud.com',),
         regex=['http://www.mixcloud.com/*/*/'],
         endpoint='http://www.mixcloud.com/oembed/?format=%s'),
    dict(hostname=('www.funnyordie.com',),
         regex=['http://www.funnyordie.com/videos/*'],
         endpoint='http://www.funnyordie.com/oembed.%s/'),
    dict(hostname=('polldaddy.com',),
         regex=['http://*.polldaddy.com/s/*',
                'http://*.polldaddy.com/poll/*',
                'http://*.polldaddy.com/ratings/*'],
         endpoint='http://polldaddy.com/oembed/?format=%s'),
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
         endpoint='http://www.ted.com/talks/oembed.%s'),
    dict(hostname=('www.videojug.com',),
         regex=['http://www.videojug.com/film/*',
                'http://www.videojug.com/interview/*'],
         endpoint='http://www.videojug.com/oembed.%s/'),
    dict(hostname=('sapo.pt',),
         regex=['http://videos.sapo.pt/*'],
         endpoint='http://videos.sapo.pt/oembed?format=%s'),
    dict(hostname=('justin.tv',),
         regex=['http://www.justin.tv/*'],
         endpoint='http://api.justin.tv/api/embed/from_url.%s'),
    dict(hostname=('huffduffer.com',),
         regex=['http://huffduffer.com/*/*'],
         endpoint='http://huffduffer.com/oembed'),
    dict(hostname=('shoudio.com',),
         regex=['http://shoudio.com/*'],
         endpoint='http://shoudio.com/api/oembed'),
    dict(hostname=('www.mobypicture.com',),
         regex=['http://moby.to/*'],
         endpoint='http://api.mobypicture.com/oEmbed'),
    dict(hostname=('urtak.com',),
         regex=['http://urtak.com/u/*',
                'http://urtak.com/clr/*'],
         endpoint='http://oembed.urtak.com/1/oembed'),
    dict(hostname=('cacoo.com',),
         regex=['https://cacoo.com/diagrams/*'],
         endpoint='http://cacoo.com/oembed.%s'),
    dict(hostname=('www.dipity.com',),
         regex=['http://www.dipity.com/*/*/'],
         endpoint='http://www.dipity.com/oembed/timeline/'),
    dict(hostname=('roomshare.jp',),
         regex=['http://roomshare.jp/post/*', 'http://roomshare.jp/en/post/*'],
         endpoint='http://roomshare.jp/en/oembed.%s'),
    dict(hostname=('crowdranking.com',),
         regex=['http://crowdranking.com/*/*'],
         endpoint='http://crowdranking.com/api/oembed.%s'),
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
    dict(hostname=('www.quiz.biz',),
         regex=['http://www.quiz.biz/quizz-*.html'],
         endpoint='http://www.quiz.biz/api/oembed'),
    dict(hostname=('coub.com',),
         regex=['http://coub.com/view/*'],
         endpoint='http://coub.com/api/oembed.%s/'),
    dict(hostname=('speakerdeck.com',),
         regex=['http://speakerdeck.com/*/*',
                'https://speakerdeck.com/*/*'],
         endpoint='https://speakerdeck.com/oembed.json'),
    dict(hostname=('app.net',),
         regex=['https://alpha.app.net/*/post/*',
                'https://photos.app.net/*/*'],
         endpoint='https://alpha-api.app.net/oembed'),
    dict(hostname=('yfrog.com',),
         regex=['http://yfrog.us/*', 'http://*.yfrog.com/*'],
         endpoint='http://www.yfrog.com/api/oembed'),
    dict(hostname=('www.kickstarter.com',),
         regex=['http://www.kickstarter.com/projects/*'],
         endpoint='http://www.kickstarter.com/services/oembed'),
    dict(hostname=('ustream.tv', 'ustream.com'),
         regex=['http://*.ustream.tv/*', 'http://*.ustream.com/*'],
         endpoint='http://www.ustream.tv/oembed'),
    dict(hostname=('gmep.org',),
         regex=['https://gmep.org/media/*'],
         endpoint='https://gmep.org/oembed.%s'),
    dict(hostname=('www.dailymile.com',),
         regex=['http://www.dailymile.com/people/*/entries/*'],
         endpoint='https://gmep.org/oembed.%s'),
    dict(hostname=('sketchfab.com',),
         regex=['http://sketchfab.com/show/*',
                'https://sketchfab.com/show/*'],
         endpoint='http://sketchfab.com/oembed'),
    dict(hostname=('meetup.com',),
         regex=['http://meetup.com/*', 'http://meetu.ps/*'],
         endpoint='https://api.meetup.com/oembed'),
    dict(hostname=('majorleaguegaming.com',),
         regex=['http://mlg.tv/*', 'http://tv.majorleaguegaming.com/*'],
         endpoint='http://tv.majorleaguegaming.com/oembed'),
    dict(hostname=('github.com',),
         regex=['http://gist.github.com/*',
                'https://gist.github.com/*'],
         endpoint='https://github.com/api/oembed'),
    dict(hostname=('dipdive.com',),
         regex=['http://*.dipdive.com/media/*'],
         endpoint='http://api.dipdive.com/oembed.%s'),
    dict(hostname=('yandex.ru',),
         regex=['http://video.yandex.ru/users/*/view/*'],
         endpoint='http://video.yandex.ru/oembed.%s'),
    dict(hostname=('bambuser.com',),
         regex=['http://bambuser.com/chanel/*/broadcast/*',
                'http://bambuser.com/chanel/*',
                'http://bambuser.com/v/*'],
         endpoint='http://api.dipdive.com/oembed.%s'),
    dict(hostname=('skitch.com',),
         regex=['http://skitch.com/*',
                'http://www.skitch.com/*',
                'https://skitch.com/*',
                'https://www.skitch.com/*',
                'http://skit.ch/*'],
         endpoint='http://skitch.com/oembed'),
    dict(hostname=('qik.com',),
         regex=['http://qik.com/video/*', 'http://qik.com/*'],
         endpoint='http://qik.com/api/oembed.%s'),
    dict(hostname=('revision3.com',),
         regex=['http://*revision3.com/*'],
         endpoint='http://revision3.com/api/oembed/'),
    dict(hostname=('www.hulu.com',),
         regex=['http://www.hulu.com/watch/*'],
         endpoint='http://www.hulu.com/api/oembed.%s'),
    dict(hostname=('vimeo.com',),
         regex=['http://vimeo.com/*',
                'http://www.vimeo.com/*',
                'https://vimeo.com/*',
                'https://www.vimeo.com/*',
                'http://player.vimeo.com/*',
                'https://player.vimeo.com/*'],
         endpoint='http://vimeo.com/api/oembed.%s'),
    dict(hostname=('www.collegehumor.com',),
         regex=['http://www.collegehumor.com/video/*'],
         endpoint='http://www.collegehumor.com/oembed.%s'),
    dict(hostname=('www.polleverywhere.com',),
         regex=['http://www.polleverywhere.com/polls/*',
                'http://www.polleverywhere.com/multiple_choice_polls/*',
                'http://www.polleverywhere.com/free_text_polls/*'],
         endpoint='http://www.polleverywhere.com/services/oembed/'),
    dict(hostname=('www.ifixit.com',),
         regex=['http://www.ifixit.com/*'],
         endpoint='http://www.ifixit.com/Embed'),
    dict(hostname=('smugmug.com', 'www.smugmug.com'),
         regex=['http://*.smugmug.com/*'],
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
    dict(hostname=('dotsub.com',),
         regex=['http://dotsub.com/view/*'],
         endpoint='http://dotsub.com/services/oembed'),
    dict(hostname=('blip.tv',),
         regex=['http://*blip.tv/*'],
         endpoint='http://blip.tv/oembed/'),
    dict(hostname=('official.fm',),
         regex=['http://official.fm/tracks/*',
                'http://official.fm/playlists/*'],
         endpoint='http://official.fm/services/oembed.%s'),
    dict(hostname=('vhx.tv',),
         regex=['http://vhx.tv/*'],
         endpoint='http://vhx.tv/services/oembed.%s'),
    dict(hostname=('www.nfb.ca',),
         regex=['http://*.nfb.ca/film/*'],
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
         endpoint='http://www.screenr.com/api/oembed.%s'),
]


class Consumer():
    def __init__(self, req_format="json"):
        self.format = req_format
        self.consumer = oembed.OEmbedConsumer()
        self.init_endpoints()

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

    def init_endpoints(self):
        """
        Add all the endpoints to the OEmbedConsumer object
        """
        for provider in REGEX_PROVIDERS:
            try:
                endpoint_url = provider[u'endpoint'] % self.format
            except TypeError:
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