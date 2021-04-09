# -*- coding: utf-8 -*-
"""
    Unit test of argument
"""
from unittest import TestCase, mock
import sys
sys.path.append('..')
from hscode.argument import parse_argv, Argument, DEFAULT_CHAPTER, DEFAULT_FILE_ROOT, print_help

FOO = 'foo.py'


class TestParseArgv(TestCase):
    """
        Test the parse_argv
    """

    def test_default_val(self):
        """
            The default value
        """
        argument = Argument()
        self.assertFalse(argument.print_help)
        self.assertFalse(argument.all_chapters)
        self.assertEqual(argument.chapter, DEFAULT_CHAPTER)
        self.assertEqual(argument.file_root, DEFAULT_FILE_ROOT)
        self.assertFalse(argument.outdated)
        self.assertFalse(argument.no_latest)
        self.assertFalse(argument.print_help)
        self.assertFalse(argument.quiet_mode)
        self.assertFalse(argument.url_proxy)

    @mock.patch('builtins.print')
    def test_help(self, mocked_print):
        """
            Test help options
        """
        argument = parse_argv([FOO, '--help'])
        self.assertTrue(argument.print_help)
        argument = parse_argv([FOO])
        self.assertFalse(argument.print_help)

        print_help()
        self.assertTrue(mocked_print.call_count > 1)

    def test_chapters(self):
        """
            Test chapters
        """
        argument = parse_argv([FOO, '-s', '02'])
        self.assertEqual('02', argument.chapter)

        argument = parse_argv([FOO, '-s'])
        self.assertEqual(DEFAULT_CHAPTER, argument.chapter)

        argument = parse_argv([FOO, '-s', '03', '-a'])
        self.assertIsNone(argument.chapter)
        self.assertTrue(argument.all_chapters)

        argument = parse_argv([FOO, '-a', '-s', '03'])
        self.assertIsNone(argument.chapter)
        self.assertTrue(argument.all_chapters)

        argument = parse_argv([FOO, '--all', '-s', '03'])
        self.assertIsNone(argument.chapter)
        self.assertTrue(argument.all_chapters)

        argument = parse_argv([FOO, '--all'])
        self.assertIsNone(argument.chapter)
        self.assertTrue(argument.all_chapters)

    def test_file_root(self):
        """
            Test file root
        """
        argument = parse_argv([FOO, '--file-root', '/home'])
        self.assertEqual(argument.file_root, '/home')
        argument = parse_argv([FOO])
        self.assertEqual(argument.file_root, DEFAULT_FILE_ROOT)

    def test_quiet(self):
        """
            Test the quiet mode
        """
        argument = parse_argv([FOO, '-q'])
        self.assertTrue(argument.quiet_mode)
        self.assertFalse(parse_argv([FOO]).quiet_mode)

    def test_outdated(self):
        """
            Test the outdated
        """
        argument = parse_argv([FOO, '--outdated'])
        self.assertTrue(argument.outdated)
        argument = parse_argv([FOO])
        self.assertFalse(argument.outdated)

    def test_no_latest(self):
        """
            Test --no-latest
        """
        argument = parse_argv([FOO, '--no-latest'])
        self.assertTrue(argument.no_latest)

        argument = parse_argv([FOO])
        self.assertFalse(argument.no_latest)

    def test_proxy(self):
        """
            Test --proxy
        """
        argument = parse_argv([FOO, '--proxy'])
        self.assertEqual(argument.url_proxy, None)

        argument = parse_argv([FOO])
        self.assertEqual(argument.url_proxy, None)

        argument = parse_argv([FOO, '--proxy', 'http://www.baidu.com?s={url}'])
        self.assertEqual(argument.url_proxy, 'http://www.baidu.com?s={url}')

        argument = parse_argv([FOO, '--proxy', 'http://www.baidu.com?s={url'])
        self.assertIsNone(argument.url_proxy)
