import requests
import apiKey

apiKey = apiKey.apiKey

def getWeeklyCharts(user):
        parameter = {'method':'user.getweeklychartlist', 'user': user, 'api_key':apiKey}
        root = requests.get('https://ws.audioscrobbler.com/2.0', params=parameter)
        print(root.text)

username = input('Last.fm user: ')
getWeeklyCharts(username)
