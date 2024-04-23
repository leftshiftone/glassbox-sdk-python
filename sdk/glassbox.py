from typing import Optional

from sdk.glassbox_config import GlassBoxConfig
from sdk.glassbox_model import GlassBoxModel, ModelRef
from sdk.mixin.data_mixin import DataMixin
from sdk.mixin.http_mixin import HttpMixin


class GlassBox(HttpMixin, DataMixin):

    def __init__(self, config: GlassBoxConfig):
        self.config = config

    def create_model(self, model: GlassBoxModel):
        self.http_put("model", model.as_dict())

    def search_model(self,
                     group: Optional[str] = None,
                     name: Optional[str] = None,
                     version: Optional[str] = None,
                     variant: Optional[str] = None):
        return self.http_post("model", {
            "group": group,
            "name": name,
            "version": version,
            "variant": variant
        })

    # def rate_model(self, model_ref: ModelRef):
    #     return self.http_post({"__type__": "model/rate", "modelRef": model_ref.to_string()})
