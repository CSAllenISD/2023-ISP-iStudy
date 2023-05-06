import requests
import apiKey
import xml.etree.ElementTree as ET
import csv
import json
import os.path

#getting apiKey from local file
apiKey = apiKey.apiKey

#gets chart date from charts.csv
def getDates():
        file = open('charts.csv')
        csvreader = csv.reader(file)

        header = []
        header = next(csvreader)
        rows = []
        for row in csvreader:
                rows.append(row)
        file.close()
        return rows
        


def getWeeklyTracks(user, date):        
        parameter = {'method':'user.getweeklytrackchart', 'user': user, 'api_key':apiKey, 'from':date[0], 'to':date[1]}
        root = requests.get('https://ws.audioscrobbler.com/2.0', params=parameter)
        with open('weeklyTracks.xml', 'wb') as f:
                f.write(root.content)

def parseXML(xml):
        #parse weeklyTracks.xml into charts tree 
        tree = ET.parse(xml)
        root = tree.getroot()

        #open JSON, create if new, write if old
        if os.path.isfile('./topTracks.json') == True:
                with open('./topTracks.json', 'r') as file:
                        data = json.load(file)
        else:
                data = []
        #data has all current song data, either none or from preexisting JSON


        #for each song, make or find a dict
        songEntry = 0
        for track in root.findall('./weeklytrackchart/'):
                songEntry +=1
                needNewSong = bool(True)
                for song in data:
                        #check if song already exists in data[]
                        if song['name'] == str(track.find('name').text):
                                #only add date object to data property of song dict
                                addData = {
                                        #always use "TO" for dates not FROM
                                        "date" : int(root.find('weeklytrackchart').get('to')),
                                        "rank" : int(track.get('rank'))
                                }
                                song['data'].append(addData)
                                needNewSong = bool(False)

                if needNewSong == bool(True):
                        newSong = {
                                #mbid & image needed
                                "name" : str(track.find('name').text),
                                "artist" : str(track.find('artist').text),
                                "url" : str(track.find('url').text),
                                "data" : [{
                                        "date" : int(root.find('weeklytrackchart').get('to')),
                                        "rank" : int(track.get('rank'))
                                }]
                        }
                        data.append(newSong)
                                
                if songEntry == 10:
                       break
        #overwrite data[] to topTracks.json
        if len(data) > 0:
                with open('./topTracks.json', 'w', encoding='utf-8') as file:
                        json.dump(data, file, indent=4)

def main():
        username = input('Last.fm user: ')
        dates = getDates()

        #array of weeklyTopTracks; all Top Tracks
        totalTopTracks = []
        
        #reset JSON
        if os.path.exists('./topTracks.json'):
                os.remove('./topTracks.json')

        for date in range(len(dates)):
                #get the .getWeeklyAlbumChart XML
                getWeeklyTracks(username, dates[date])
        
                #get first 10 tracks from XML
                weeklyTopTracks = parseXML('weeklyTracks.xml')

                #percent complete
                percent = round(date * 100 / len(dates))
                previousPercent = round((date-1) * 100 / len(dates))
                if percent != previousPercent:
                        print(str(round(percent,2)) + "% done parsing XMLs")
                
                #add the weekly top tracks to total
                if weeklyTopTracks:
                        totalTopTracks.append(weeklyTopTracks)

main()
