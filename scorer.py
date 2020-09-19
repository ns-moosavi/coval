#!/usr/bin/python3
"""Coreference evaluation tool for CoNLL files.
Usage: python3 scorer.py <key> <system> [options]
'key' and 'system' are the key and system files, respectively.
Options:
    lea muc bcub ceafe ceafm  specify metrics to compute (default: all)
    remove_singletons         remove singletons for scoring (default: keep)
    np_only                   only evaluate NPs (default: unrestricted)
    min_spans                 score with minimal spans using MINA algorithm
                              (default: off)"""
import sys
from coval.conll import reader
from coval.conll import util
from coval.eval import evaluator


def main():
    allmetrics = [
            ('mentions', evaluator.mentions),
            ('muc', evaluator.muc),
            ('bcub', evaluator.b_cubed),
            ('ceafe', evaluator.ceafe),
            ('ceafm', evaluator.ceafm),
            ('lea', evaluator.lea)]

    try:
        key_file = sys.argv[1]
        sys_file = sys.argv[2]
    except IndexError:
        print(__doc__)
        return

    NP_only = 'NP_only' in sys.argv
    remove_nested = 'remove_nested' in sys.argv
    keep_singletons = ('remove_singletons' not in sys.argv
            and 'remove_singleton' not in sys.argv)
    min_span = False
    if ('min_span' in sys.argv
        or 'min_spans' in sys.argv
        or 'min' in sys.argv):
        min_span = True
        has_gold_parse = util.check_gold_parse_annotation(key_file)
        if not has_gold_parse:
                util.parse_key_file(key_file)
                key_file = key_file + ".parsed"

    if 'all' in sys.argv:
        metrics = allmetrics
    else:
        metrics = [(name, metric) for name, metric in allmetrics
                if name in sys.argv]
        if not metrics:
            metrics = allmetrics

    evaluate(key_file, sys_file, metrics, NP_only, remove_nested,
            keep_singletons, min_span)


def evaluate(key_file, sys_file, metrics, NP_only, remove_nested,
        keep_singletons, min_span):
    doc_coref_infos = reader.get_coref_infos(key_file, sys_file, NP_only,
            remove_nested, keep_singletons, min_span)

    conll = 0
    conll_subparts_num = 0

    print('             recall  precision         F1')
    for name, metric in metrics:
        recall, precision, f1 = evaluator.evaluate_documents(doc_coref_infos,
                metric,
                beta=1)
        if name in ('muc', 'bcub', 'ceafe'):
            conll += f1
            conll_subparts_num += 1
        print(
                name.ljust(8),
                '    %6.2f' % (recall * 100),
                '    %6.2f' % (precision * 100),
                '    %6.2f' % (f1 * 100))

    if conll_subparts_num == 3:
        conll = (conll / 3) * 100
        print('CoNLL score: %6.2f' % conll)


if __name__ == '__main__':
    main()
