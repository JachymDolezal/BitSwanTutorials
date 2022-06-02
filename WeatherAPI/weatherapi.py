#!/usr/bin/env python3

import bspump
import bspump.common
import bspump.http
import bspump.trigger
import aiohttp


class LoadSource(bspump.TriggerSource):

    def __init__(self, app, pipeline, choice=None, id=None, config=None):
        super().__init__(app, pipeline, id=id, config=config)
        self.cities = ['London', 'New York', 'Berlin']  # List of cities

    async def cycle(self):
        async with aiohttp.ClientSession() as session:
            # goes through the list of cities and requests from API for each city
            for city in self.cities:
                async with session.get(url=self.Config['url'].format(city=city, api_key=self.Config['api_key'])) as response:
                    event = await response.content.read()
                    await self.process(event)


class SamplePipeline(bspump.Pipeline):

    def __init__(self, app, pipeline_id):
        super().__init__(app, pipeline_id)

        self.build(
            LoadSource(app, self).on(
                bspump.trigger.PeriodicTrigger(app, 5)
            ),
            bspump.common.PPrintSink(app, self),
        )


if __name__ == '__main__':
    app = bspump.BSPumpApplication()
    svc = app.get_service("bspump.PumpService")
    pl = SamplePipeline(app, 'SamplePipeline')
    svc.add_pipeline(pl)
    app.run()
