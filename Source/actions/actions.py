# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from xml.etree import ElementTree

import requests
import sqlite3

database_path = "actions/mydb.db"

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_latest_race_result"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Getting the info for latest race using GET and storing result
        response = requests.get('http://ergast.com/api/f1/current/last/results.json').json()
        data_result = response['MRData']

        # Parsing the obtained data
        raceTrackLocation = data_result['RaceTable']['Races'][0]['Circuit']['circuitId']
        raceTrackName = data_result['RaceTable']['Races'][0]['Circuit']['circuitName']
        raceYear = data_result['RaceTable']['season']
        raceRound = data_result['RaceTable']['round']

        standings_list = []

        # Only get the podium finishes
        for i in range(3):
            constructor = data_result['RaceTable']['Races'][0]['Results'][i]['Constructor']['name']
            driverFirstName = data_result['RaceTable']['Races'][0]['Results'][i]['Driver']['givenName']
            driverLastName = data_result['RaceTable']['Races'][0]['Results'][i]['Driver']['familyName']
            driverNumber = data_result['RaceTable']['Races'][0]['Results'][i]['Driver']['permanentNumber']
            pointsObtained = data_result['RaceTable']['Races'][0]['Results'][i]['points']
            position = data_result['RaceTable']['Races'][0]['Results'][i]['position']

            temp_dict = {}
            for var in ["driverFirstName", "driverLastName", "driverNumber", "constructor", "pointsObtained", "position"]:
                temp_dict[var] = eval(var)

            standings_list.append(temp_dict)

        utter_text = "Here's the latest race result:\nRace " + raceRound + ", season " + raceYear + ", took place at " + raceTrackLocation + ", at " + raceTrackName + " circuit\n"
        utter_text += "Standings:\n" 

        for item in standings_list:
            utter_text += "Position " + item['position'] + ", points obtained : " + item['pointsObtained'] + " - Driver: " + item['driverFirstName'] + " " + item['driverLastName'] + ", Number: " + item['driverNumber'] + ", driving for " + item['constructor']  + ".\n"

        utter_text += "__________________________________"

        dispatcher.utter_message(text=utter_text)
        return []


class ActionQualify(Action):

    def name(self) -> Text:
        return "action_latest_qualify_result"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Getting the info for latest race using GET and storing result
        response = requests.get('http://ergast.com/api/f1/2022/4/qualifying.json').json()
        data_result = response['MRData']

        # Parsing the obtained data
        raceTrackLocation = data_result['RaceTable']['Races'][0]['Circuit']['circuitId']
        raceTrackName = data_result['RaceTable']['Races'][0]['Circuit']['circuitName']
        raceYear = data_result['RaceTable']['season']
        raceRound = data_result['RaceTable']['round']

        standings_list = []

        # Get the entire grid results for qualifying
        for i in range(len( data_result['RaceTable']['Races'][0]['QualifyingResults'])):
            constructor = data_result['RaceTable']['Races'][0]['QualifyingResults'][i]['Constructor']['name']
            driverFirstName = data_result['RaceTable']['Races'][0]['QualifyingResults'][i]['Driver']['givenName']
            driverLastName = data_result['RaceTable']['Races'][0]['QualifyingResults'][i]['Driver']['familyName']
            driverNumber = data_result['RaceTable']['Races'][0]['QualifyingResults'][i]['Driver']['permanentNumber']
            position = data_result['RaceTable']['Races'][0]['QualifyingResults'][i]['position']

            if "Q1" in data_result['RaceTable']['Races'][0]['QualifyingResults'][i]:
                q1 = data_result['RaceTable']['Races'][0]['QualifyingResults'][i]['Q1']
            else:
                q1 = "NA"
            if "Q2" in data_result['RaceTable']['Races'][0]['QualifyingResults'][i]:
                q2 = data_result['RaceTable']['Races'][0]['QualifyingResults'][i]['Q2']
            else: 
                q2 = "NA"
            if "Q3" in data_result['RaceTable']['Races'][0]['QualifyingResults'][i]:
                q3 = data_result['RaceTable']['Races'][0]['QualifyingResults'][i]['Q3']
            else: 
                q3 = "NA"

            temp_dict = {}
            for var in ["driverFirstName", "driverLastName", "driverNumber", "constructor", "position", "q1", "q2", "q3"]:
                temp_dict[var] = eval(var)

            standings_list.append(temp_dict)

        utter_text = "Here's the latest qualifying result:\nRace " + raceRound + ", season " + raceYear + ", took place at " + raceTrackLocation + ", at " + raceTrackName + " circuit\n"
        utter_text += "Standings:\n" 

        for item in standings_list:
            utter_text += "Position " + item['position'] + ", Driver: " + item['driverFirstName'] + " " + item['driverLastName'] + ", Number: " + item['driverNumber'] + ", driving for " + item['constructor']  + ".\n"
            utter_text += "Qualifying times:\nQ1 : " + item['q1'] + "\nQ2 : " + item['q2'] + "\nQ3 : " + item['q3'] + "\n\n"
        utter_text += "__________________________________"

        dispatcher.utter_message(text=utter_text)
        return []

class ActionFeedbackForm(Action):

    def name(self) -> Text:
        return "action_feedback_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        # Creating table if not exists
        cursor.execute("CREATE TABLE IF NOT EXISTS dataTable (firstName CHAR, lastName CHAR, feedback CHAR)")

        # Extracting the slots (related to feedback form)
        extract_firstName = tracker.get_slot("firstName")
        extract_lastName = tracker.get_slot("lastName") 
        extract_feedback = tracker.get_slot("feedback")

        # Inserting values into the table
        query_string = "INSERT INTO dataTable VALUES ('" + extract_firstName + "','" + extract_lastName + "','" + extract_feedback + "')"
        cursor.execute(query_string)

        dispatcher.utter_message(text="Thank you for your feedback! I have submitted your form.")
        return []

class ActionLatestSchedule(Action):

    def name(self) -> Text:
        return "action_latest_race_schedule"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Getting the info for latest race using GET and storing result
        response = requests.get('http://ergast.com/api/f1/current.json').json()
        data_result = response['MRData']

        race_list = []

        current_season = data_result['RaceTable']['season']

        # Get the race schedule
        for i in range(len( data_result['RaceTable']['Races'])):
            raceNo = data_result['RaceTable']['Races'][i]['round']
            race_track = data_result['RaceTable']['Races'][i]['Circuit']['circuitName']
            country = data_result['RaceTable']['Races'][i]['Circuit']['Location']['country']
            fp1 = data_result['RaceTable']['Races'][i]['FirstPractice']['date']
            fp2 = data_result['RaceTable']['Races'][i]['SecondPractice']['date']

            if "ThirdPractice" in data_result['RaceTable']['Races'][i]:
                fp3 = data_result['RaceTable']['Races'][i]['ThirdPractice']['date']
            else:
                fp3 = data_result['RaceTable']['Races'][i]['Sprint']['date'] + "(Sprint)"
            qualifying = data_result['RaceTable']['Races'][i]['Qualifying']['date']
            raceday = data_result['RaceTable']['Races'][i]['date']
            racename = data_result['RaceTable']['Races'][i]['raceName']
            time = data_result['RaceTable']['Races'][i]['time']

            temp_dict = {}
            for var in ["raceNo", "racename", "race_track", "country", "fp1", "fp2", "fp3", "qualifying", "raceday", "time"]:
                temp_dict[var] = eval(var)

            race_list.append(temp_dict)

        utter_text = "Here's the schedule for the latest season:\n\n"

        for item in race_list:
            utter_text += "Season : " + current_season + "  round " + item['raceNo'] + ", " + item['racename'] + " at " + item['race_track'] + ", " + item['country'] + "\n"
            utter_text += "Free Practice Dates ---> FP1 : " + item['fp1'] + ", FP2 : " + item['fp2'] + ", FP3 : " + item['fp3'] + "\n"
            utter_text += "Race Day---> Date : " + item['raceday'] + ", Time : " + item['time'] + "\n\n"
        utter_text += "__________________________________"

        dispatcher.utter_message(text=utter_text)
        return []