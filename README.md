Trivial script to manage meeting note etherpad to wiki transitions.

Basic usage:

```sh
date=2014-04-01

thing() {
    wikimtgs -uTeamName -pRealStrongPassword \
             -Eteam-name-meetings -e'%(date)s' \
             -wTeamName/Meetings "$@"
}

# Creates a new etherpad at
# https://team-name-meetings.etherpad.mozilla.org/2014-04-01 and
# links to it from https://wiki.mozilla.org/TeamName/Meetings after
# the first line containing the string 'NEW_MEETING_MINUTES_ENTRIES'
# (sans quotes)
thing create $DATE

sleep 45m

# Copies the contents of the etherpad at
# https://team-name-meetings.etherpad.mozilla.org/2014-04-01
# to a new wiki page at
# https://wiki.mozilla.org/TeamName/Meetings/2014-01-01
# and replaces the appropriate etherpad link at
# https://wiki.mozilla.org/TeamName/Meetings with a link to the new
# wiki page.
thing archive $DATE
```

Requirements
------------
* curl
* pandoc
* mwclient
