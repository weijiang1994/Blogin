"""
# coding:utf-8
GitHub API social stats fetcher.
"""
import requests

from blogin.utils.constants import (
    GITHUB_STAR, GITHUB_FORK, GITHUB_WATCHER,
    GITHUB_STAR_DARK, GITHUB_FORK_DARK, GITHUB_WATCHER_DARK,
    USER_API, REPO_API,
)


def github_social():
    star = requests.get(GITHUB_STAR, timeout=30)
    fork = requests.get(GITHUB_FORK, timeout=30)
    watcher = requests.get(GITHUB_WATCHER, timeout=30)
    star_dark = requests.get(GITHUB_STAR_DARK, timeout=30)
    fork_dark = requests.get(GITHUB_FORK_DARK, timeout=30)
    watcher_dark = requests.get(GITHUB_WATCHER_DARK, timeout=30)
    user_info = requests.get(USER_API, timeout=30)
    repo_info = requests.get(REPO_API, timeout=30)
    return star, fork, watcher, star_dark, fork_dark, watcher_dark, user_info, repo_info
