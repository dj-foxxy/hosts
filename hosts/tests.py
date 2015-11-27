import unittest

from hosts.parser import Parsers


DEBUG_PARSERS = False


class ParserTestCase(unittest.TestCase):
    def setUp(self):
        self.parser = self.get_parser(Parsers(debug=DEBUG_PARSERS))

    def parse(self, string):
        return self.parser.parseString(string)[0]


class EntryParserTestCase(ParserTestCase):
    def get_parser(self, parsers):
        return parsers.entry

    def test_ip_and_host(self):
        self.parse('127.0.0.1 localhost.local')

    def test_ip_host_and_alias(self):
        entry = self.parse('127.0.0.1 localhost.local localhost')
        self.assertEqual(entry.ip_address.text, '127.0.0.1')
        self.assertEqual(entry.canonical_hostname.text, 'localhost.local')


class LineContentTestCase(ParserTestCase):
    def get_parser(self, parsers):
        return parsers.line_content

    def test_line_content(self):
        print(self.parse(''))
        print(self.parse('#'))
        print(self.parse('127.0.0.1 localhost.local localhost'))

class WhitespaceParserTestCase(ParserTestCase):
    def get_parser(self, parsers):
        return parsers.whitespace

    def test_space(self):
        self.parse(' ')

    def test_tab(self):
        self.parse('\t')

    def test_multiple_spaces(self):
        self.parse('   ')

    def test_multiple_tabs(self):
        self.parse('\t\t\t')

    def test_spaces_and_tabs(self):
        self.parse(' \t \t')

