#!/usr/bin/env python3

import bspump
import bspump.common
import bspump.http
import bspump.trigger


class SamplePipeline(bspump.Pipeline):

    def __init__(self, app, pipeline_id):
        super().__init__(app, pipeline_id)

        self.build(
            bspump.http.HTTPClientSource(app, self,
                                         config={'url': self.Config['url'].format(api_key=self.Config['api_key'])}).on(bspump.trigger.PeriodicTrigger(app, 2)),
            bspump.common.StdJsonToDictParser(app, self),
            bspump.common.PPrintSink(app, self)
        )


if __name__ == '__main__':
    app = bspump.BSPumpApplication()

    svc = app.get_service("bspump.PumpService")
    # Construct and register Pipeline
    pl = SamplePipeline(app, 'SamplePipeline')
    svc.add_pipeline(pl)

    app.run()
