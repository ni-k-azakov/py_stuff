import collections


class Chat:
    def __init__(self):
        self._flood = collections.Counter()

    def plus(self, user_id):
        self._flood[user_id] += 1

    def get(self, user_id):
        return self._flood[user_id]

    def get_all(self):
        return self._flood

    def sort(self):
        self._flood.most_common()
