import json


DIR = './db/'
QUESTIONS = 'questions.json'
CONTESTS = 'contests.json'
TALES = 'tales.json'



def save_list_of_records(records, target: str):
    """ Accede al db per salvare la lista di records passati in input.
        Questa è da intendersi come una funzione privata e non dovrebbe essere
        chiamata al di fuori di questo modulo.

        Parametri
        ---------
        records: list[dict]
            La lista di record da dover salvare

        target: str
            Il path del file da accedere"""
    file = open(target, 'w')
    file.seek(0)
    json.dump(records, file)
    file.close()


def load_list_of_records(target: str) :
    """ Accede al db per caricare una lista di record dal file specificato.
        Questa è da intendersi come una funzione privata e non dovrebbe essere
        chiamata al di fuori di questo modulo.

        Parametri
        ---------
        target: str
            Il path del file da accedere

        Ritorna
        -------
        La lista dei record trovati"""
    file = open(target, 'r')
    records = json.load(file)
    file.close()
    return records


def questions_path():
    return f'{DIR}{QUESTIONS}'


def save_questions(questions):
    """ Accede al db per sovrascrivere le domande trivia con quelle passate
        in input

        Parametri
        ---------
        questions : list[dict]
            Lista dei record delle domande da salvare nel db"""
    save_list_of_records(questions, questions_path())


def load_questions() :
    """ Accede al db in modo da caricare la lista di record di domande
        trivia registrate.

        Ritorna
        -------
        Una lista di dizionari da usare per poter istanziare le domande"""
    return load_list_of_records(questions_path())


def tales_path():
    return f'{DIR}{TALES}'


def save_tales(tales):
    """ Accede al db per sovrascrivere la lista di racconti con quelli passati
        in input

        Parametri
        ---------
        tales : list[dict]
            Lista dei record dei racconti da salvare nel db"""
    save_list_of_records(tales, tales_path())


def load_tales():
    """ Accede al db in modo da caricare la lista di record di domande
        trivia registrate.

        Ritorna
        -------
        Una lista di dizionari da usare per poter istanziare le domande"""
    return load_list_of_records(tales_path())


def contests_path():
    return f'{DIR}{CONTESTS}'


def save_contests(contests):
    save_list_of_records(contests, contests_path())

def load_contests():
    return load_list_of_records(contests_path())
