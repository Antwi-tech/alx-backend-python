#!/usr/bin/env python3
"""Unit tests for GithubOrgClient class."""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD





class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient class."""

    @parameterized.expand([
        ("google", {"login": "google", "id": 1}),
        ("abc", {"login": "abc", "id": 2}),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, expected_response, mock_get_json):
        """Test that GithubOrgClient.org returns correct value from get_json."""

        # Arrange
        mock_get_json.return_value = expected_response

        # Act
        client = GithubOrgClient(org_name)
        result = client.org

        # Assert
        self.assertEqual(result, expected_response)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the correct URL from org payload."""
        with patch("client.GithubOrgClient.org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "https://api.github.com/orgs/testorg/repos"}
            client = GithubOrgClient("testorg")

            result = client._public_repos_url

            self.assertEqual(result, "https://api.github.com/orgs/testorg/repos")
            mock_org.assert_called_once()


class TestGithubOrgClient(unittest.TestCase):
    """Test case for the GithubOrgClient class."""

    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"})
    ])
    @patch('client.get_json')
    def test_org(self, org_name, expected, mock_get_json):
        """Test that GithubOrgClient.org returns correct org info."""
        mock_get_json.return_value = expected
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """Test _public_repos_url returns expected URL."""
        with patch.object(GithubOrgClient, 'org',
                          new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "http://repos.com"}
            client = GithubOrgClient("google")
            self.assertEqual(client._public_repos_url, "http://repos.com")

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns expected list of repos."""
        mock_get_json.return_value = [
            {"name": "repo1"}, {"name": "repo2"}
        ]
        with patch.object(GithubOrgClient,
                          '_public_repos_url',
                          new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "http://fake.url"
            client = GithubOrgClient("test")
            self.assertEqual(client.public_repos(), ["repo1", "repo2"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("http://fake.url")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({}, "my_license", False),
        ({"license": {}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns True if license matches, else False."""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)
    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns expected list and mocks are called correctly."""
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]

        mock_get_json.return_value = test_payload

        with patch("client.GithubOrgClient._public_repos_url", new_callable=PropertyMock) as mock_repos_url:
            mock_repos_url.return_value = "https://api.github.com/orgs/testorg/repos"

            client = GithubOrgClient("testorg")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2", "repo3"])
            mock_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/testorg/repos")
    
    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({}, "my_license", False),
        ({"license": {}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license returns correct boolean for license check."""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)

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
