import sys
from conll import reader
from eval import evaluator


def main():
    allmetrics = [('mentions', evaluator.mentions), ('muc', evaluator.muc),
            ('bcub', evaluator.b_cubed), ('ceafe', evaluator.ceafe),
            ('lea', evaluator.lea)]

    key_file = sys.argv[1]
    sys_file = sys.argv[2]

    NP_only = 'NP_only' in sys.argv
    remove_nested = 'remove_nested' in sys.argv
    keep_singletons = ('remove_singletons' in sys.argv
            or 'remove_singleton' in sys.argv)

    if 'all' in sys.argv:
        metrics = allmetrics
    else:
        metrics = [(name, metric) for name, metric in allmetrics
                if name in sys.argv]
        if not metrics:
            metrics = allmetrics

    evaluate(key_file, sys_file, metrics, NP_only, remove_nested,
            keep_singletons)


def evaluate(key_file, sys_file, metrics, NP_only, remove_nested,
        keep_singletons):
    doc_coref_infos = reader.get_coref_infos(key_file, sys_file, NP_only,
            remove_nested, keep_singletons)

    conll = 0
    conll_subparts_num = 0

    for name, metric in metrics:
        recall, precision, f1 = evaluator.evaluate_documents(doc_coref_infos,
                metric,
                beta=1)
        if name in ["muc", "bcub", "ceafe"]:
            conll += f1
            conll_subparts_num += 1

        print(name.ljust(10), 'Recall: %.2f' % (recall * 100),
                ' Precision: %.2f' % (precision * 100),
                ' F1: %.2f' % (f1 * 100))

    if conll_subparts_num == 3:
        conll = (conll / 3) * 100
        print('CoNLL score: %.2f' % conll)


if __name__ == '__main__':
    main()
