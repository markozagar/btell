"""Functionality to parse and transform user-provided search filters so we can build a reasonable QuerySet for stories."""
from typing import ClassVar, Dict, List, Optional
import dataclasses
import enum


@dataclasses.dataclass
class StoryFilter:
    """Provides the filter values from a parsed story filter string."""
    author: Optional[str] = None
    tags: List[str] = dataclasses.field(default_factory=list)
    completed: Optional[bool] = None
    freeform: List[str] = dataclasses.field(default_factory=list)
    sortby: str = '-last_update'  # Default sorting is newest first.
    filter_error: Optional[str] = None
    #
    accepted_fields: ClassVar[Dict[str, str]] = {
        "author": "author",
        "tags": "tags",
        "tag": "tags",
    }

    def add_filter(self, field: 'FilterToken', value: 'FilterToken'):
        """Adds the specified field to the story filter.

        Args:
            field: The field we want to add. Must be a TokenType.FIELD and have
                one of the known values.
            value: The value we want to add, must be a TokenType.LITERAL.
        
        Raises:
            SyntaxError: if the given tokens were incorrect types, or the field name is not known.
        """
        if not field.is_field():
            raise SyntaxError("Expected a field name, but was given a literal value!")
        if not value.is_literal():
            raise SyntaxError("Expected a literal value for the field, but was given another field!")

        # Some special values first
        if field.contents == "is":
            if value.contents == "completed":
                self.completed = True
                return
            raise SyntaxError(f"Uknown predicate for `is`: {value.contents}")

        if field.contents not in self.accepted_fields:
            raise SyntaxError(f"Unknown field name: {field.contents}")

        target_field = getattr(self, self.accepted_fields[field.contents])
        if isinstance(target_field, List):
            target_field.append(value.contents)
        else:
            setattr(self, self.accepted_fields[field.contents], value.contents)

    def add_literal(self, literal: 'FilterToken'):
        """Adds the specified literal value to the filter."""
        if not literal.is_literal():
            raise SyntaxError("Can't add a field name as a literal filter!")
        self.freeform.append(literal.contents)


class TokenType(enum.Enum):
    """Type of the query token we're parsing."""
    LITERAL = enum.auto()
    FIELD = enum.auto()


@dataclasses.dataclass
class FilterToken:
    """Describes each individual filter token from the query string."""
    contents: str
    type: TokenType

    @staticmethod
    def literal(val: str) -> 'FilterToken':
        """Creates a new literal token."""
        return FilterToken(contents=val, type=TokenType.LITERAL)

    @staticmethod
    def field(field_name: str) -> 'FilterToken':
        """Creates a new field token."""
        return FilterToken(contents=field_name, type=TokenType.FIELD)

    def is_literal(self) -> bool:
        """Returns true of this token is a literal."""
        return self.type == TokenType.LITERAL

    def is_field(self) -> bool:
        """Returns true if this token is a field."""
        return self.type == TokenType.FIELD

    def __str__(self):
        if self.type == TokenType.LITERAL:
            return f"LITERAL({self.contents})"
        elif self.type == TokenType.FIELD:
            return f"FIELD({self.contents})"
        else:
            return f"UNKNOWN({self.contents})"


def tokenize_query(filter_str: str) -> List[FilterToken]:
    """Lex-analyses the filter and returns distinct tokens as a list of strings."""
    cpos = 0
    ppos = 0
    tokens = []
    in_literal = False
    while cpos < len(filter_str):
        # Literal takes precedence over special symbol parsing.
        if in_literal:
            if filter_str[cpos] == '"':  # Closing quote
                in_literal = False
                tok = filter_str[ppos:cpos].strip()
                if tok:
                    tokens.append(FilterToken.literal(tok))  # Skip the final quote, we only want the contents
                ppos = cpos + 1
            cpos += 1
            # Skip normal processing while in literal
            continue
        if filter_str[cpos] in [':', ' ']:
            # grab current token
            if ppos < cpos:
                tok = filter_str[ppos:cpos].strip()
                if tok:
                    if filter_str[cpos] == ':':
                        tokens.append(FilterToken.field(tok))
                    else:
                        tokens.append(FilterToken.literal(tok))

            cpos += 1  # Skip the separator
            ppos = cpos
            continue
        if filter_str[cpos] == '"':
            # Start of literal
            # We may have some token preceding
            if ppos < cpos:
                tok = filter_str[ppos:cpos].strip()
                if tok:
                    tokens.append(FilterToken.literal(tok))
            in_literal = True
            cpos += 1  # We are only interested in the contents of the literal
            ppos = cpos
            continue
        # if we came this far, nothing special happened
        cpos += 1
    # Note: We may still be in_literal here, if a quote was not terminated.
    if in_literal:
        raise SyntaxError('Missing \'"\' in filter!')
    # When we've reached the end of the filter string, we may still have something pending
    if ppos < cpos:
        tok = filter_str[ppos:cpos].strip()
        if tok:
            tokens.append(FilterToken.literal(tok))
    return tokens


def prepare_stories_query(filter_str: Optional[str]) -> StoryFilter:
    """Parses the given stories filter and returns a query set with those conditions."""
    # Filter is like 'author:a tags:b,c,d freeform text'
    # - field:value
    # - space separated
    # - freeform text searches both title and description (any words)
    # - "literal text" - searches for this exactly
    # - special fields:
    #   - is:completed
    #   - author:who
    #   - tags:a,b,c
    #   - tag:a,b,c  # same as a above
    if not filter_str:
        return StoryFilter()  #  Basically everything
    tokens = tokenize_query(filter_str)
    ctoken = 0
    query = StoryFilter()
    while ctoken < len(tokens):
        tok = tokens[ctoken]
        if tok.is_field():
            if ctoken + 1 == len(tokens):
                query.filter_error = f"Field {tok.contents} specified without value!"
                return query
            next_token = tokens[ctoken + 1]
            try:
                query.add_filter(tok, next_token)
            except SyntaxError as syntax_error:
                query.filter_error = str(syntax_error)
                return query
            ctoken += 1
        elif tok.is_literal():
            query.add_literal(tok)
        ctoken += 1

    return query
