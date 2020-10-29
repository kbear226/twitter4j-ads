# Python GitHub Instance
import github
from github import Github


class LocalGitHub():

    def __init__(self, user, pwd, org):
        self._user = user
        self._pwd = pwd
        self._g = Github(self._user, self._pwd)
        self.repos = self._g.get_organization(login=org).get_repos()
        self.fork_stats = {}
        self.star_stats = {}
        self.pull_stats = {}

    def GetStatStore(self):
        return {
            'forks': self.fork_stats,
            'stars': self.star_stats,
            'pulls': self.pull_stats
        }

    def PopulateStats(self):
        for r in self.repos:
            self.fork_stats[r.name] = r.forks_count
            self.star_stats[r.name] = r.stargazers_count
            self.pull_stats[r.name] = r.get_pulls().totalCount

    def CheckTotalOrgRepCountCheck(self, number):
        # Returns True if number less than total repo count
        # Assert enough repos to populate a top N list.
        if number < self.repos.totalCount:
            return True
        else:
            return False

    def _GetForkStats(self):
        return {r.name:r.forks_count for r in self.repos}

    def _GetStarStats(self):
        return {r.name:r.stargazers_count for r in self.repos}

    def _GetPullStats(self):
        return {r.name:r.get_pulls().totalCount for r in self.repos}
