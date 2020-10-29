#!/usr/bin/env python3.9

# Command line tool to populate and display the following stats:
# * Top-N repos by number of stars.
# * Top-N repos by number of forks.
# * Top-N repos by number of Pull Requests (PRs).
# * Top-N repos by contribution percentage (PRs/forks).
#
# From the command line enter ./task.py -args

import sys
import json
import ssl
import local_github
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username" ,dest="username", required=True)
parser.add_argument("-p", "--password", dest="password", required=True)
parser.add_argument("-org", "--organization", dest="organization", required=True)
parser.add_argument("-n", "--number", dest="number", type=int, default=10)
args = parser.parse_args()

class Error(Exception):
    pass

class CheckError(Error):
    """Exception raised if Top N is more than number of repos in an org."""

    def __init__(self, error):
        self.message = error


class TwitterTask():

    def __init__(self, user, pwd, org, number):
        self.github = local_github.LocalGitHub(user, pwd, org)
        self.number = number

    def main(self):
        if not self.github.CheckTotalOrgRepCountCheck(self.number):
            raise(CheckError(
                "ERROR:Top N number larger than total number if repos in org."))
        self.github.PopulateStats()
        self.stat_store = self.github.GetStatStore()
        self.GetContributionPercent()
        self.GetResults()

    def GetResults(self):
        for key in self.stat_store.keys():
            self.GetTopReposByAttribute(key)

    def DisplayResults(self, results, type):
        x = 1
        print(f'Top-{len(results)} repos by number of {type} \n')
        for r in results:
            print(f'{x:2}:{r[0]:20} =====> {r[1]}')
            x+=1
        print('\n')

    def GetTopReposByAttribute(self, att):
        output = []
        x = self.stat_store
        y = sorted(x[att].items(),  key=lambda x: x[1],  reverse=True)
        count = 0
        while count < self.number:
            output.append(y[count])
            count+=1
        self.DisplayResults(output, att)

    def GetContributionPercent(self):
        # repos by contribution percentage (PRs/forks).
        self.stat_store['contribution_percent'] = {}
        for name, fork_count  in self.stat_store['forks'].items():
            try:
                percent = (self.stat_store['pulls'][name] / fork_count)*100
                self.stat_store['contribution_percent'][name] = percent
            except ZeroDivisionError:
                self.stat_store['contribution_percent'][name] = 0


if __name__ == "__main__":
    TwitterTask(args.username, args.password,
                args.organization, args.number).main()
    sys.exit("Run Complete")
