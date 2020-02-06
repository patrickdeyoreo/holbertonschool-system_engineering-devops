#!/usr/bin/python3
"""
Show number of occurrences of keywords in hot post titles (case-insensitive)
"""
import requests

URL = 'https://www.reddit.com/r/{}/hot.json'
USER_AGENT = 'Mozilla/5.0 (Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0'


def count_words(subreddit, word_list, **kwargs):
    """
    Query reddit for hot posts and print total occurrences of each keyword
    """
    totals = kwargs.setdefault('totals', dict.fromkeys(word_list, 0))
    params = {
        'after': kwargs.setdefault('after'),
        'count': kwargs.setdefault('count', 0),
        'limit': kwargs.setdefault('limit', 100)
    }
    r = requests.get(
        URL.format(subreddit),
        headers={'User-Agent': USER_AGENT},
        params=params,
        allow_redirects=False,
        timeout=30,
    )
    if r.status_code == 200:
        results = r.json()['data']
        for post in results['children']:
            for word in post['data']['title'].split():
                if word.lower() in totals:
                    totals[word.lower()] += 1
        if results['after'] is not None:
            kwargs['after'] = results['after']
            kwargs['count'] += kwargs['limit']
            return count_words(subreddit, word_list, **kwargs)
        word_list = filter(totals.get, totals)
        for word in sorted(word_list, key=totals.get, reverse=True):
            print('{}: {}'.format(word, totals[word]))