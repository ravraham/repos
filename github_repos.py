import psycopg2
from psycopg2.extras import RealDictCursor
from config import config
import logging
import GitHub

repos_dict = {}


def get_query(query):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query)
        print("Count of records: ", cur.rowcount)
        return cur.fetchall()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def put_query(query):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query)
        conn.commit()
        return 'success'
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return error
    finally:
        if conn is not None:
            conn.close()


def query_github(key):
    gh_obj = GitHub.Repo(key)
    response = gh_obj.get_repos()
    for user in response:
        repos_dict[user['id']] = {'name': user['name'],
                                  'stars_count': user['stargazers_count'],
                                  'language': user['language']}
        query = "INSERT INTO github (name, stars, language) " \
                "VALUES('{name}', '{stars}', '{language}');". \
            format(name=user['name'],
                   stars=user['stargazers_count'],
                   language=user['language'])
        put_query(query)


def main():
    try:
        query_github('users')
        query_github('orgs')
        sorted_keys = sorted(repos_dict, key=lambda x: (repos_dict[x]['stars_count']))
        for i in sorted_keys:
            print (repos_dict[i])
        query = "select * from test;"
        print (get_query(query))
    except Exception as e:
        logging.error("{}".format(e))
        exit(1)


if __name__ == '__main__':
    main()
