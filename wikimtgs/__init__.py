import re
import subprocess

import mwclient
import requests

class WikiMtgs(object):
    SITE = {
        'host': ('https', 'wiki.mozilla.org'),
        'path': '/',
    }

    INDEX_START        = 'NEW_MEETING_MINUTES_ENTRIES'
    ETHERPAD_SITE      = 'https://%(subpad)setherpad.mozilla.org'
    ETHERPAD_CREATE    = ETHERPAD_SITE + '/ep/pad/create'

    @property
    def etherpad_export(self):
        return '%s/ep/pad/export/%s/latest?format=html' % (self.ETHERPAD_SITE,
                                                           self.etherpad_page)

    @property
    def etherpad_template(self):
        return '%s/%s' % (self.ETHERPAD_SITE, self.etherpad_page)

    @property
    def archive_template(self):
        return self.index_page + '/%(date)s'


    def __init__(self, login, index_page, etherpad_page, etherpad_team=''):
        self.etherpad_page = etherpad_page
        self.index_page = index_page
        self.login = login
        self.subpad = etherpad_team

    def params(self, date=None):
        return {
            'date': date,
            'subpad': '%s.' % self.subpad if self.subpad else ''
        }

    def connect(self):
        site = mwclient.Site(**self.SITE)
        site.login(*self.login)
        return site

    def archive(self, date):
        site = self.connect()

        params = self.params(date=date)

        etherpad = self.etherpad_template % params
        export   = self.etherpad_export   % params
        archive  = self.archive_template  % params

        text = call('pandoc', '-fhtml', '-tmediawiki',
                    input=requests.get(export).text.encode('utf-8'))

        site.pages[archive].save(
            summary='Archiving meeting notes from %s to wiki' % etherpad,
            text=text)
        
        page = site.Pages[self.index_page]

        page.save(summary='Archive notes for %s' % date,
                  text=page.edit().replace(etherpad,
                                           '[[%s]]' % archive))

    def create(self, date):
        site = self.connect()

        params = self.params(date=date)

        etherpad = self.etherpad_template % params
        create   = self.ETHERPAD_CREATE % params

        if False:
            # Grr. Etherpad. This does not work as expected. I
            # suspect it's because `requests` attempts to use
            # HTTP/1.1
            requests.post(create,
                          data=dict(padId=date))
        else:
            call('curl', '-LsdpadId=%s' % date, create)

        page = site.Pages[self.index_page]

        text = re.sub(self.INDEX_START + r'.*\n',
                      lambda r: r.group(0) + '* %s\n' % etherpad,
                      page.edit())

        page.save(summary='Adding notes pad for %s' % date,
                  text=text)

def call(*args, **kwargs):
    import os
    import signal

    background = kwargs.pop('background', False)
    stdin = subprocess.PIPE if not background else open('/dev/null', 'r')
    pipe  = subprocess.PIPE if not background else None
    input = kwargs.pop('input', None)
    p = subprocess.Popen(args, stdin=stdin, stdout=pipe, stderr=pipe,
                         preexec_fn=lambda: signal.signal(signal.SIGPIPE, signal.SIG_DFL),
                         cwd=os.environ['HOME'], close_fds=True, **kwargs)
    if not background:
        return p.communicate(input)[0].rstrip('\n')
