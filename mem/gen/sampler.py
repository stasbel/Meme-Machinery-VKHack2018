import numpy as np
from numpy import random

from mem.gen.stages import Matcher


class TextSampler:
    def __init__(self, matrix, meta, top_k=5):
        self.matcher = Matcher(matrix)
        self.meta = meta
        self.top_k = top_k

    def sample(self, image):
        nearest_ids = self.matcher.match(image, top_k=self.top_k)

        posts = [self.meta[id_] for id_ in nearest_ids]
        w_posts = np.array([post.upvotes for post in posts])
        post_id = random.choice(len(posts), size=1, replace=False,
                                p=w_posts / w_posts.sum())[0]
        post = posts[post_id]
        if post.caption is not None:
            return post.caption

        comments = post.comments
        w_comments = np.array([comment.upvotes for comment in comments])
        comment_id = random.choice(len(comments), size=1, replace=False,
                                   p=w_comments / w_comments.sum())[0]
        comment = comments[comment_id]

        return comment.text
