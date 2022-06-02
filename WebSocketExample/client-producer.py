#!/usr/bin/env python3
import bspump
import bspump.common
import bspump.http
import bspump.trigger


class SamplePipeline(bspump.Pipeline):

    def __init__(self, app, pipeline_id):
        super().__init__(app, pipeline_id)
        self.Counter = 1

        # self.Source = bspump.common.InternalSource(app, self)

        self.build(
            bspump.http.HTTPClientSource(app, self, config={
                'url': 'https://api.coindesk.com/v1/bpi/currentprice.json'
                # Trigger that triggers the source every second (based on the method parameter)
            }).on(bspump.trigger.PeriodicTrigger(app, 5)),

            bspump.http.HTTPClientWebSocketSink(app, self, config={
                'url': 'http://127.0.0.1:8080/bspump/ws',
            })

        )


if __name__ == '__main__':
    app = bspump.BSPumpApplication()

    svc = app.get_service("bspump.PumpService")

    # Construct and register Pipeline
    pl = SamplePipeline(app, 'SamplePipeline')
    svc.add_pipeline(pl)

    app.run()
