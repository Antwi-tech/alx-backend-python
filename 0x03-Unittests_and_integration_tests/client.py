#!/usr/bin/env python3
"""GithubOrgClient module that fetches information about GitHub organizations."""

import requests
from functools import lru_cache


def get_json(url):
    """Fetch and return JSON content from a URL."""
    response = requests.get(url)
    return response.json()


class GithubOrgClient:
    """Client to interact with a GitHub organization."""

    ORG_URL = "https://api.github.com/orgs/{org}"

    def __init__(self, org):
        self.org_name = org

    @property
    @lru_cache()
    def org(self):
        """Return the organization data from GitHub."""
        url = self.ORG_URL.format(org=self.org_name)
        return get_json(url)

    @property
    def _public_repos_url(self):
        """Return the URL to fetch public repos of the organization."""
        return self.org.get("repos_url")

    def public_repos(self, license=None):
        """Return the list of public repo names. Optionally filter by license."""
        repos = get_json(self._public_repos_url)
        repo_names = [repo["name"] for repo in repos]
        if license:
            repo_names = [
                repo["name"] for repo in repos
                if repo.get("license", {}).get("key") == license
            ]
        return repo_names

    @staticmethod
    def has_license(repo, license_key):
        """Check if a repo has the given license."""
        return repo.get("license", {}).get("key") == license_key
