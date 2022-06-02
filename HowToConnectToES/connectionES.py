import bspump.elasticsearch


class SamplePipeline(bspump.Pipeline):


def __init__(self, app, pipeline_id):
    super().__init__(app, pipeline_id)
    self.build(
        # Adding ES Source component with trigger set up to trigger data every 5 seconds
        bspump.elasticsearch.ElasticSearchSource(app, self, "ESConnection").on(
            bspump.trigger.PeriodicTrigger(app, 5)),
        # Rest of the pipeline with source and processors
    )


if __name__ == '__main__':
    app = bspump.BSPumpApplication()
    svc = app.get_service("bspump.PumpService")

    # Part where you add the ESConnection service
    es_connection = bspump.elasticsearch.ElasticSearchConnection(
        app, "ESConnection")
    svc.add_connection(es_connection)

    # Construct and register Pipeline
    pl = SamplePipeline(app, 'SamplePipeline')
    svc.add_pipeline(pl)

    app.run()
