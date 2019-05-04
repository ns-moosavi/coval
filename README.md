# CoVal: A coreference evaluation tool for the CoNLL and ARRAU datasets

We provide the implementation of the common evaluation metrics including MUC,
B-cubed, CEAFe, and LEA for both CoNLL and ARRAU datasets.

### Requirements
This evaluation tool requires numpy, scipy, and scikit-learn packages.

## Usage
Basic usage with CoNLL files:

	$ python scorer.py key system

`key` and `system` are the files with gold coreference and system output, respectively.

Please refer to
[ARRAU README](https://github.com/ns-moosavi/coval/blob/master/arrau/README.md)
for evaluations of the ARRAU files and
[CoNLL README](https://github.com/ns-moosavi/coval/blob/master/conll/README.md)
for CoNLL evaluations.

Run tests with `python3 -m pytest unittests.py`

## Reference
If you use this code in your work, please cite the paper:
```
@InProceedings{moosavi2016coreference,
    author = {Moosavi, Nafise Sadat  and Strube, Michael},
    title = {Which Coreference Evaluation Metric Do You Trust?
		A Proposal for a Link-based Entity Aware Metric},
    year = {2016},
    booktitle = {Proceedings of the 54th Annual Meeting of
		the Association for Computational Linguistics (Volume 1: Long Papers)},
    pages = {632--642},
    publisher = {Association for Computational Linguistics},
    address = {Berlin, Germany},
    doi = {10.18653/v1/P16-1060},
    url = {https://www.aclweb.org/anthology/P16-1060},
}
```

## Authors
This code was written by @ns-moosavi
Some parts are borrowed from
https://github.com/clarkkev/deep-coref/blob/master/evaluation.py
The test suite is taken from https://github.com/conll/reference-coreference-scorers/
Mention evaluation and the test suite were added by @andreasvc
