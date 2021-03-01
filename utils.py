import csv

def get_issues(name, auth, state='all'):
    requests.adapters.DEFAULT_RETRIES = 5
    url = 'https://api.github.com/repos/{}/issues?state={}'.format(name, state)
    r = requests.get(url, auth=auth)
    output = []
    return output


config = configparser.ConfigParser()
config.read(".config")
access_token = config.get("GITHUB", "token")
username = 'retroam'
state = 'all'