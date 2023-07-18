#
# This code is part of Ansible, but is an independent component.
# This particular file snippet, and this file snippet only, is BSD licensed.
# Modules you write using this snippet, which is embedded dynamically by Ansible
# still belong to the author of the module, and may assign their own license
# to the complete work.
#
# Copyright (c), Michael DeHaan <michael.dehaan@gmail.com>, 2012-2013
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright notice,
#      this list of conditions and the following disclaimer in the documentation
#      and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from typing import List


def _get_quote_state(token: str, quote_char: str) -> str:
    '''
    the goal of this block is to determine if the quoted string
    is unterminated in which case it needs to be put back together
    '''
    prev_char = None
    for idx, cur_char in enumerate(token):
        if idx > 0:
            prev_char = token[idx - 1]
        if cur_char in '"\'' and prev_char != '\\':
            if quote_char:
                if cur_char == quote_char:
                    quote_char = None
            else:
                quote_char = cur_char
    return quote_char


def _count_jinja2_blocks(token: str, cur_depth: int, open_token: str, close_token: str) -> int:
    '''
    this function counts the number of opening/closing blocks for a
    given opening/closing type and adjusts the current depth for that
    block based on the difference
    '''
    num_open = token.count(open_token)
    num_close = token.count(close_token)
    if num_open != num_close:
        cur_depth += (num_open - num_close)
        if cur_depth < 0:
            cur_depth = 0
    return cur_depth


def split_args(args: str) -> List[str]:
    '''
    Splits args on whitespace, but intelligently reassembles
    those that may have been split over a jinja2 block or quotes.

    When used in a remote module, we won't ever have to be concerned about
    jinja2 blocks, however this function is/will be used in the
    core portions as well before the args are templated.

    example input: a=b c="foo bar"
    example output: ['a=b', 'c="foo bar"']

    Basically this is a variation shlex that has some more intelligence for
    how Ansible needs to use it.
    '''

    params = []

    args = args.strip()
    try:
        args = args.encode('utf-8')
        do_decode = True
    except UnicodeDecodeError:
        do_decode = False
    items = args.split('\n')

    quote_char = None
    inside_quotes = False
    print_depth = 0
    block_depth = 0
    comment_depth = 0

    for itemidx, item in enumerate(items):

        tokens = item.strip().split(' ')

        line_continuation = False
        for idx, token in enumerate(tokens):

            if token == '\\' and not inside_quotes:
                line_continuation = True
                continue

            was_inside_quotes = inside_quotes
            quote_char = _get_quote_state(token, quote_char)
            inside_quotes = quote_char is not None

            appended = False

            if inside_quotes and not was_inside_quotes:
                params.append(token)
                appended = True
            elif print_depth or block_depth or comment_depth or inside_quotes or was_inside_quotes:
                if idx == 0 and not inside_quotes and was_inside_quotes:
                    params[-1] = "%s%s" % (params[-1], token)
                elif len(tokens) > 1:
                    spacer = ''
                    if idx > 0:
                        spacer = ' '
                    params[-1] = "%s%s%s" % (params[-1], spacer, token)
                else:
                    spacer = ''
                    if not params[-1].endswith('\n') and idx == 0:
                        spacer = '\n'
                    params[-1] = "%s%s%s" % (params[-1], spacer, token)
                appended = True

            prev_print_depth = print_depth
            print_depth = _count_jinja2_blocks(token, print_depth, "{{", "}}")
            if print_depth != prev_print_depth and not appended:
                params.append(token)
                appended = True

            prev_block_depth = block_depth
            block_depth = _count_jinja2_blocks(token, block_depth, "{%", "%}")
            if block_depth != prev_block_depth and not appended:
                params.append(token)
                appended = True

            prev_comment_depth = comment_depth
            comment_depth = _count_jinja2_blocks(token, comment_depth, "{#", "#}")
            if comment_depth != prev_comment_depth and not appended:
                params.append(token)

            if not (print_depth or block_depth or comment_depth) and not inside_quotes and not appended and token != '':
                params.append(token)

        if len(items) > 1 and itemidx != len(items) - 1 and not line_continuation:
            if not params[-1].endswith('\n') or item == '':
                params[-1] += '\n'

        line_continuation = False

    if print_depth or block_depth or comment_depth or inside_quotes:
        raise Exception("error while splitting arguments, either an unbalanced jinja2 block or quotes")

    if do_decode:
        params = [x.decode('utf-8') for x in params]

    return params


def is_quoted(data: str) -> bool:
    return len(data) > 0 and (data[0] == '"' and data[-1] == '"' or data[0] == "'" and data[-1] == "'")


def unquote(data: str) -> str:
    if is_quoted(data):
        return data[1:-1]
    return data
