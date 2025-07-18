#!/usr/bin/env python3
"""Unit tests for GithubOrgClient class."""

import unittest
from unittest.mock import Mock, patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient class."""


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
        """Test public_repos returns expected repo names."""
        
        
        mock_get_json.return_value = [
            {"name": "repo-alpha"},
            {"name": "repo-beta"},
            {"name": "repo-gamma"}
        ]

        with patch.object(GithubOrgClient,
                          '_public_repos_url',
                          new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/fake/repos"
            client = GithubOrgClient("fake")
            result = client.public_repos()
            self.assertEqual(result, ["repo-alpha", "repo-beta", "repo-gamma"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/fake/repos"
            )

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

@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD['org_payload'],
        'repos_payload': TEST_PAYLOAD['repos_payload'],
        'expected_repos': TEST_PAYLOAD['expected_repos'],
        'apache2_repos': TEST_PAYLOAD['apache2_repos'],
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test for GithubOrgClient.public_repos with real payloads."""


    @classmethod
    def setUpClass(cls):
        """Start patching requests.get and setup mock returns."""
        
        
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        # Configure side_effect to mock responses based on the URL
        cls.mock_get.side_effect = [
            Mock(json=lambda: cls.org_payload),
            Mock(json=lambda: cls.repos_payload),
        ]

    @classmethod
    def tearDownClass(cls):
        """Stop patching requests.get."""
        
        
        cls.get_patcher.stop()


    def test_public_repos(self):
        """Test that public_repos returns expected list of repo names."""
        client = GithubOrgClient("test")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test that public_repos returns repos filtered by license='apache-2.0'."""
        
        
        client = GithubOrgClient("test")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )


@parameterized_class([
    {
        'org_payload': org_payload,
        'repos_payload': repos_payload,
        'expected_repos': expected_repos,
        'apache2_repos': apache2_repos
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos method."""


    @classmethod
    def setUpClass(cls):
        """Set up patcher for requests.get using fixtures."""
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        # Mocked JSON responses based on call order
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
        """Test public_repos filters repos by license key."""
        client = GithubOrgClient("test")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )


if __name__ == '__main__':
    unittest.main()
