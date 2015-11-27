#!/usr/bin/env python

import sys
from argparse import ArgumentParser
from contextlib import contextmanager

from hosts.nodes import *
from hosts.parser import Parsers


def main():
    args = parse_args()

    with open_spec(args.input_spec, sys.stdin) as input_file:
        hosts_string = input_file.read()

    parsers = Parsers()
    hosts = parsers.hosts.parseString(hosts_string)[0]

    for line in args.add_lines:
        line_content = parsers.line_content.parseString(line)[0]
        hosts.lines.append(LineNode([line_content, LineEndNode('\n')]))

    for host in args.remove_hosts:
        lines = []
        for line in hosts.lines:
            entry = line.line_content.entry
            if entry and entry.canonical_hostname.text == host:
                continue
            lines.append(line)
        hosts.lines = lines

    hosts_string = hosts.dump()

    with open_spec(args.output_spec, sys.stdout, 'w') as output_file:
        output_file.write(hosts_string)


def parse_args():
    parser = ArgumentParser()

    default_spec = '/etc/hosts'

    parser.add_argument(
        '-a', '--add-line',
        action='append',
        default=[],
        dest='add_lines',
    )

    parser.add_argument(
        '-i', '--input',
        default=default_spec,
        dest='input_spec',
    )

    parser.add_argument(
        '-o', '--output',
        default=default_spec,
        dest='output_spec',
    )

    parser.add_argument(
        '-r', '--remove',
        action='append',
        default=[],
        dest='remove_hosts',
    )

    return parser.parse_args()


@contextmanager
def open_spec(spec, std_file, *open_args):
    if spec == '-':
        yield std_file
    else:
        with open(spec, *open_args) as file_:
            yield file_


if __name__ == '__main__':
    main()

