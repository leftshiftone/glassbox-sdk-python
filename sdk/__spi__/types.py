from dataclasses import dataclass
from typing import Optional

from abc import ABC


class Traceable(ABC):
    """
    Traceable classes can be validated if the given url information is available.
    If the given url is not available the user is informed about it.
    """

    url: str



@dataclass
class Benchmark(Traceable):
    type: str
    score: str
    url: str

class CodeSource(Traceable):
    pass


@dataclass
class GitCommit(CodeSource):
    """
    A Git instance represents a code repository state at a custom hash value.
    """

    url: str
    hash: str

    def __post_init__(self):
        self.type = "commit"


@dataclass
class GitTag(CodeSource):
    """
    A Git instance represents a code repository state at a custom git tag.
    """

    url: str
    tag: str

    def __post_init__(self):
        self.type = "tag"

class DataSource(Traceable):
    pass


@dataclass
class Dataset(DataSource):
    """
    A data instance represents a collection of information used by an ai model for training or testing.
    """

    url: str
    checksum: Optional[str] = None

    def __post_init__(self):
        self.type = "dataset"

@dataclass
class License:
    name: str
    url: str


CC_BY_4 = License("cc-by-4.0", "https://creativecommons.org/licenses/by/4.0/")
APACHE_2 = License("apache-2.0", "http://www.apache.org/licenses/LICENSE-2.0")

@dataclass
class Metric:
    name: str
    value: float
    value_min: Optional[float] = 0
    value_max: Optional[float] = 1