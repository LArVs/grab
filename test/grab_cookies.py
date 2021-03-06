# coding: utf-8
from unittest import TestCase
#import string
import json

from grab import Grab, GrabMisuseError
from .util import TMP_FILE, GRAB_TRANSPORT
from .tornado_util import SERVER

class TestCookies(TestCase):
    def setUp(self):
        SERVER.reset()

    #def test_parsing_response_cookies(self):
        #g = Grab(transport=GRAB_TRANSPORT)
        #SERVER.RESPONSE['cookies'] = {'foo': 'bar', '1': '2'}
        #g.go(SERVER.BASE_URL)
        #self.assertEqual(g.response.cookies['foo'], 'bar')

    #def test_multiple_cookies(self):
        #g = Grab(transport=GRAB_TRANSPORT)
        #SERVER.RESPONSE['cookies'] = {}
        #g.setup(cookies={'foo': '1', 'bar': '2'})
        #g.go(SERVER.BASE_URL)
        #self.assertEqual(
            #set(map(lambda item: item.strip(),
                    #SERVER.REQUEST['headers']['Cookie'].split('; '))),
            #set(['foo=1', 'bar=2']))

    #def test_session(self):
        ## Test that if Grab gets some cookies from the server
        ## then it sends it back
        #g = Grab(transport=GRAB_TRANSPORT)
        #g.setup(reuse_cookies=True)
        #SERVER.RESPONSE['cookies'] = {'foo': 'bar'}
        #g.go(SERVER.BASE_URL)
        #self.assertEqual(g.response.cookies['foo'], 'bar')
        #g.go(SERVER.BASE_URL)
        #self.assertEqual(SERVER.REQUEST['headers']['Cookie'], 'foo=bar')
        #g.go(SERVER.BASE_URL)
        #self.assertEqual(SERVER.REQUEST['headers']['Cookie'], 'foo=bar')

        ## Test reuse_cookies=False
        #g = Grab(transport=GRAB_TRANSPORT)
        #g.setup(reuse_cookies=False)
        #SERVER.RESPONSE['cookies'] = {'foo': 'baz'}
        #g.go(SERVER.BASE_URL)
        #self.assertEqual(g.response.cookies['foo'], 'baz')
        #g.go(SERVER.BASE_URL)
        #self.assertTrue(len(SERVER.REQUEST['cookies']) == 0)

        ## Test something
        #g = Grab(transport=GRAB_TRANSPORT)
        #g.setup(reuse_cookies=True)
        #SERVER.RESPONSE['cookies'] = {'foo': 'bar'}
        #g.go(SERVER.BASE_URL)
        #self.assertEqual(g.response.cookies['foo'], 'bar')
        #g.clear_cookies()
        #g.go(SERVER.BASE_URL)
        #self.assertTrue(len(SERVER.REQUEST['cookies']) == 0)

    #def test_redirect_session(self):
        #g = Grab(transport=GRAB_TRANSPORT)
        #SERVER.RESPONSE['cookies'] = {'foo': 'bar'}
        #g.go(SERVER.BASE_URL)
        #self.assertEqual(g.response.cookies['foo'], 'bar')

        ## Setup one-time redirect
        #g = Grab(transport=GRAB_TRANSPORT)
        #SERVER.RESPONSE['cookies'] = {}
        #SERVER.RESPONSE_ONCE['headers'].append(('Location', SERVER.BASE_URL))
        #SERVER.RESPONSE_ONCE['headers'].append(('Set-Cookie', 'foo=bar'))
        #SERVER.RESPONSE_ONCE['code'] = 302
        #g.go(SERVER.BASE_URL)
        #self.assertEqual(SERVER.REQUEST['cookies']['foo'].value, 'bar')

    #def test_load_dump(self):
        #g = Grab(transport=GRAB_TRANSPORT)
        #cookies = {'foo': 'bar', 'spam': 'ham'}
        #g.setup(cookies=cookies)
        #g.go(SERVER.BASE_URL)
        #g.dump_cookies(TMP_FILE)
        #self.assertEqual(set(cookies.items()),
                         #set((x['name'], x['value']) for x in json.load(open(TMP_FILE))))

        ## Test non-ascii
        #g = Grab(transport=GRAB_TRANSPORT)
        #cookies = {'foo': 'bar', 'spam': u'бегемот'}
        #g.setup(cookies=cookies)
        #g.go(SERVER.BASE_URL)
        #g.dump_cookies(TMP_FILE)
        #self.assertEqual(set(cookies.items()),
                         #set((x['name'], x['value']) for x in json.load(open(TMP_FILE))))

        ## Test load cookies
        #g = Grab(transport=GRAB_TRANSPORT)
        #cookies = [{'name': 'foo', 'value': 'bar'},
                   #{'name': 'spam', 'value': u'бегемот'}]
        #json.dump(cookies, open(TMP_FILE, 'w'))
        #g.load_cookies(TMP_FILE)
        #self.assertEqual(set(g.cookies.items()),
                         #set((x['name'], x['value']) for x in cookies))

    #def test_cookiefile(self):
        #g = Grab(transport=GRAB_TRANSPORT)

        ## Empty file should not raise Exception
        #open(TMP_FILE, 'w').write('')
        #g.setup(cookiefile=TMP_FILE)
        #g.go(SERVER.BASE_URL)

        #cookies = [{'name': 'spam', 'value': 'ham'}]
        #json.dump(cookies, open(TMP_FILE, 'w'))

        ## One cookie are sent in server reponse
        ## Another cookies is passed via the `cookiefile` option
        #SERVER.RESPONSE['cookies'] = {'godzilla': 'monkey'}
        #g.setup(cookiefile=TMP_FILE)
        #g.go(SERVER.BASE_URL)
        #self.assertEqual(SERVER.REQUEST['cookies']['spam'].value, 'ham')

        ## This is correct reslt of combining two cookies
        #MERGED_COOKIES = [('godzilla', 'monkey'), ('spam', 'ham')]

        ## g.cookies should contains merged cookies
        #self.assertEqual(set(MERGED_COOKIES),
                         #set(g.cookies.items()))

        ## `cookiefile` file should contains merged cookies
        #self.assertEqual(set(MERGED_COOKIES),
                         #set((x['name'], x['value']) for x in json.load(open(TMP_FILE))))

    #def test_manual_dns(self):
        #import pycurl

        #g = Grab(transport=GRAB_TRANSPORT)
        #g.transport.curl.setopt(pycurl.RESOLVE, ('foo:80:127.0.0.1',))
        #SERVER.RESPONSE['get'] = 'zzz'
        #g.go('http://foo')
        #self.assertEqual('zzz', g.response.body)


    def test_different_domains(self):
        import pycurl

        g = Grab(transport=GRAB_TRANSPORT)
        names = [
            'foo:%d:127.0.0.1' % SERVER.PORT,
            'bar:%d:127.0.0.1' % SERVER.PORT,
        ]
        g.transport.curl.setopt(pycurl.RESOLVE, names)

        SERVER.RESPONSE['cookies'] = {'foo': 'foo'}
        g.go('http://foo:%d' % SERVER.PORT)
        self.assertEqual(dict(g.response.cookies.items()), {'foo': 'foo'})

        SERVER.RESPONSE['cookies'] = {'bar': 'bar'}
        g.go('http://bar:%d' % SERVER.PORT)
        self.assertEqual(dict(g.response.cookies.items()), {'bar': 'bar'})
