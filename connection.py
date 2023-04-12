from urllib.parse import urlencode
import requests


class RepositoryConnection:
    def __init__(self, endpoint, repository_name):
        self.endpoint = endpoint
        self.repository_name = repository_name
        self.session = requests.Session()
        self.headers = {
            'Content-Type': 'application/sparql-query',
            'Accept': 'application/sparql-results+json'
        }

    def query(self, query):
        params = {
            'query': query
        }
        url = f'{self.endpoint}/repositories/{self.repository_name}?{urlencode(params)}'
        response = self.session.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()['results']

    def update(self, update):
        params = {
            'update': update
        }
        url = f'{self.endpoint}/repositories/{self.repository_name}/statements'
        response = self.session.post(url, data=params, headers=self.headers)
        response.raise_for_status()

    def close(self):
        self.session.close()

    def __enter__(self):
        # Code to establish a connection to the repository
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Code to close the connection to the repository
        self.session.close()

