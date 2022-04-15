# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from transformers import pipeline

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
   
        message = tracker.latest_message.get('text')
        question_answerer =  pipeline("question-answering")
        context =  """Greetings, I am Pastor Zimmerman, thanks for meeting me today.\
        I am here today because I had a nodule removed recently and I have been drinking a lot. \
        My wife's at home with Alzheimer's. I feel very guilty these days because I've been drinking pretty heavily and I don't want to disappoint people.\
        But it’s the only way I’ve been able to cope lately. It's not an easy situation with my wife.\
        My wife has good days and bad days. And on the bad days regarding my wife, I get affected the most.\
        You know my son helps a lot around the house but he is working on his PhD and he doesn’t have time to help me out that much. \
        It's just very painful to watch my wife deteriorate and the drinking helps me cope. \
        Drinking calms me down, helps me sleep, and makes it easier for me to communicate with people.\
        I know it's not healthy for me but drinking is the most cost-efficient way for me to calm down these days.\
        I am using alcohol as a coping mechanism and I am not proud of it. The disadvantages of drinking are as follows:\
        one thing is what happened to my throat, I could also lose face with those who have placed a lot of trust in me, and overall, \
        it is detrimental to my health. I drink about two or three beers a night with a couple of shots. Yes, I would like to discuss a\
        solution together with you. Drinking only beer might be a good way of trying to wean me off the heavy stuff. \
        I have not looked for any Alzheimer’s support group yet but I think that's a good idea. I know I can join Alcohol and Anonymous.\
        Sometimes my wife's situation could be beneficial to this. Before when I have tried to cut back I've been successful sometimes. \
        I can cut back to two or three beers a day but then something will always come up to trigger it again. \
        I have a problem with trying to communicate with my wife or something in the family.\
        when I focus on trying to exercise more and when I meet with friends, it helps me to drink less. \
        But I don't have a lot of time to do that with my current situation.\
        That’s why I could never get any consistent with any of that. \
        My willingness to cut down on drinking is at least an eight out of 10.\
        I am not so confident that I can stop drinking \
        It’s because I haven’t been successful in maintaining it in the past.\
        Back in the day, I used to exercise every day and that helped. This form of exercise was very relaxing for me. \
        You know with my current situation if I could just find some way to do it regularly, I think it will help. \
        I am perfectly okay with talking more about my condition the next time we meet.\
        Thank you so much for meeting with me, have a great day.\
        I developed a nodule in my throat because I was drinking too much. \
        I am not so sure if I can stop drinking. This form of exercise was very relaxing for me. \
        But I can't take advantage of it. I feel very depressed. I don`t know what do with my life.  \
        I know it is wrong, but I feel like drinking is the only way I can forget about everything. \
        These days I just feel so lonely and alone. But when I drink, even for a while, i can forget all stress. \
        You know with my current situation if I could just find some way to do it regularly, I think it will help. \
        I am perfectly okay with talking more about my condition the next time we meet.\
        If something bad happens you drink in an attempt to forget; if something good \
        happens you drink in order to celebrate; and if nothing happens you drink to make something happen \
        I am going to try to spend more time with my family and friends \
       """

        final = "I am sorry. Could please rephrase that!"
        result = question_answerer(question=message, context=context)
        value = result['answer']
        if (result['score']>=0.1):
          final = value
  

        dispatcher.utter_message(text=final)

        return []
