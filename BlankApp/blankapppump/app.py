import bspump
import bspump.elasticsearch

from .pipelines.blankapppipeline.pipeline import BlankAppPipeline


class BlankApp(bspump.BSPumpApplication):

    def __init__(self):
        super().__init__()

        svc = self.get_service("bspump.PumpService")

        # es_connection = bspump.elasticsearch.ElasticSearchConnection(
        #     self, "ESConnection")
        # svc.add_connection(es_connection)

        svc.add_pipeline(BlankAppPipeline(self, "BlankAppPipeline"))
