import tweepy
import requests
import keys
from random import randrange

MAX_TWEETS = 100


def is_retweet(tweet):

    try:
        #prova a sollevare un'eccezione accedendo a campi definiti
        #sse si tratta di un retweet
        tweet.retweeted_status.full_text
        print('ATTENZIONE CAZZOOOOO QUA CE UN RETWEET')
        return True

    except AttributeError:
        return False


def text_from_dict(tweet_dict):
    """ Ritorna il testo contenuto del tweet sotto forma di dizionario, così
        come è creato dalla funzione dictify_single_tweet. Nel caso il tweet
        dovesse essere quello di un retweet ritorna il testo del tweet
        originale"""
    if is_retweet(tweet_dict):
        return tweet_dict['retweeted_status.full_text']
    else:
        return tweet_dict['full_text']


def dictify_place(place: str):
    if place != None:
        place_dict = {}
        x = place.partition(",")
        posti_lat = float(x[0])
        posti_long = float(x[2])
        print(posti_lat)
        print(posti_long)
        diff_lat = randrange(-50, 50)
        diff_long = randrange(-50, 50)
        posti_lat = posti_lat+(diff_lat/1000)
        posti_long = posti_long+(diff_long/1000)
        print(posti_lat)
        print(posti_long)
        place_dict['lat'] = posti_lat
        place_dict['long'] = posti_long
        return place_dict


def dictify_user(user):
    """ Ritorna una rappresentazione in forma di dizionario di python
        del record di user ottenuto dallo status di un tweet"""
    user_dict = {}
    user_dict['screen_name'] = user.screen_name
    user_dict['profile_image_url_https'] = user.profile_image_url_https
    return user_dict


def dictify_single_tweet(tweet, place):
    """ Ritorna una rappresentazione in forma di dizionario di python
        dello status di tweet"""

    tweet_dict = {}
    tweet_dict['user'] = dictify_user(tweet.user)
    if place == "a":
        tweet_dict['place'] = ""
    else:
        tweet_dict['place'] = dictify_place(place)

    if is_retweet(tweet):
        tweet_dict['retweeted_status'] = dictify_single_tweet(
            tweet.retweeted_status)
    else:
        tweet_dict['full_text'] = tweet.full_text

    return tweet_dict


def listify_tweets(tweets, place):
    """ Ritorna una rappresentazione in forma di dizionario di python
        di tweets. Il dizionario è indicizzato su interi da 0 a n come
        fosse una lista"""
    tweets_list = []

    for tweet in tweets:
        tweet_dict = dictify_single_tweet(tweet, place)
        tweets_list.append(tweet_dict)

    return tweets_list


def printTweet(tweet):
    #print('////////////////////////////////////////')
    if tweet.place:

        """#print("Place:")
        print(tweet.place.bounding_box.coordinates[0][1])
        posti_long1=(tweet.place.bounding_box.coordinates[0][0][0] + tweet.place.bounding_box.coordinates[0][1][0])/2
        posti_lat1=(tweet.place.bounding_box.coordinates[0][0][1]+tweet.place.bounding_box.coordinates[0][1][1])/2
        posti_long2=(tweet.place.bounding_box.coordinates[0][2][0]+tweet.place.bounding_box.coordinates[0][3][0])/2
        posti_lat2=(tweet.place.bounding_box.coordinates[0][2][1]+tweet.place.bounding_box.coordinates[0][3][1])/2
        posti_long=(posti_long1+posti_long2)/2
        posti_lat=(posti_lat1+posti_lat2)/2
        print(posti_long)
        print(posti_lat)"""

        #print(tweet.place.bounding_box.coordinates[0][0])
        print(f'@{tweet.user.screen_name}')
        #quando fai la richiesta con tweet_mode=extended il testo sta nel campo full_text
        try:

            print("------")
            print(
                f'è un retweet di @{tweet.retweeted_status.user.screen_name}')
            print(tweet.retweeted_status.full_text)

        #se non è un retweet retweeted_status non è definito e si entra qui dentro
        except AttributeError:
            print(tweet.full_text)
        print('////////////////////////////////////////')
        print(end='\n\n')


#autorizzazione via tweepy con informazioni di accesso
auth = tweepy.OAuthHandler(keys.consumer_key(), keys.consumer_secret())
auth.set_access_token(keys.access_token(), keys.access_token_secret())
#oggetto API per interazione con twitter
api = tweepy.API(auth)
#public_tweets: tweepy.models.ResultSet = api.home_timeline()


def make_query(query: str, amount: int = MAX_TWEETS):
    """ Helper function che effettua effettivamente la richiesta ai server
        di twitter e ritorna una lista di dizionari che rappresentano gli
        oggetti"""
    found_tweets = api.search_tweets(
        query, tweet_mode='extended', count=amount)
    return listify_tweets(found_tweets, "a")


def search_by_content(content: str, amount: int = MAX_TWEETS, remove_user: bool = True):
    """ Interroga l'API di twitter per la ricerca di tweet che nel loro testo
        includono content. Il numero di tweet richiesti è specificato da amount
        settato di default a MAX_TWEETS, il massimo; qualsiasi quantitativo
        superiore sarà limitato a MAX_TWEETS.
        I tweets sono ritornati in una lista sottoforma di dizionario"""
    query = content
    if remove_user:
        query += f' -from:{content}'
    query += ' -filter:retweets'

    return make_query(query, amount)


def search_by_username(username: str, amount: int = MAX_TWEETS):
    """ Interroga l'API di twitter per la ricerca di tweet postati dall'account
        username. Il numero di tweet richiesti è specificato da amount
        settato di default a MAX_TWEETS, il massimo; qualsiasi quantitativo
        superiore sarà limitato a MAX_TWEETS.
        I tweets sono ritornati in una lista sottoforma di dizionario"""
    query = f'from:{username} -filter:retweets'
    return make_query(query, amount)


def search_by_username_with_content(username: str, content: str, amount: int = MAX_TWEETS):
    query = f'{content} from:{username} -filter:retweets'
    return make_query(query, amount)


def search_by_hashtag(hashtag: str, amount: int):
    query = f'from:{hashtag} - filter:retweets'
    """
    found_tweets = api.search_tweets(q = hashtag, tweet_mode = 'extended', count = amount)
    for tweet in found_tweets:
        printTweet(tweet)
    return listify_tweets(found_tweets)
    """
    return make_query(query, amount)


def search_votes(contest):
    """
    Raccoglie tutti i voti del contest di id ''contest'' e li ritorna sotto forma di stringa

    in seconda battuta va aggiunto il controllo che per ogni nome utente vanno presi solo gli ultimi 10 tweet che ha fatto
    """
    d = search_by_content(f'#IngSof2021vote #{contest}')
    return d


def get_coordinates(place: str):

    url = "https://nominatim.openstreetmap.org/search?q=" + place + "&format=geojson"
    payload = {}
    headers = {
        'User-Agent': 'My User Agent 1.0',
        'From': 'youremail@domain.com'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    tmp = response.json()
    print(tmp['features'][0]['geometry']['coordinates'])
    return(tmp['features'][0]['geometry']['coordinates'])


def search_by_geotag(place: str, amount: int):
    """"
    la query in input deve essere del tipo "lat, long, rad", es "40.730610, -73.935242, 1mi"
    "40.7127281, -74.0060152, 1mi"
    """
    coordinates = get_coordinates(place)
    long = coordinates[0]
    lat = coordinates[1]
    coordinate = str(lat) + "," + str(long) + "," + "6mi"
    coordinate_tweet = str(lat) + "," + str(long)
    print(coordinate)
    tmp = coordinate

    query = f'-filter:retweets'
    found_tweets = api.search_tweets(
        query, geocode=tmp, tweet_mode='extended', count=amount)

    """print("ao")
    for i in found_tweets:
        printTweet(i)"""

    return listify_tweets(found_tweets, coordinate_tweet)
