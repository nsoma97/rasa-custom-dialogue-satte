from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

import pandas as pd
from datetime import date, time, timedelta, datetime
from random import randint


class TimeTableSlot:

    def __init__(self, dct=None):

        if not dct:
            dates = pd.date_range(date.today(), date.today() + timedelta(days=14))
            times = [time(i) for i in range(24)]

            self.time_table = pd.DataFrame(columns=dates, index=times).fillna(0)
        else:
            self.time_table = pd.DataFrame(dct)

    def serialize_to_dict(self):
        return self.time_table.to_dict()

    @staticmethod
    def from_dict(dct):
        return TimeTableSlot(dct)

    def set_appointment(self, *args, **kwargs):
        self.time_table.iloc[randint(0, 24),
                             randint(0, 14)] = 1

    def save(self):
        time_str = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        # df_styled = self.time_table.style.background_gradient(cmap="Blues")
        self.time_table.to_excel(f'time_table_{time_str}.xls')


class ActionTimeTableFiller(Action):

    def name(self) -> Text:
        return "action_fill_table"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        time_table = tracker.get_slot('time_table')

        if not time_table:
            time_table = TimeTableSlot()
        #else:
        #    time_table = TimeTableSlot(time_table_dct)

        time_table.set_appointment()
        time_table.save()

        return [SlotSet("time_table", time_table)]
