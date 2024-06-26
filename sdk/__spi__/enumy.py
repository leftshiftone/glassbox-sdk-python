from enum import Enum


class Label(Enum):
    # tasks
    TRANSLATION = "translation"
    QUESTION_ANSWERING = "question-answering"
    SUMMARIZATION = "summarization"
    CLASSIFICATION = "classification"
    TABULAR_CLASSIFICATION = "tabular-classification"

    # frameworks
    ONNX = "onnx"
    SCIKIT_LEARN = "scikit-learn"

class Property(Enum):
    SEED_VALUE = "seedValue"
    PARAMETER_SIZE = "parameterSize"
    TRAIN_TEST_SPLIT = "trainTestSplit"