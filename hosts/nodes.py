class HostsNode:
    def __init__(self, lines):
        self.lines = lines

    def append_entry(self, ip_address, canonical_hostname, aliases=None):
        line = Line.create_entry(ip_address, canonical_hostname,
                                 aliases=aliases)
        self.lines.append(line)

    def dump(self):
        return ''.join(line.dump() for line in self.lines)

    def remove_lines_with_canonical_hostname(self, canonical_hostname):
        lines = []
        for line in self.lines:
            entry = line.entry
            if entry and entry.canonical_hostname != canonical_hostname:
                lines.append(line)
        self.lines = lines

    def remove_lines_with_ip_address(self, ip_address):
        lines = []
        for line in self.lines:
            if line.entry and line.entry.ip_address.text != ip_address:
                lines.append(line)
        self.lines = lines


class Tokens:
    def __init__(self, tokens):
        self.tokens = tokens

    def  __repr__(self):
        return '{}({!r})'.format(self.__class__.__name__, self.tokens)

    def dump(self):
        return ''.join(token.dump() for token in self.tokens)


class LineNode(Tokens):
    def __init__(self, tokens):
        super().__init__(tokens)
        for token in self.tokens:
            if isinstance(token, LineContentNode):
                self.line_content = token
            elif isinstance(token, LineEndNode):
                self.line_end = token

    def has_comment(self):
        return self.comment is not None


class LineContentNode(Tokens):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.entry = None
        self.commenty = None
        for token in tokens:
            if isinstance(token, EntryNode):
                self.entry = token
            elif isinstance(token, CommentNode):
                self.comment = token


class EntryNode(Tokens):
    def __init__(self, tokens):
        super().__init__(tokens)

        def is_token(type_):
            return isinstance(token, type_)

        for token in self.tokens:
            if is_token(IPAddressNode):
                self.ip_address = token
            elif is_token(CanonicalHostnameNode):
                self.canonical_hostname = token
            elif is_token(AliasesNode):
                self.aliases = token

        if not hasattr(self, 'aliases'):
            self.aliases = AliasesNode([])

    def __str__(self):
        return '{} {} {}'.format(self.ip_address, self.canonical_hostname,
                                 self.aliases)

    @classmethod
    def create(cls, ip_address, canonical_hostname, aliases=None):
        if aliases is None:
            aliases = []
        return cls([
            IPAddress(ip_address),
            WhiteSpace(' '),
            CanonicalHostname(canonical_hostname),
            Aliases.create(aliases),
        ])


class AliasesNode(Tokens):
    def __str__(self):
        return ' '.join(str(token) for token in self.tokens
                        if isinstance(token, AliasNode))

    @classmethod
    def create(cls, aliases):
        tokens = []
        for i, alias in enumerate(aliases):
            if i > 0:
                tokens.append(WhiteSpace(' '))
            tokens.append(Alias(alias))
        return cls(tokens)


class Token:
    def __init__(self, text):
        self.text = text

    def __len__(self):
        return len(self.text)

    def __repr__(self):
        return '{}({!r})'.format(self.__class__.__name__, self.text)

    def __str__(self):
        return self.text

    def dump(self):
        return self.text


class CommentNode(Token):
    pass


class LineEndNode(Token):
    pass


class FieldNode(Token):
    pass


class IPAddressNode(FieldNode):
    pass


class CanonicalHostnameNode(FieldNode):
    pass


class AliasNode(FieldNode):
    pass


class WhitespaceNode(Token):
    def expand_tabs(self, width):
        self._text = self._text.replace('\t', ' ' * width)

