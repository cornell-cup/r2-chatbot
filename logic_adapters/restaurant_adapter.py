from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from util import keywords
from util import make_response
from util.api import restaurant

class RestaurantAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        restaurant.import_keys()

    def can_process(self, statement):
        output = keywords.get_topic(statement.text)
        print(output)

        if "name" in output.keys():
            return output["name"] == "restaurant"
        
        return False

    def get_default_response(self, input_statement):
        statement = Statement(text="no answer")
        
        return statement

    def process(self, statement, additional_response_selection, selection_parameters=None):
        topic_data = keywords.get_topic(statement.text)
        api_data = restaurant.lookup_restaurant_city("ithaca, ny")

        response = make_response.make_response_api(topic_data, api_data)

        statement = Statement(text=response, confidence=1)
        
        return statement


