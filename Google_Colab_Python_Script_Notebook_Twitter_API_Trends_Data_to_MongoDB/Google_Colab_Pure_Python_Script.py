# Installazione delle librerie necessarie

# !pip install --user dnspython
# !pip install --user twitter

# Importazione delle librerie

import pymongo
import dns  # necessario per una connessione MongoDB con SRV
import twitter
import time
from datetime import datetime

# Configurazione del database MongoDB, delle collezioni e utenti
dbURI = "mongodb+srv://ilmiocluster.wzfj1.mongodb.net"
dbName = "Database_del_Progetto"
collectionNameTrendingTopics = "Trending_Topics"
collectionNameAvailableLocations = "Available_locations"
dbUsername = ""
dbPassword = ""
localJsonDataFile = "data.json"

# Configurazione delle access keys all'API di Twitter
API_key = ''
API_secret = ''
accessToken = ''
accessTokenSecret = ''

# Configurazione del tempo in secondi per il reset della rate limit di requests all'API di twitter
seconds_to_reset = 15 * 60  # 15 minuti

""" Definizione delle funzioni di connessione, pulizia di una collection, rinomina e stampa """


# Connect to a MongoDB database
def connectToDB(uri, uname, pword):
    return pymongo.MongoClient(uri, username=uname, password=pword)


# Pulizia delle collection
def cleanCollection(collection):
    collection.delete_many({})


# Rinomina collection
def renameCollection(oldCollection, newCorrectionName):
    oldCollection.rename(newCorrectionName)


# Stampa contenuto di una collection
def printCollectionData(collection):
    for elemento in collection.find():
        print(elemento)


# Funzione di controllo che dato un trending topic di una certa
# location in una certa data, controlla che non sia già presente
# in una collection
def checkIfPresent(collection, trendingTopicRecord):
    data = trendingTopicRecord['created_at'][0:10]
    woeid = trendingTopicRecord['locations_woeid']
    trendName = trendingTopicRecord['name']
    presentRecord = collection.find({"$and": [{'created_at': {"$regex": str(data) + '.*'}},
                                              {'locations_woeid': woeid},
                                              {'name': trendName}]})
    for records in presentRecord:
        return True
    return False


# Definizione di una funzione che data una location, l'API di twitter, una
# collection delle TT e i tempi da una request all'altra all'API di Twitter
# e di reset delle rate limit, inserisce le trending topics in tale collezione
def getAndAddTrendingTopics(location,
                            api_di_twitter,
                            collezione_delle_trending_topics,
                            seconds_between_each_app_request_arg,
                            seconds_to_reset_arg):
    rate_status_trends = api_di_twitter.application.rate_limit_status()['resources']['trends']['/trends/place']
    time.sleep(seconds_between_each_app_request_arg)  # wait for trends request time
    # print("seconds_between_each_app_request   ", seconds_between_each_app_request_arg)
    limit_trends = rate_status_trends['limit']
    remaining_limit_trends = rate_status_trends['remaining']
    seconds_between_each_trends_request = seconds_to_reset_arg / limit_trends
    # print("remaining_limit_trends             ", remaining_limit_trends)
    # print("seconds_between_each_trends_request", seconds_between_each_trends_request)

    while remaining_limit_trends <= 1:
        remaining_limit_trends = \
            api_di_twitter.application.rate_limit_status()['resources']['trends']['/trends/place']['remaining']
        time_to_wait = 0 if remaining_limit_trends > 1 else max(seconds_between_each_trends_request,
                                                                seconds_between_each_app_request_arg)
        time.sleep(time_to_wait)  # wait for trends or app request time
        # print("seconds_between_each_app_trend_req ", time_to_wait)
        # print("remaining_limit_trends             ", remaining_limit_trends)

    trendsDataJsonText = api_di_twitter.trends.place(_id=location['woeid'])
    time.sleep(max(seconds_between_each_trends_request - seconds_between_each_app_request_arg,
                   0))  # wait for trends request time - app request time
    trends = trendsDataJsonText[0]['trends']
    dateTimeNow = datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ')
    metadata = {
        "as_of": trendsDataJsonText[0]['as_of'],
        "created_at": str(dateTimeNow),
        "locations_name": location['name'],
        "location_type": location['placeType']['name'],
        "locations_woeid": location['woeid'],
        "parent_id": location['parentid'],
        "parent_name": "Worldwide" if location['placeType']['name'] == "Country" else location[
            'country']
    }
    for trend in trends:
        record = {**metadata, **trend}
        if not checkIfPresent(collezione_delle_trending_topics,
                              record):  # controlla che tale trending topic non sia già in db
            collezione_delle_trending_topics.insert_one(record)


# Definizione di una funzione che dato l'API di Twitter, la collection delle
# trending topics e delle available locations, dei tempi di secondi tra ogni
# request e di reset delle rate limit, prende dall'API di twitter i dati e
# inserisce senza duplicati le available locations con trends e i rispettivi
# trending topics nelle due collections.
def getAndAddAvailableLocationsAndTrendingTopics(api_di_twitter,
                                                 collezione_trending_topics,
                                                 collezione_available_locations,
                                                 secondsBetweenEachAppRequestArg,
                                                 secondsToReset):
    dateNow = datetime.today().strftime('%Y-%m-%d')
    dateTimeNow = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    woiedsWhereTrendsAvailable = api_di_twitter.trends.available()

    for availableLocation in woiedsWhereTrendsAvailable:

        print("Adding", availableLocation['name'], "to the available locations collection.")

        # Inserimento locations in available locations collection
        locationRecord = {"locations_name": "Worldwide", "locations_woeid": 1, "countries": []}
        locationInDBquery = collezione_available_locations.find({'dateTime': {"$regex": str(dateNow) + '.*'}})

        locationInDB = ""
        for item in locationInDBquery:
            locationInDB = item

        if len(locationInDB) == 0:  # empty locationInDB
            if availableLocation['placeType']['name'] != "Supername":
                if availableLocation['placeType']['name'] == "Country":
                    locationRecord['countries'] = [
                        {"locations_name": availableLocation['name'], "locations_woeid": availableLocation['woeid'],
                         "towns": []}]
                else:  # it's a town
                    locationRecord['countries'] = \
                        [
                            {
                                "locations_name": availableLocation['country'],
                                "locations_woeid": availableLocation['parentid'],
                            }
                        ]
                    towns = {"towns": [{"locations_name": availableLocation['name'],
                                        "locations_woeid": availableLocation['woeid']}]}
                    locationRecord = {**locationRecord['countries'][0], **towns}
            jsonRecord = {"dateTime": dateTimeNow, "locations": locationRecord}
            collezione_available_locations.insert_one(jsonRecord)
        else:  # locationInDB is not empty, contains locations
            if availableLocation['placeType']['name'] != "Supername":
                if availableLocation['placeType']['name'] == "Country":
                    # check if country is present
                    alreadyPresent = False
                    for country in locationInDB['locations']['countries']:
                        if country['locations_woeid'] == availableLocation['woeid']:
                            alreadyPresent = True
                    # if country is not present add it
                    if not alreadyPresent:
                        newCountry = {"locations_name": availableLocation['name'],
                                      "locations_woeid": availableLocation['woeid'], "towns": []}
                        locationInDB['locations']['countries'] = locationInDB['locations']['countries'] + [newCountry]
                        jsonRecord = {"dateTime": dateTimeNow, "locations": locationInDB['locations']}
                        collezione_available_locations.delete_one({'dateTime': {"$regex": str(dateNow) + '.*'}})
                        collezione_available_locations.insert_one(jsonRecord)
                else:  # if it's a town
                    # check if the town is present
                    alreadyPresentCountry = False
                    for country in locationInDB['locations']['countries']:
                        # check first if the country is present
                        if country['locations_woeid'] == availableLocation['parentid']:
                            alreadyPresentCountry = True
                            alreadyPresentTown = False
                            # Country is present, check if town is present
                            for town in country['towns']:
                                if town['locations_woeid'] == availableLocation['woeid']:
                                    alreadyPresentTown = True
                            # if country present but town not present, add town
                            if not alreadyPresentTown:
                                newTown = {"locations_name": availableLocation['name'],
                                           "locations_woeid": availableLocation['woeid']}
                                country['towns'] = country['towns'] + [newTown]
                                jsonRecord = {"dateTime": dateTimeNow, "locations": locationInDB['locations']}
                                collezione_available_locations.delete_one({'dateTime': {"$regex": str(dateNow) + '.*'}})
                                collezione_available_locations.insert_one(jsonRecord)
                    # if country not present, add country and town
                    if not alreadyPresentCountry:
                        newCountry = {"locations_name": availableLocation['country'],
                                      "locations_woeid": availableLocation['parentid'], "towns": []}

                        newTown = {"locations_name": availableLocation['name'],
                                   "locations_woeid": availableLocation['woeid']}
                        newCountry['towns'] = [newTown]
                        locationInDB['locations']['countries'] = locationInDB['locations']['countries'] + [newCountry]
                        jsonRecord = {"dateTime": dateTimeNow, "locations": locationInDB['locations']}
                        collezione_available_locations.delete_one({'dateTime': {"$regex": str(dateNow) + '.*'}})
                        collezione_available_locations.insert_one(jsonRecord)

        getAndAddTrendingTopics(availableLocation,
                                twitterAPI,
                                collezione_trending_topics,
                                secondsBetweenEachAppRequestArg,
                                secondsToReset)  # inserisci i trends


# Creazione delle connessioni all'API di twitter e a MongoDB ed esecuzione
# delle operazioni di inserimento nelle collections delle locations con
# available trending topics e i rispettivi TT.

authentication = twitter.oauth.OAuth(accessToken, accessTokenSecret, API_key, API_secret)
twitterAPI = twitter.Twitter(auth=authentication)

client = connectToDB(dbURI, dbUsername, dbPassword)
db = client[dbName]
collezioneTrendingTopics = db[collectionNameTrendingTopics]
collezioneAvailableLocations = db[collectionNameAvailableLocations]

# cleanCollection(collezioneTrendingTopics)
# printCollectionData(collezioneTrendingTopics)

rate_status_app = \
    twitterAPI.application.rate_limit_status()['resources']['application']['/application/rate_limit_status']
limit_app = rate_status_app['limit']
remaining_limit_app = rate_status_app['remaining']
# print("remaining_limit_app                ", remaining_limit_app)
seconds_between_each_app_request = seconds_to_reset / limit_app

getAndAddAvailableLocationsAndTrendingTopics(twitterAPI,
                                             collezioneTrendingTopics,
                                             collezioneAvailableLocations,
                                             seconds_between_each_app_request,
                                             seconds_to_reset)
