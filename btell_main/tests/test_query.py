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
        self.assertEqual(result, l2ft(['word']))

    def test_tokenize_multiple_words(self):
        filter_str = 'some more words to parse'
        result = filter_query.tokenize_query(filter_str)
        self.assertEqual(result, l2ft(['some', 'more', 'words', 'to', 'parse']))

    def test_tokenize_multiple_spaces(self):
        filter_str = 'double  space'
        result = filter_query.tokenize_query(filter_str)
        self.assertEqual(result, l2ft(['double', 'space']))

    def test_tokenize_special_field(self):
        filter_str = 'author:someone'
        result = filter_query.tokenize_query(filter_str)
        expected = [
            filter_query.FilterToken.field('author'),
            filter_query.FilterToken.literal('someone'),
        ]
        self.assertEqual(result, expected)

    def test_tokenize_multiple_special_fields(self):
        filter_str = 'author:someone is:completed'
        result = filter_query.tokenize_query(filter_str)
        expected = [
            filter_query.FilterToken.field('author'),
            filter_query.FilterToken.literal('someone'),
            filter_query.FilterToken.field('is'),
            filter_query.FilterToken.literal('completed'),
        ]
        self.assertEqual(result, expected)

    def test_tokenize_fields_double_space(self):
        filter_str = 'author:someone  is:completed'
        result = filter_query.tokenize_query(filter_str)
        expected = [
            filter_query.FilterToken.field('author'),
            filter_query.FilterToken.literal('someone'),
            filter_query.FilterToken.field('is'),
            filter_query.FilterToken.literal('completed'),
        ]
        self.assertEqual(result, expected)

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
        self.assertEqual(result, expected)

    def test_tokenize_quoted_literal(self):
        filter_str = '"single token literal"'
        result = filter_query.tokenize_query(filter_str)
        self.assertEqual(result, l2ft(['single token literal']))

    def test_tokenize_multiple_quoted(self):
        filter_str = '"some token" "another token"'
        result = filter_query.tokenize_query(filter_str)
        self.assertEqual(result, l2ft(['some token', 'another token']))

    def test_tokenize_multi_no_space(self):
        filter_str = '"some token""another token"'
        result = filter_query.tokenize_query(filter_str)
        self.assertEqual(result, l2ft(['some token', 'another token']))

    def test_tokenize_mixed_multi_normal(self):
        filter_str = '"some token" another token'
        result = filter_query.tokenize_query(filter_str)
        self.assertEqual(result, l2ft(['some token', 'another', 'token']))
 
    def test_tokenize_mixed_multi_normal2(self):
        filter_str = ' first some "then some" and more "also this"'
        result = filter_query.tokenize_query(filter_str)
        self.assertEqual(result, l2ft(['first', 'some', 'then some', 'and', 'more', 'also this']))

    def test_tokenize_mixed_literal_field(self):
        filter_str = '"literal field" author:someone "author:fake"'
        result = filter_query.tokenize_query(filter_str)
        expected = [
            filter_query.FilterToken.literal('literal field'),
            filter_query.FilterToken.field('author'),
            filter_query.FilterToken.literal('someone'),
            filter_query.FilterToken.literal('author:fake'),
        ]
        self.assertEqual(result, expected)