import logging
from collections import namedtuple
from multiprocessing import Pool

import praw
import tqdm
from praw.models import MoreComments

logger = logging.getLogger(__name__)

Comment = namedtuple('Comment', 'text, upvotes')
Post = namedtuple('Post', 'url, upvotes, comments, file_name, caption')


class RedditScrapper:
    def __init__(self, client_id, client_secret):
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            grant_type='client_credentials',
            user_agent='mytestscript/1.0'
        )

    def scrap(self, subreddits, n_processes=14):
        data = []
        with Pool(n_processes) as p:
            with tqdm.tqdm(total=len(subreddits),
                           desc='Downloading subreddits') as pbar:
                iterator = p.imap_unordered(self._process_subreddit, subreddits)
                for data_part in iterator:
                    data.extend(data_part)
                    pbar.update()

        return data

    def _process_subreddit(self, subreddit):
        visited = set()

        posts = self.reddit.subreddit(subreddit).top(limit=500)
        posts = [sub for sub in posts if not sub.domain.startswith('self.')]

        data = []
        for post in tqdm.tqdm(posts, 'Iterating though posts'):
            url = post.url
            if url.endswith('.jpg') or url.endswith('.png'):
                comments = self._read_comments(post)
                if len(comments) and url not in visited:
                    post = Post(url, post.score, comments, None, None)
                    data.append(post)
                    visited.add(url)

        return data

    def _read_comments(self, post):
        comments = post.comments

        clean_comments = []
        for comment in comments:
            if isinstance(comment, MoreComments):
                continue

            flag, purge_body = self.purge_comment(comment.body, comment.score)
            if flag:
                clean_comment = Comment(purge_body, comment.score)
                clean_comments.append(clean_comment)

        return clean_comments

    @staticmethod
    def purge_comment(body, score):
        rules = [
            lambda: score >= 10,
            lambda: 8 <= len(body) <= 60,
            lambda: body[0] != '!',
            lambda: body.count('\n') <= 1,
            lambda: not body.startswith('http'),
            lambda: not body.startswith('['),
            lambda: sum(ch.isalpha() for ch in body) >= 0.8 * len(body),
            lambda: not body.startswith('/')
        ]

        return all(rule() for rule in rules), body.strip()
