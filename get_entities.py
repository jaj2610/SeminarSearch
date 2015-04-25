from alchemyapi_python.alchemyapi import AlchemyAPI
import json

alchemyapi = AlchemyAPI()

def get_entities(doc):
    """Return (list of people, list of facilities)"""

    response = alchemyapi.entities('html', doc, {'linked_data':0,'max_retrieve':3})
    if response['status'] == 'OK':
        people = [entity for entity in response['entities'] if entity['type'] == "Person"]
        facilities = [entity for entity in response['entities'] if entity['type'] == "Facility"]
        return (people,facilities)

def get_concepts(doc):
    response = alchemyapi.concepts('html', demo_text, {'linked_data':0})
    if response['status'] == 'OK':
        return response['concepts']