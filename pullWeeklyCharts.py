import requests
import apiKey
import xml.etree.ElementTree as ET
import csv
import json
import os.path

#getting apiKey from local file
apiKey = apiKey.apiKey


def getWeeklyCharts(user):        
        parameter = {'method':'user.getweeklychartlist', 'user': user, 'api_key':apiKey}
        root = requests.get('https://ws.audioscrobbler.com/2.0', params=parameter)
        with open('weeklyCharts.xml', 'wb') as f:
                f.write(root.content)

def parseXML(xml):
        #parse weeklyCharts.xml into charts tree 
        tree = ET.parse(xml)
        root = tree.getroot()
        charts =[]

        for chart in root.findall('./weeklychartlist/'):
                chartData = {}
                chartData['from'] = chart.get('from')
                chartData['to'] = chart.get('to')
                charts.append(chartData)
        print("Charts pulled from weeklyCharts.xml")
        return charts


def saveCSV(charts):
        fields = ['from','to']
        with open('charts.csv', 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fields)
                writer.writeheader()
                writer.writerows(charts)
        print("XML data written in charts.csv")

def saveJSON():
        with open('./topTracks.json', 'r') as file:
                data = json.load(file)
                print(data)
        
                

def main():
        username = input('Last.fm user: ')
        getWeeklyCharts(username)
        charts = parseXML('weeklyCharts.xml')
        saveCSV(charts)

saveJSON()
