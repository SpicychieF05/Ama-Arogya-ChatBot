# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import random


class ActionHealthAdvice(Action):
    """Custom action to provide personalized health advice"""

    def name(self) -> Text:
        return "action_health_advice"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get the latest intent
        intent = tracker.latest_message['intent']['name']

        # Health advice database
        health_advice = {
            "ask_fever": [
                "बुखार के दौरान आराम बहुत जरूरी है। पानी खूब पिएं।",
                "ଜ୍ବର ସମୟରେ ବିଶ୍ରାମ ନିଅନ୍ତୁ ଏବଂ ପାଣି ପିଅନ୍ତୁ।",
                "For fever, rest is crucial. Drink plenty of fluids and monitor temperature."
            ],
            "ask_headache": [
                "सिरदर्द के लिए आराम और ठंडी पट्टी सहायक होती है।",
                "ମାଥା ବଥା ପାଇଁ ବିଶ୍ରାମ ଓ ଠଣ୍ଡା ସେକ ସାହାଯ୍ୟକାରୀ।",
                "For headache, rest in a dark room and apply cold compress."
            ],
            "ask_pregnancy_care": [
                "गर्भावस्था में नियमित जांच और पौष्टिक आहार जरूरी है।",
                "ଗର୍ଭାବସ୍ଥାରେ ନିୟମିତ ଯାଞ୍ଚ ଓ ପୁଷ୍ଟିକର ଖାଦ୍ୟ ଆବଶ୍ୟକ।",
                "During pregnancy, regular checkups and nutritious diet are essential."
            ]
        }

        # Get random advice for the intent
        if intent in health_advice:
            advice = random.choice(health_advice[intent])
            dispatcher.utter_message(text=advice)
        else:
            dispatcher.utter_message(
                text="Please ask me about specific health concerns like fever, headache, pregnancy care, etc.")

        return []


class ActionEmergencyContact(Action):
    """Provide emergency contact information"""

    def name(self) -> Text:
        return "action_emergency_contact"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        emergency_info = """
🚨 EMERGENCY CONTACTS:
• National Emergency: 108
• Ambulance: 102
• Police: 100
• Fire: 101
• Women Helpline: 181
• Child Helpline: 1098

ଜରୁରୀକାଳୀନ ସମ୍ପର୍କ: ୧୦୮
आपातकालीन संपर्क: १०८
        """

        dispatcher.utter_message(text=emergency_info)
        return []


class ActionNearestHospital(Action):
    """Provide information about finding nearest hospitals"""

    def name(self) -> Text:
        return "action_nearest_hospital"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        hospital_info = """
🏥 TO FIND NEAREST HOSPITAL:
1. Call 108 for emergency ambulance
2. Visit: www.nhp.gov.in for hospital directory
3. Use Google Maps: "hospital near me"
4. Contact local PHC (Primary Health Center)

ନିକଟତମ ଡାକ୍ତରଖାନା ପାଇଁ ୧୦୮ କଲ୍ କରନ୍ତୁ।
निकटतम अस्पताल के लिए १०८ पर कॉल करें।
        """

        dispatcher.utter_message(text=hospital_info)
        return []


class ActionMedicineReminder(Action):
    """Provide medicine taking guidelines"""

    def name(self) -> Text:
        return "action_medicine_reminder"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        medicine_info = """
💊 MEDICINE GUIDELINES:
• Take medicines at the same time daily
• Complete the full course as prescribed
• Don't skip doses
• Store medicines properly
• Check expiry dates
• Consult doctor before stopping

ଔଷଧ ସମୟ ମତେ ଖାଆନ୍ତୁ।
दवा समय पर लें।
        """

        dispatcher.utter_message(text=medicine_info)
        return []

# This is the original example action (commented out for reference)
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
