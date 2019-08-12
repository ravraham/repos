import logging
import GitHub

repos_dict = {}


def query_github(key):
    gh_obj = GitHub.Repo(key)
    response = gh_obj.get_repos()
    for user in response:
        repos_dict[user['id']] = {'name': user['name'],
                                  'stars_count': user['stargazers_count'],
                                  'language': user['language']}


def main():
    try:
        query_github('users')
        query_github('orgs')
        sorted_keys = sorted(repos_dict, key=lambda x: (repos_dict[x]['stars_count']))
        for i in sorted_keys:
            print (repos_dict[i])
    except Exception as e:
        logging.error("{}".format(e))
        exit(1)


if __name__ == '__main__':
    main()
