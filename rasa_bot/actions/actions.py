import requests
from rasa_sdk import Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Tracker

class ActionFetchVoterId(Action):

    def name(self):
        return "action_fetch_voter_id"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain):

        try:
            res = requests.get(
                "http://localhost:8000/api/services/info/Voter ID/",
                timeout=5
            )

            data = res.json()
            docs = "\n".join([f"✔ {d}" for d in data["documents"]])

            dispatcher.utter_message(
                text=f"You will need the following documents 📄\n{docs}"
            )
            dispatcher.utter_message(response="utter_connect_employee")

        except Exception:
            dispatcher.utter_message(
                text="Unable to fetch documents right now 😅"
            )

        return []
