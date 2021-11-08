# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import json
import os



DATA = {}
file_loaded = False

class ManageFile():

    def loadData():
        global DATA, file_loaded
        if not os.path.exists('data.json'):
            with open('data.json', 'w') as file:
                json.dump({}, file)
                pass 
        try:
            file = open("data.json", "r+")
            data_read = file.read()
            DATA = json.loads(data_read)
            file.close()
            print("File Loaded")
            file_loaded = True
        except FileNotFoundError:
            print("Error during file loading")
            return 

    def writeData():
        file = open("data.json", "w")
        json.dump(DATA, file)
        file.close()


class UpdateElement(Action):

    def name(self) -> Text:
        return "update_element"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        if file_loaded is False:
            ManageFile.loadData()
        
        element = tracker.get_slot("element")
        quantity = tracker.get_slot("quantity")

        print("\nElement:",element)
        print("Quantity:",quantity)

        
        if element in DATA:
            old_quantity = DATA[element]
            new_quantity = str(int(old_quantity) + int(quantity))
            DATA[element] = new_quantity
        else:
            DATA[element] = quantity
        
        
        ManageFile.writeData()
        
        dispatcher.utter_message(text="List updated.") 

        return [SlotSet("element", None), SlotSet("quantity", None)]


class DisplayList(Action):
    def name(self) -> Text:
        return "display_list"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        if file_loaded is False:
            ManageFile.loadData()

        
        if DATA:
            for element in DATA:
                list_entry = f"{element}:{DATA[element]}\n"
                dispatcher.utter_message(text=list_entry) 
        else:
             dispatcher.utter_message(text="Your list is empty\n")    
               
        return []


class DeleteElement(Action):
    
    def name(self) -> Text:
        return "delete_element"
    

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        if file_loaded is False:
            ManageFile.loadData()
            
        element = tracker.get_slot("element")

        print("\nElement:",element)
        
        if element in DATA:
            del DATA[element]
            dispatcher.utter_message(text="Element removed.") 
        else:
            dispatcher.utter_message(text="Element not found.") 
        
        ManageFile.writeData()

        
        return [SlotSet("element", None)]