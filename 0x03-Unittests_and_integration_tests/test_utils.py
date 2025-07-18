#!/usr/bin/env python3
"""Unit tests for utils module."""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for the access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "'a'"),
        ({"a": 1}, ("a", "b"), "'b'"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_message):
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), expected_message)


class TestGetJson(unittest.TestCase):
    """Test cases for get_json function."""

    @patch('utils.requests.get')
    def test_get_json(self, mock_get):
        test_url = "http://example.com/api"
        test_payload = {"key": "value"}

        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = get_json(test_url)
        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Test cases for memoize decorator."""

    def test_memoize(self):
        class TestClass:
            def __init__(self):
                self.call_count = 0

            @memoize
            def a_method(self):
                self.call_count += 1
                return 42

        obj = TestClass()
        result1 = obj.a_method
        result2 = obj.a_method

        self.assertEqual(result1, 42)
        self.assertEqual(result2, 42)
        self.assertEqual(obj.call_count, 1)  # Ensure it was only called once


class TestGetJson(unittest.TestCase):
    @patch('utils.requests.get')
    def test_get_json(self, mock_get):
        url = "http://example.com"
        expected_payload = {"message": "Hello"}

        mock_response = MagicMock()
        mock_response.json.return_value = expected_payload
        mock_get.return_value = mock_response

        self.assertEqual(get_json(url), expected_payload)
        mock_get.assert_called_once_with(url)


if __name__ == '__main__':
    unittest.main()
