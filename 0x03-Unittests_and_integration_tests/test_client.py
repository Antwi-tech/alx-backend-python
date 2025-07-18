#!/usr/bin/env python3
"""Unit and integration tests for GithubOrgClient."""

import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient methods."""

    @parameterized.expand([
        ("google", {"login": "google", "id": 1}),
        ("abc", {"login": "abc", "id": 2}),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, expected_response, mock_get_json):
        """Test that .org returns expected JSON from get_json."""
        mock_get_json.return_value = expected_response
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected_response)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self):
        """Test _public_repos_url returns expected repos_url."""
        with patch("client.GithubOrgClient.org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/testorg/repos"
            }
            client = GithubOrgClient("testorg")
            self.assertEqual(client._public_repos_url, "https://api.github.com/orgs/testorg/repos")
            mock_org.assert_called_once()

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns expected repo names."""
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = test_payload

        with patch("client.GithubOrgClient._public_repos_url", new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/testorg/repos"
            client = GithubOrgClient("testorg")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2", "repo3"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/testorg/repos")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({}, "my_license", False),
        ({"license": {}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns True if license key matches."""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": TEST_PAYLOAD["org_payload"],
        "repos_payload": TEST_PAYLOAD["repos_payload"],
        "expected_repos": TEST_PAYLOAD["expected_repos"],
        "apache2_repos": TEST_PAYLOAD["apache2_repos"],
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test for GithubOrgClient using real fixture payloads."""

    @classmethod
    def setUpClass(cls):
        """Patch requests.get to simulate API responses."""
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        # Configure sequence of responses to .json() calls
        cls.mock_get.side_effect = [
            Mock(json=lambda: cls.org_payload),
            Mock(json=lambda: cls.repos_payload)
        ]
        
    def test_public_repos(self):
        """
        Test that public_repos returns all expected repo names
        from the fixtures' repos_payload.
        """
        client = GithubOrgClient("testorg")
        result = client.public_repos()
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self):
        """
        Test that public_repos(license="apache-2.0") correctly
        filters repositories with 'apache-2.0' license from fixtures.
        """
        client = GithubOrgClient("testorg")
        result = client.public_repos(license="apache-2.0")
        self.assertEqual(result, self.apache2_repos)


    @classmethod
    def tearDownClass(cls):
        """Stop patching requests.get."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns all expected repos."""
        client = GithubOrgClient("testorg")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test that public_repos can filter by license key."""
        client = GithubOrgClient("testorg")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )


if __name__ == "__main__":
    unittest.main()
