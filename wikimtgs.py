#!/usr/bin/env python2
from optparse import OptionParser
import sys

from wikimtgs import WikiMtgs

usage = 'usage: %prog -u<username> -p<password> [-E<team_etherpad_name>] -e<etherpad_name_template> -w<wiki_index_page> <command> <date>'

parser = OptionParser(usage=usage)
parser.add_option('-u', '--user',
                  dest='username', action='store',
                  help='Wiki site username')

parser.add_option('-p', '--password',
                  dest='password', action='store',
                  help='Wiki site password')

parser.add_option('-E', '--team-pad',
                  dest='team_pad', action='store',
                  default='',
                  help='Team etherpad name, e.g., <team-pad-name>.etherpad.mozilla.org')

parser.add_option('-e', '--etherpad',
                  dest='etherpad', action='store',
                  default='%(date)s',
                  help='Etherpad name template, e.g., "team-meeting-%(date)s"')

parser.add_option('-w', '--wiki-index',
                  dest='wiki_index', action='store',
                  help='Wiki index page, e.g., "FooTeam/Meetings"')


options, args = parser.parse_args(sys.argv[1:])

w = WikiMtgs(login=(options.username, options.password),
             index_page=options.wiki_index,
             etherpad_page=options.etherpad,
             etherpad_team=options.team_pad)

if args[0] == 'archive':
    w.archive(args[1])

elif args[0] == 'create':
    w.create(args[1])

# vim:se sts=4 sw=4 et:
