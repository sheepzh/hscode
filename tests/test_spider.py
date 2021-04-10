# -*- coding: utf-8 -*-
"""
    Unit test of spider
"""
from unittest import TestCase, mock
import sys
sys.path.append('..')
from hscode import spider

CODE = '7201500010'


class TestSpider(TestCase):
    """
        Tests of the spider
    """

    def test_detail(self):
        """
            Parse the detail of hscode
        """
        hscode = spider.parse_details(CODE)
        self.assertNotEqual("{}", str(hscode))
        self.assertIsNotNone(hscode.tax)
        self.assertIsNotNone(hscode.name)
        self.assertTrue(len(hscode.declarations) > 0)
        self.assertTrue(len(hscode.ciq_code.keys()) > 0)

        hscode = spider.parse_details('110')
        self.assertIsNone(hscode)

    def test_proxy(self):
        """
            Test proxy
        """
        proxy = "https://www.baidu.com?s={url}"
        with mock.patch('requests.get') as mocked_get:
            hscode = spider.parse_details(CODE, proxy)
            self.assertIsNone(hscode.name)
            args = mocked_get.call_args_list[0][0]
            self.assertTrue(args[0].startswith('https://www.baidu.com'))

    def test_search_chapter(self):
        """
            Test chapter
        """
        # The count of chapter #97 is small
        included_outdated_codes = spider.search_chapter("97", True, quiet=True, proxy=None)

        with mock.patch('builtins.print') as mocked_print:
            latest_codes = spider.search_chapter("97", False, quiet=False, proxy=None)
            self.assertTrue(mocked_print.call_count > len(latest_codes))

        self.assertTrue(len(latest_codes) <= len(included_outdated_codes))
