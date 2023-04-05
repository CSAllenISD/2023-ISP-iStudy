import requests
import apiKey
import xml.etree.ElementTree as ET
import csv

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
        weeklyTracks = []

        #weeklyTracks = [from, to, song 1, song 2, ...]
        weeklyTracks.append(root.find('weeklytrackchart').get('from'))
        weeklyTracks.append(root.find('weeklytrackchart').get('to'))

        #each song is a dictionary w/rank, title, artist, & url
        songEntry = 0
        for track in root.findall('./weeklytrackchart/'):
                #only do first 10 instances
                songEntry +=1
                
                song = {}
                song[track.get('rank')] = track.get('rank')
                song['name'] = track.find('name').text
                song['artist'] = track.find('artist').text
                song['url'] = track.find('url').text
                weeklyTracks.append(song)

                if songEntry == 10:
                        break

        #ONLY RETURN IF NOT EMPTY!
        if len(weeklyTracks) > 2:
                return weeklyTracks


def saveCSV(rows):
        fields = ['from','to']
        for x in range(10):
                fields.append("song "+str(x))
        fieldWrapper = [fields]

        with open('topTracks.csv', 'w') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(fieldWrapper)
                writer.writerows(rows)
        print("XML data written in topTracks.csv")

def main():
        username = input('Last.fm user: ')
        dates = getDates()

        #array of weeklyTopTracks; all Top Tracks
        totalTopTracks = []
        
        for date in range(len(dates)):
                #get the .getWeeklyAlbumChart XML
                getWeeklyTracks(username, dates[date])

                #get first 10 tracks from XML
                weeklyTopTracks = parseXML('weeklyTracks.xml')

                #percent complete
                percent = round(date * 100 / len(dates))
                print(str(round(percent,2)) + "% done parsing XMLs")
                
                #add the weekly top tracks to total
                if weeklyTopTracks:
                        totalTopTracks.append(weeklyTopTracks)
    
        #save totalTopTracks to topTracks.csv
        saveCSV(totalTopTracks)

main()
