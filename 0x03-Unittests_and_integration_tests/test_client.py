#!/usr/bin/env python3
"""Unit tests for GithubOrgClient class."""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD



class TestGithubOrgClient(unittest.TestCase):
    """Test cases for the GithubOrgClient class."""

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns expected repos and uses correct URL."""

        # Mocked payload from get_json
        mock_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = mock_payload

        # Expected result from public_repos
        expected_repos = ["repo1", "repo2", "repo3"]

        # Create instance of client
        client = GithubOrgClient("test_org")

        # Patch _public_repos_url to avoid external calls
        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=MagicMock) as mock_url:
            mock_url.return_value = "http://mocked-url.com"

            # Call the method
            result = client.public_repos()

            # Assertions
            self.assertEqual(result, expected_repos)
            mock_get_json.assert_called_once_with("http://mocked-url.com")
            mock_url.assert_called_once()
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test for GithubOrgClient.public_repos."""

    @classmethod
    def setUpClass(cls):
        """Start patching requests.get."""
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        # Mock .json() response based on url
        cls.mock_get.side_effect = [
            unittest.mock.Mock(json=lambda: cls.org_payload),
            unittest.mock.Mock(json=lambda: cls.repos_payload)
        ]

    @classmethod
    def tearDownClass(cls):
        """Stop patching requests.get."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected repositories."""
        client = GithubOrgClient("test")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos returns repos with license="apache-2.0"."""
        client = GithubOrgClient("test")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )


if __name__ == '__main__':
    unittest.main()
