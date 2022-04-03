import random

import dbmanager
import twitter_client as tc


QUESTION_TAG: str = '#IngSof2021qst'
ANSWER_TAG: str = '#IngSof2021ans'


class Question:
    def __init__(self, id: str, quiz: str, right: str, wrongs):
        self._id: str = id
        self._quiz: str = quiz
        self._right: str = right
        self._wrongs: list[str] = wrongs
        answers = wrongs
        answers.append(right)
        random.shuffle(answers)
        self._answers: list[str] = answers
        print(self._answers)

    @property
    def id(self):
        return self._id

    @property
    def quiz(self):
        return self._quiz

    @property
    def right(self):
        return self._right

    @property
    def answers(self):
        return self._answers

    @property
    def suggested_text(self):
        text: str = f'{QUESTION_TAG} #{self.id} {self.quiz}\n'
        for i in range(len(self.answers)):
            text += f'{i}) {self.answers[i]}\n'

        return text

    def is_right_answer(self, n: int):
        return self.answers[n] == self.right

    def toDict(self):
        retVal = {}
        retVal['id'] = self.id
        retVal['quiz'] = self.quiz
        retVal['right'] = self.right
        retVal['answers'] = self.answers
        retVal['suggested_text'] = self.suggested_text
        return retVal

    @staticmethod
    def fromDict(d: dict):
        q = Question('', '', '', [])
        q._id = d['id']
        q._quiz = d['quiz']
        q._right = d['right']
        q._answers = d['answers']
        q._wrongs = q.answers.copy()
        q._wrongs.remove(q.right)

        return q


questions = {}
next_id: int = 0
initialized: bool = False


def get_dict_list():
    l = []
    for question in questions.values():
        l.append(question.toDict())
    return l


def module_init():
    global questions, next_id, initialized

    if not initialized:
        questions_list = dbmanager.load_questions()
        for question in questions_list:
            questions[question['id']] = Question.fromDict(question)
            next_id = max(next_id, int(question['id'], base=16))
        print(questions)
        next_id += 1
        initialized = True


def save_questions():
    questions_list = get_dict_list()
    dbmanager.save_questions(questions_list)


def add_question(quiz: str, right: str, wrongs) -> Question:
    global next_id, questions
    new_question: Question = Question(hex(next_id)[2:], quiz, right, wrongs)
    questions[new_question.id] = new_question
    next_id += 1
    save_questions()

    return new_question


def is_registered(id: str):
    return id in questions.keys()


def total_score(answers: dict):
    score: int = 0
    seen = []
    for answer in answers:
        text: str = tc.text_from_dict(answer)
        words = text.split(' ')
        try:
            #il tweet di risposta dev'essere nella forma ANSWER_TAG #id_trivia risposta
            #per cui il controllo della validità dell'id passa tramite words[1]
            id: str = words[1][1:]
            if is_registered(id) and id not in seen:
                trivia: Question = questions[id]
                seen.append(id)
                if trivia.is_right_answer(int(words[2])):
                    score += 1
            else:
                continue
        except:
            continue

    return score


module_init()
