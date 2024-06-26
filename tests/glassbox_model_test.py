import os
import time
import unittest

from sdk.__spi__ import BETA_API_URL
from sdk.__spi__.enumy import Label, Property
from sdk.__spi__.types import APACHE_2, GitCommit, Dataset, Benchmark
from sdk.glassbox import GlassBox, GlassBoxConfig
from sdk.glassbox_config import ModelRef, HMACCredentials
from sdk.glassbox_model import GlassBoxModel
from sdk.glassbox_model import Purpose
from sdk.mixin.data_mixin import DataMixin


class GlassboxTest(unittest.TestCase, DataMixin):

    def test(self):
        credentials = HMACCredentials(api_key=os.environ["API_KEY"], api_secret=os.environ["API_SECRET"])
        config = GlassBoxConfig(url=BETA_API_URL, credentials=credentials)

        glassbox = GlassBox(config)

        model_name = "opus-mt-it-en"
        model = GlassBoxModel(ModelRef("leftshiftone", model_name, "1.0.0"))
        model.checksum = self.checksum(model)
        model.size = str(time.time())
        model.url = f"https://{model.group}/{model.name}/{model.version}"
        model.license = APACHE_2
        model.add_label(Label.TRANSLATION)
        model.add_label(Label.ONNX)

        model.add_property(Property.SEED_VALUE, 123)
        model.add_property(Property.PARAMETER_SIZE, 1000000)

        model.add_hyper_parameters({
            "vocab_size": 58101,
            "max_position_embeddings": 512,
            "d_model": 512,
            "encoder_ffn_dim": 2048,
            "encoder_layers": 6,
            "encoder_attention_heads": 8,
            "decoder_ffn_dim": 2048,
            "decoder_layers": 6,
            "decoder_attention_heads": 8,
            "dropout": 0.1,
            "attention_dropout": 0.0,
            "activation_dropout": 0.0,
            "activation_function": "swish",
            "init_std": 0.02,
            "encoder_layerdrop": 0.0,
            "decoder_layerdrop": 0.0,
            "classifier_dropout": 0.0,
            "use_cache": True,
            "num_hidden_layers": 6,
            "scale_embedding": True,
            "return_dict": True,
            "output_hidden_states": False,
            "output_attentions": False,
            "torchscript": False,
            "torch_dtype": None,
            "use_bfloat16": False,
            "pruned_heads": {},
            "tie_word_embeddings": True,
            "is_encoder_decoder": True,
            "is_decoder": False,
            "add_cross_attention": False,
            "tie_encoder_decoder": False,
            "max_length": 512,
            "min_length": 0,
            "do_sample": False,
            "early_stopping": False,
            "num_beams": 4,
            "num_beam_groups": 1,
            "diversity_penalty": 0.0,
            "temperature": 1.0,
            "top_k": 50,
            "top_p": 1.0,
            "repetition_penalty": 1.0,
            "length_penalty": 1.0,
            "no_repeat_ngram_size": 0,
            "encoder_no_repeat_ngram_size": 0,
            "bad_words_ids": [
                [
                    58100
                ]
            ],
            "num_return_sequences": 1,
            "chunk_size_feed_forward": 0,
            "output_scores": False,
            "return_dict_in_generate": False,
            "forced_bos_token_id": None,
            "forced_eos_token_id": 0,
            "remove_invalid_values": False,
            "architectures": [
                "MarianMTModel"
            ],
            "finetuning_task": None,
            "id2label": {
                "0": "LABEL_0",
                "1": "LABEL_1",
                "2": "LABEL_2"
            },
            "label2id": {
                "LABEL_0": 0,
                "LABEL_1": 1,
                "LABEL_2": 2
            },
            "tokenizer_class": None,
            "prefix": None,
            "bos_token_id": 0,
            "pad_token_id": 58100,
            "eos_token_id": 0,
            "sep_token_id": None,
            "decoder_start_token_id": 58100,
            "task_specific_params": None,
            "problem_type": None,
            "_name_or_path": "Helsinki-NLP/opus-mt-en-de",
            "transformers_version": "4.9.0.dev0",
            "_num_labels": 3,
            "add_bias_logits": False,
            "add_final_layer_norm": False,
            "classif_dropout": 0.0,
            "gradient_checkpointing": False,
            "model_type": "marian",
            "normalize_before": False,
            "normalize_embedding": False,
            "static_position_embeddings": True
        })

        code = GitCommit("https://github.com/Helsinki-NLP/OPUS-MT-train", "4b0d49ddbbb0ebc7819999288ff3dc6ffcfcced4")
        model.add_code(code, purposes=[Purpose.TRAIN, Purpose.TEST, Purpose.EVALUATE])

        data1 = Dataset(url="https://opus.nlpl.eu")
        model.add_data(data1, purposes=Purpose.TRAIN)

        data2 = Dataset(url="https://object.pouta.csc.fi/OPUS-MT-models/en-de/opus-2020-02-26.test.txt")
        model.add_data(data2, purposes=Purpose.TEST)

        data3 = Dataset(url="https://object.pouta.csc.fi/OPUS-MT-models/en-de/opus-2020-02-26.eval.txt")
        model.add_data(data3, purposes=Purpose.EVALUATE)

        benchmark_url1 = "https://github.com/Helsinki-NLP/OPUS-MT-train/tree/master/testsets/de-en/newssyscomb2009.de.gz"
        benchmark_url2 = "https://github.com/Helsinki-NLP/OPUS-MT-train/tree/master/testsets/de-en/news-test2008.de.gz"
        benchmark_url3 = "https://github.com/Helsinki-NLP/OPUS-MT-train/tree/master/testsets/de-en/newstest2009.de.gz"
        benchmark_url4 = "https://github.com/Helsinki-NLP/OPUS-MT-train/tree/master/testsets/de-en/newstest2010.de.gz"
        benchmark_url5 = "https://github.com/Helsinki-NLP/OPUS-MT-train/tree/master/testsets/de-en/newstest2011.de.gz"
        benchmark_url6 = "https://github.com/Helsinki-NLP/OPUS-MT-train/tree/master/testsets/de-en/newstest2012.de.gz"
        benchmark_url7 = "https://github.com/Helsinki-NLP/OPUS-MT-train/tree/master/testsets/de-en/newstest2013.de.gz"
        benchmark_url8 = "https://github.com/Helsinki-NLP/OPUS-MT-train/tree/master/testsets/de-en/newstest2015-ende.de.gz"
        benchmark_url9 = "https://github.com/Helsinki-NLP/OPUS-MT-train/tree/master/testsets/de-en/newstest2016-ende.de.gz"
        benchmark_url10 = "https://github.com/Helsinki-NLP/OPUS-MT-train/tree/master/testsets/de-en/newstest2017-ende.de.gz"
        benchmark_url11 = "https://github.com/Helsinki-NLP/OPUS-MT-train/tree/master/testsets/de-en/newstest2018-ende.de.gz"
        benchmark_url12 = "https://github.com/Helsinki-NLP/OPUS-MT-train/tree/master/testsets/de-en/newstest2019-ende.de.gz"

        model.add_benchmarks([
            Benchmark("bleu", "23.5", benchmark_url1),
            Benchmark("chrf", "0.540", benchmark_url1),
            Benchmark("bleu", "23.5", benchmark_url2),
            Benchmark("chrf", "0.529", benchmark_url2),
            Benchmark("bleu", "22.3", benchmark_url3),
            Benchmark("chrf", "0.530", benchmark_url3),
            Benchmark("bleu", "24.9", benchmark_url4),
            Benchmark("chrf", "0.544", benchmark_url4),
            Benchmark("bleu", "22.5", benchmark_url5),
            Benchmark("chrf", "0.524", benchmark_url5),
            Benchmark("bleu", "23.0", benchmark_url6),
            Benchmark("chrf", "0.525", benchmark_url6),
            Benchmark("bleu", "26.9", benchmark_url7),
            Benchmark("chrf", "0.553", benchmark_url7),
            Benchmark("bleu", "31.1", benchmark_url8),
            Benchmark("chrf", "0.594", benchmark_url8),
            Benchmark("bleu", "37.0", benchmark_url9),
            Benchmark("chrf", "0.636", benchmark_url9),
            Benchmark("bleu", "29.9", benchmark_url10),
            Benchmark("chrf", "0.586", benchmark_url10),
            Benchmark("bleu", "45.2", benchmark_url11),
            Benchmark("chrf", "0.690", benchmark_url11),
            Benchmark("bleu", "40.9", benchmark_url12),
            Benchmark("chrf", "0.654", benchmark_url12)
        ])

        model.description = """
Tools and resources for open translation services

* based on Marian-NMT
* trained on OPUS data using OPUS-MT-train (New: leaderboard)
* mainly SentencePiece-based segmentation
* mostly trained with guided alignment based on eflomal wordalignments
* pre-trained downloadable translation models (matrix view), CC-BY 4.0 license
* more freely available translation models from the Tatoeba translation challenge, CC-BY 4.0 license
* demo translation interface available from https://opusmt.wmflabs.org/
        """

        print(glassbox.create_model(model))
        model.save("model.json")

    def test_search_model(self):
        credentials = HMACCredentials(api_key=os.environ["API_KEY"], api_secret=os.environ["API_SECRET"])
        config = GlassBoxConfig(url=BETA_API_URL, credentials=credentials)

        glassbox = GlassBox(config)
        models = glassbox.search_model()

        print(models)
        self.assertTrue(len(models) > 0)
