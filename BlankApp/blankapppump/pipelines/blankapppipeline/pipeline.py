import bspump.common
import bspump.elasticsearch
import bspump.http
import bspump.trigger
from datetime import datetime
import pandas as pd
import pytz


from .processors.enrichprocessor import EnrichProcessor


class BlankAppPipeline(bspump.Pipeline):

    def __init__(self, app, pipeline_id):
        super().__init__(app, pipeline_id)

        self.build(
            # Source that GET requests from the API source.
            bspump.http.HTTPClientSource(app, self, config={
                'url': 'https://api.coindesk.com/v1/bpi/currentprice.json'
                # Trigger that triggers the source every second (based on the method parameter)
            }).on(bspump.trigger.PeriodicTrigger(app, 5)),
            # Converts incoming json event to dict data type.
            bspump.common.StdJsonToDictParser(app, self),
            # Adds a CZK currency to the dict
            EnrichProcessor(app, self),
            bspump.common.StdDictToJsonParser(app, self),
            # prints the event to a console
            bspump.common.PPrintSink(app, self),
        )
