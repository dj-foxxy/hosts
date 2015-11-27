from pyparsing import LineEnd, Optional, Optional, StringEnd, Word, \
                      ZeroOrMore, printables, restOfLine

from hosts.nodes import *


__all__ = ['Parsers']


COMMENT_START = '#'


class Parsers:
    def __init__(self, debug=False):
        self._debug = debug
        self._create_whitespace_parser()
        self._create_field_parser()
        self._create_ip_address_parser()
        self._create_canonical_hostname_parser()
        self._create_alias_parser()
        self._create_aliases_parser()
        self._create_entry_parser()
        self._create_comment_parser()
        self._create_line_content()
        self._create_line_end_parser()
        self._create_line_parser()
        self._create_hosts_parser()

    def _config(self, parser, name, parse_action):
        parser.leaveWhitespace()
        parser.setDebug(self._debug)
        parser.setName(name)
        parser.setParseAction(parse_action)

    def _create_alias_parser(self):
        def parse_action(string, location, tokens):
            return AliasNode(tokens[0])
        self.alias = self.field.copy()
        self._config(self.alias, 'alias', parse_action)

    def _create_aliases_parser(self):
        def parse_action(string, location, tokens):
            return AliasesNode(tokens.asList())
        self.aliases = self.alias + ZeroOrMore(self.whitespace + self.alias)
        self._config(self.aliases, 'aliases', parse_action)

    def _create_entry_parser(self):
        def parse_action(string, location, tokens):
            return EntryNode(tokens.asList())
        self.entry = (
            self.ip_address +
            self.whitespace +
            self.canonical_hostname +
            Optional(self.whitespace + self.aliases)
        )
        self._config(self.entry, 'entry', parse_action)

    def _create_field_parser(self):
        self.field = Word(printables.replace(COMMENT_START, ''))
        self._config(self.field, 'field', lambda: None)

    def _create_canonical_hostname_parser(self):
        def parse_action(string, location, tokens):
            return CanonicalHostnameNode(tokens[0])
        self.canonical_hostname = self.field.copy()
        self._config(self.canonical_hostname, 'canonical_hostname',
                     parse_action)

    def _create_comment_parser(self):
        def parse_action(string, location, tokens):
            return CommentNode(''.join(tokens.asList()))
        self.comment = COMMENT_START + restOfLine
        self._config(self.comment, 'comment', parse_action)

    def _create_ip_address_parser(self):
        def parse_action(string, location, tokens):
            return IPAddressNode(tokens[0])
        self.ip_address = self.field.copy()
        self._config(self.ip_address, 'ip_address', parse_action)

    def _create_hosts_parser(self):
        def parse_action(string, location, tokens):
            return HostsNode(tokens.asList())
        self.hosts = ZeroOrMore(self.line) + StringEnd()
        self._config(self.hosts, 'hosts', parse_action)

    def _create_line_content(self):
        def parse_action(string, location, tokens):
            return LineContentNode(tokens.asList())
        self.line_content = (Optional(self.whitespace) + Optional(self.entry) +
                             Optional(self.whitespace) +
                             Optional(self.comment))
        self._config(self.line_content, 'line_content', parse_action)

    def _create_line_parser(self):
        def parse_action(string, location, tokens):
            return LineNode(tokens.asList())
        self.line = self.line_content + self.line_end
        self._config(self.line, 'line', parse_action)

    def _create_line_end_parser(self):
        def parse_action(string, location, tokens):
            return LineEndNode(tokens[0])
        self.line_end = LineEnd()
        self._config(self.line_end, 'line_end', parse_action)

    def _create_whitespace_parser(self):
        def parse_action(string, location, tokens):
            return WhitespaceNode(tokens[0])
        self.whitespace = Word('\t ')
        self._config(self.whitespace, 'white_space', parse_action)

