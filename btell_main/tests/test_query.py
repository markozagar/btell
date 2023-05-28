from typing import List

from django import test

from btell_main.util import filter_query

def l2ft(literals: List[str]) -> List[filter_query.FilterToken]:
    return [filter_query.FilterToken.literal(a) for a in literals]


class TestFilterQueryTokenizer(test.TestCase):

    def test_tokenize_trivial(self):
        filter_str = ''
        result = filter_query.tokenize_query(filter_str)
        self.assertEqual(result, [])

    def test_tokenize_one_word(self):
        filter_str = 'word'
        result = filter_query.tokenize_query(filter_str)
        self.assertEqual(l2ft(['word']), result)

    def test_tokenize_multiple_words(self):
        filter_str = 'some more words to parse'
        result = filter_query.tokenize_query(filter_str)
        self.assertEqual(l2ft(['some', 'more', 'words', 'to', 'parse']), result)

    def test_tokenize_multiple_spaces(self):
        filter_str = 'double  space'
        result = filter_query.tokenize_query(filter_str)
        self.assertEqual(l2ft(['double', 'space']), result)

    def test_tokenize_special_field(self):
        filter_str = 'author:someone'
        result = filter_query.tokenize_query(filter_str)
        expected = [
            filter_query.FilterToken.field('author'),
            filter_query.FilterToken.literal('someone'),
        ]
        self.assertEqual(expected, result)

    def test_tokenize_multiple_special_fields(self):
        filter_str = 'author:someone is:completed'
        result = filter_query.tokenize_query(filter_str)
        expected = [
            filter_query.FilterToken.field('author'),
            filter_query.FilterToken.literal('someone'),
            filter_query.FilterToken.field('is'),
            filter_query.FilterToken.literal('completed'),
        ]
        self.assertEqual(expected, result)

    def test_tokenize_fields_double_space(self):
        filter_str = 'author:someone  is:completed'
        result = filter_query.tokenize_query(filter_str)
        expected = [
            filter_query.FilterToken.field('author'),
            filter_query.FilterToken.literal('someone'),
            filter_query.FilterToken.field('is'),
            filter_query.FilterToken.literal('completed'),
        ]
        self.assertEqual(expected, result)

    def test_tokenize_mix_fields_literals(self):
        filter_str = 'author:someone literal1 is:completed other words'
        result = filter_query.tokenize_query(filter_str)
        expected = [
            filter_query.FilterToken.field('author'),
            filter_query.FilterToken.literal('someone'),
            filter_query.FilterToken.literal('literal1'),
            filter_query.FilterToken.field('is'),
            filter_query.FilterToken.literal('completed'),
            filter_query.FilterToken.literal('other'),
            filter_query.FilterToken.literal('words'),
        ]
        self.assertEqual(expected, result)

    def test_tokenize_quoted_literal(self):
        filter_str = '"single token literal"'
        result = filter_query.tokenize_query(filter_str)
        self.assertEqual(l2ft(['single token literal']), result)

    def test_tokenize_multiple_quoted(self):
        filter_str = '"some token" "another token"'
        result = filter_query.tokenize_query(filter_str)
        self.assertEqual(l2ft(['some token', 'another token']), result)

    def test_tokenize_multi_no_space(self):
        filter_str = '"some token""another token"'
        result = filter_query.tokenize_query(filter_str)
        self.assertEqual(l2ft(['some token', 'another token']), result)

    def test_tokenize_mixed_multi_normal(self):
        filter_str = '"some token" another token'
        result = filter_query.tokenize_query(filter_str)
        self.assertEqual(l2ft(['some token', 'another', 'token']), result)
 
    def test_tokenize_mixed_multi_normal2(self):
        filter_str = ' first some "then some" and more "also this"'
        result = filter_query.tokenize_query(filter_str)
        self.assertEqual(l2ft(['first', 'some', 'then some', 'and', 'more', 'also this']), result)

    def test_tokenize_mixed_literal_field(self):
        filter_str = '"literal field" author:someone "author:fake"'
        result = filter_query.tokenize_query(filter_str)
        expected = [
            filter_query.FilterToken.literal('literal field'),
            filter_query.FilterToken.field('author'),
            filter_query.FilterToken.literal('someone'),
            filter_query.FilterToken.literal('author:fake'),
        ]
        self.assertEqual(expected, result)

    def test_malformed_field(self):
        filter_str = 'author:someone:field'
        result = filter_query.tokenize_query(filter_str)
        expected = [
            filter_query.FilterToken.field('author'),
            filter_query.FilterToken.field('someone'),
            filter_query.FilterToken.literal('field'),
        ]
        self.assertEqual(expected, result)

    def test_multiword_field_literal(self):
        filter_str = 'author:"Some Fancypants"'
        result = filter_query.tokenize_query(filter_str)
        expected = [
            filter_query.FilterToken.field('author'),
            filter_query.FilterToken.literal('Some Fancypants'),
        ]
        self.assertEqual(expected, result)

# TODO: More tests for incorrect syntax


class TestFilterQuery(test.TestCase):

    def test_trivial_empty(self):
        filter_str = ''
        q = filter_query.prepare_stories_query(filter_str)
        expected = filter_query.StoryFilter()
        self.assertEqual(expected, q)

    def test_simple_freeform(self):
        filter_str = 'free form text'
        q = filter_query.prepare_stories_query(filter_str)
        expected = filter_query.StoryFilter(freeform=['free', 'form', 'text'])
        self.assertEqual(expected, q)

    def test_simple_field(self):
        filter_str = 'author:someone'
        q = filter_query.prepare_stories_query(filter_str)
        expected = filter_query.StoryFilter(author='someone')
        self.assertEqual(expected, q)

    def test_field_with_literal(self):
        filter_str = 'author:someone extra text'
        q = filter_query.prepare_stories_query(filter_str)
        expected = filter_query.StoryFilter(author='someone', freeform=['extra', 'text'])
        self.assertEqual(expected, q)

    def test_field_with_quoted_literal(self):
        filter_str = 'author:someone "extra text"'
        q = filter_query.prepare_stories_query(filter_str)
        expected = filter_query.StoryFilter(author='someone', freeform=['extra text'])
        self.assertEqual(expected, q)

    def test_multi_field(self): 
        filter_str = 'author:someone tag:bla'
        q = filter_query.prepare_stories_query(filter_str)
        expected = filter_query.StoryFilter(author='someone', tags=['bla'])
        self.assertEqual(expected, q)

    def test_multi_field_and_literals(self):
        filter_str = 'author:someone extra text tag:bla1 "more text" tags:bla2'
        q = filter_query.prepare_stories_query(filter_str)
        expected = filter_query.StoryFilter(
            author='someone',
            tags=['bla1', 'bla2'],
            freeform=['extra', 'text', 'more text'])
        self.assertEqual(expected, q)

# TODO: Add tests for some incorrect syntax