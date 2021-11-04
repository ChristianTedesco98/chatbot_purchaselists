# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

DATA = {
    'List1' : {
    }
}

class AddElement(Action):

    def name(self) -> Text:
        return "utter_add_element"
    
    def write_file():
        f = open("test.txt", "w")
        f.write("Something saved")
        f.close()

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        element = tracker.get_slot("element")
        quantity = tracker.get_slot("quantity")

        print("\nElement:",element)
        print("Quantity:",quantity)

        for list in DATA:
            if element in list:
                old_quantity = list[element]
                new_quantity = old_quantity + quantity
                list[element] = new_quantity
            else:
                list[element] = quantity
        
        self.write_file()
        
        dispatcher.utter_message(text="List updated.") 

        return []
