import argparse
import requests
import json


class Repo(object):

    def __init__(self, key):

        self.url = 'https://api.github.com/{}/kubernetes/repos'.format(key)

    def execute_request(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            pass
        else:
            raise Exception('{}'.format(response))

        return response.json()

    def get_repos(self):

        return self.execute_request()

