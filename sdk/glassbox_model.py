import json
import logging
from enum import Enum
from typing import List, Union, Optional, Tuple, OrderedDict

from sdk.__spi__.enumy import Property, Label
from sdk.__spi__.types import License, Benchmark, Metric, DataSource, CodeSource
from sdk.glassbox_config import ModelRef
from sdk.mixin.data_mixin import DataMixin
from sdk.__spi__.validation import Logging


class Purpose(Enum):
    TRAIN = "train"
    TEST = "test"
    EVALUATE = "evaluate"
    VALIDATE = "validate"


Purposes = Union[Purpose, List[Purpose]]


class GlassBoxModel(DataMixin):
    """
    A glass box model represents all necessary information about a ready to use AI model
    in order to reproduce the model results and to clearly identify the model.
    """

    license: Optional[License] = None
    checksum: Optional[str] = None
    size: Optional[str] = None
    url: Optional[str] = None

    description: Optional[str] = None
    labels: List[str] = []
    benchmarks: List[Benchmark] = []
    properties: OrderedDict = {}
    hyper_parameters: OrderedDict = {}

    metrics: List[Metric] = []
    data_sources: List[Tuple[DataSource, Purposes, Optional[Logging]]] = []
    code_sources: List[Tuple[CodeSource, Purposes, Optional[Logging]]] = []

    def __init__(self, model_ref: ModelRef):
        self.group = model_ref.group
        self.name = model_ref.name
        self.version = model_ref.version
        self.variant = model_ref.variant

    def add_benchmark(self, benchmark: Benchmark):
        """
        Adds the given benchmark instance
        """
        self.benchmarks.append(benchmark)

    def add_benchmarks(self, benchmarks: List[Benchmark]):
        """
        Adds the given list of benchmark instances
        """
        self.benchmarks.extend(benchmarks)

    def add_properties(self, key_values: dict):
        """
        Adds the given key value pairs
        """
        self.properties.update(key_values)

    def add_property(self, key: Union[str, Property], value: any):
        """
        Adds the given key value pair
        """
        key = key.value if isinstance(key, Property) else key
        self.properties[key] = value

    def add_label(self, label: Union[Label, str]):
        """
        Adds the given label
        """
        if label not in self.labels:
            self.labels.append(label.name.lower() if isinstance(label, Label) else label)

    def add_hyper_parameter(self, key: str, value: any):
        """
        Adds the given hyper parameter
        """
        self.hyper_parameters[key] = value

    def add_hyper_parameters(self, hyper_parameters: dict):
        """
        Adds the given hyper parameters
        """
        self.hyper_parameters.update(self.to_string_dict(hyper_parameters))

    def add_metric(self, metric: Metric):
        """
        Adds the given metric to the payload
        """
        self.metrics.append(metric)

    def add_code(self, code: CodeSource, purposes: Purposes, logs: Optional[Logging] = None):
        """
        Adds the given code tracking in combination with its purpose
        """
        self.code_sources.append((code, purposes, logs))

    def add_data(self, data: DataSource, purposes: Purposes, logs: Optional[Logging] = None):
        """
        Adds the given data tracking in combination with itspurpose
        """
        self.data_sources.append((data, purposes, logs))

    def validate(self):
        """
        Validates the glass box model
        """
        assert self.group is not None, "group must not be None"
        assert self.name is not None, "name must not be None"
        assert self.version is not None, "version must not be None"
        assert self.checksum is not None, "checksum must not be None"
        assert self.size is not None, "size must not be None"
        assert self.url is not None, "url must not be None"
        assert self.license is not None, "license must not be None"
        assert self.description is not None, "description must not be None"
        assert len(self.labels) > 0, "labels must not be empty"
        assert len(self.benchmarks) > 0, "benchmarks must not be empty"
        assert len(self.hyper_parameters) > 0, "hyper_parameters must not be empty"
        assert len(self.data_sources) > 0, "data_tracing must not be empty"
        assert len(self.code_sources) > 0, "code_tracing must not be empty"

        if Property.SEED_VALUE.value not in self.properties:
            logging.warning("missing SEED_VALUE leads to a lower model score")

        if Property.PARAMETER_SIZE.value not in self.properties:
            logging.warning("missing PARAMETER_SIZE leads to a lower model score")

    def as_dict(self):
        """
        Returns the glass box model as a dictionary
        """
        self.validate()

        def tuple_to_dict(data: Tuple[any, Purposes, Optional[Logging]]):
            purposes = data[1] if isinstance(data[1], list) else [data[1]]
            purposes = list(map(lambda x: x.name.lower(), purposes))

            _obj = {"purposes": purposes}
            for k, v in data[0].__dict__.items():
                if v is not None:
                    _obj[k] = v
            if data[2] is not None:
                _obj["logging"] = data[2].as_dict()
            return _obj

        obj = {
            "group": self.group,
            "name": self.name,
            "version": self.version,
            "variant": self.variant,
            "license": self.license.__dict__,
            "checksum": self.checksum,
            "size": self.size,
            "url": self.url,
            "labels": self.labels,
            "benchmarks": list(map(lambda x: x.__dict__, self.benchmarks)),
            "properties": self.properties,
            "hyperParameters": self.hyper_parameters,
            "metrics": [e.__dict__ for e in self.metrics],
            "dataSources": list(map(lambda x: tuple_to_dict(x), self.data_sources)),
            "codeSources": list(map(lambda x: tuple_to_dict(x), self.code_sources)),
        }

        if self.description is not None:
            from html import escape
            obj["description"] = escape(self.description)

        return obj

    def save(self, name: str):
        """
        Saves the glassbox model as a json file.
        """
        with open(name, "w") as outfile:
            outfile.write(json.dumps(self.as_dict(), indent=4))
