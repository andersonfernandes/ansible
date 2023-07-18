from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import re
import sys
from typing import Dict, Union

from ansible import constants as C

ANSIBLE_COLOR: bool = True
if C.ANSIBLE_NOCOLOR:
    ANSIBLE_COLOR = False
elif not hasattr(sys.stdout, 'isatty') or not sys.stdout.isatty():
    ANSIBLE_COLOR = False
else:
    try:
        import curses
        curses.setupterm()
        if curses.tigetnum('colors') < 0:
            ANSIBLE_COLOR = False
    except ImportError:
        pass
    except curses.error:
        ANSIBLE_COLOR = False

if C.ANSIBLE_FORCE_COLOR:
    ANSIBLE_COLOR = True


def parsecolor(color: str) -> Union[str, int]:
    """SGR parameter string for the specified color name."""
    matches = re.match(
        r"color(?P<color>[0-9]+)"
        r"|(?P<rgb>rgb(?P<red>[0-5])(?P<green>[0-5])(?P<blue>[0-5]))"
        r"|gray(?P<gray>[0-9]+)", color
    )
    if not matches:
        return C.COLOR_CODES[color]
    if matches.group('color'):
        return u'38;5;%d' % int(matches.group('color'))
    if matches.group('rgb'):
        return u'38;5;%d' % (
            16 + 36 * int(matches.group('red')) +
            6 * int(matches.group('green')) +
            int(matches.group('blue'))
        )
    if matches.group('gray'):
        return u'38;5;%d' % (232 + int(matches.group('gray')))


def stringc(text: str, color: str, wrap_nonvisible_chars: bool = False) -> str:
    """String in color."""
    if ANSIBLE_COLOR:
        color_code = parsecolor(color)
        fmt = u"\033[%sm%s\033[0m"
        if wrap_nonvisible_chars:
            fmt = u"\001\033[%sm\002%s\001\033[0m\002"
        return u"\n".join([fmt % (color_code, t) for t in text.split(u'\n')])
    else:
        return text


def colorize(lead: str, num: int, color: str) -> str:
    """Print 'lead' = 'num' in 'color'"""
    s = u"%s=%-4s" % (lead, str(num))
    if num != 0 and ANSIBLE_COLOR and color is not None:
        s = stringc(s, color)
    return s


def hostcolor(host: str, stats: Dict[str, int], color: bool = True) -> str:
    if ANSIBLE_COLOR and color:
        if stats['failures'] != 0 or stats['unreachable'] != 0:
            return u"%-37s" % stringc(host, C.COLOR_ERROR)
        elif stats['changed'] != 0:
            return u"%-37s" % stringc(host, C.COLOR_CHANGED)
        else:
            return u"%-37s" % stringc(host, C.COLOR_OK)
    return u"%-26s" % host
