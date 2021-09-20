from typing import Any, Dict, Text

from rasa.nlu.extractors.extractor import EntityExtractor
from rasa.shared.nlu.training_data.message import Message

from hun_date_parser import text2datetime


class HunDateExtractor(EntityExtractor):
    name = "HunDateExtractor"
    provides = ["entities"]
    requires = ["tokens"]

    def __init__(self, parameters: Dict[Text, Text]) -> None:
        super(HunDateExtractor, self).__init__(parameters)

        if parameters is None:
            raise AttributeError("No valid config given!")
        if not isinstance(parameters, dict):
            raise AttributeError(f"config has type {type(parameters)}")

    def process(self, message: Message, **kwargs: Any) -> None:
        extracted = self._match_entities(message)
        message.set("entities", extracted, add_to_output=True)

    @staticmethod
    def _match_entities(message: Message):
        message_text = message.get("text", "")

        return text2datetime(message_text)
