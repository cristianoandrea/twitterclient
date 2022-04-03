

import dbmanager

class Tale:
    def __init__(self, id: int, creator: str, text: str):
        self._id = id
        self._creator: str = creator
        self._text: str = text

    @property
    def id(self):
        return self._id

    @property
    def creator(self):
        return self._creator

    @property
    def text(self):
        return self._text

    def toDict(self):
        d = {}
        d['id'] = self.id
        d['creator'] = self.creator
        d['text'] = self.text
        return d

    @staticmethod
    def fromDict(d: dict):
        return Tale(d['id'], d['creator'], d['text'])


class Contest:
    def __init__(self, id: int, tales: list, organizer: str, name: str):
        self._id = id
        self._tales: list = tales
        self._organizer: str = organizer
        self._name: str = name

    @property
    def id(self):
        return self._id

    @property
    def tales(self):
        return self._tales

    @property
    def organizer(self):
        return self._organizer

    @property
    def name(self):
        return self._name

    @property
    def is_active(self):
        return True

    def add_tale(self, tale: int):
        self._tales.append(tale)

    def has_tale(self, tale_id: int):
        return tale_id in self.tales

    def toDict(self):
        d = {}
        d['tales'] = self.tales
        d['id'] = self.id
        d['organizer'] = self.organizer
        d['name'] = self.name
        return d

    @staticmethod
    def fromDict(d: dict):
        return Contest(d['id'], d['tales'], d['organizer'], d['name'])


next_contest_id: int = 0
next_tale_id: int = 0
initialized: bool = False
contests = {}
tales = {}


def module_init():
    global initialized

    if not initialized:
        for tale_dict in dbmanager.load_tales():
            tale = Tale.fromDict(tale_dict)
            tales[tale.id] = tale
        for contest_dict in dbmanager.load_contests():
            contest = Contest.fromDict(contest_dict)
            contests[contest.id] = contest

        initialized = True


def get_contest_list(active=False):
    l = []
    for contest in contests.values():
        if contest.is_active:
            l.append(contest.toDict())

    return l


def get_tale_list():
    t: list[dict] = []
    for tale in tales.values():
        t.append(tale.toDict())

    return t


def save_contests():
    contest_list = get_contest_list()
    dbmanager.save_contests(contest_list)


def save_tales():
    tale_list= get_tale_list()
    dbmanager.save_tales(tale_list)


def register_contest(organizer: str, name: str) :
    global next_contest_id

    c: Contest = Contest(next_contest_id, [], organizer, name)
    contests[c.id] = c
    next_contest_id += 1
    #memorizzarlo su disco
    #save_contests()

    return c


def register_tale(creator: str, text: str):
    global next_tale_id

    t: Tale = Tale(next_tale_id, creator, text)
    tales[t.id] = t
    next_tale_id += 1
    save_tales()

    return t


def add_tale_to(tale_id: int, contest_id: int):
    c: Contest = contests[contest_id]
    c.tales.append(tale_id)
    save_contests()


def is_tale_registered(tale_id: int):
    return tale_id in tales


def is_contest_registered(contest_id: int):
    return contest_id in contests


def make_vote_object(contest_id, tweets):
    MAX_VOTES = 10
    votes = {}
    #chiavi twitter username, valori il numero di voti in questo contest
    user_count = {}

    try:
        c = contests[contest_id]
        for tweet in tweets:
            try:
                indicated_contest = int(tweet['full_text'].split(' ')[1][1:])
                if indicated_contest != contest_id:
                    print(
                        f'indicato: {indicated_contest}, cercato {contest_id}')
                    continue
                username: str = tweet['user']['screen_name']
                if not username in user_count:
                    user_count[username] = 0

                if user_count[username] < MAX_VOTES:
                    user_count[username] += 1
                    tale_id = int(tweet['full_text'].split(' ')[2][1:])
                    if not c.has_tale(tale_id):
                        continue
                    if not tale_id in votes:
                        votes[tale_id] = 0
                    votes[tale_id] += 1
            except:
                continue

        return votes
    except KeyError:
        return {}


module_init()
