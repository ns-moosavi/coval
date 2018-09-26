import os
import sys

from conll import reader
from eval import evaluator

def main():

    metric_dict = {'lea': evaluator.lea, 'muc': evaluator.muc, 
          'bcub': evaluator.b_cubed, 'ceafe' : evaluator.ceafe}

    key_file = sys.argv[1]
    sys_file = sys.argv[2]

    if 'NP_only' in sys.argv:
        NP_only = True
    else:
        NP_only = False


    if 'remove_nested' in sys.argv:
        remove_nested = True
    else:
        remove_nested = False

    if 'remove_singletons' in sys.argv or 'remove_singleton' in sys.argv:
        keep_singletons = False
    else:
        keep_singletons = True
        
    if 'all' in sys.argv:
        metrics=[(k, metric_dict[k]) for k in metric_dict]
    else:
        metrics=[]
        for name in metric_dict:
            if name in sys.argv:
                metrics.append((name, metric_dict[name]))
        if not metrics:
            metrics=[(k, metric_dict[k]) for k in metric_dict]


    evaluate(key_file, sys_file, metrics, NP_only, remove_nested, keep_singletons)

def evaluate(key_file, sys_file, metrics, NP_only, remove_nested, keep_singletons):

    doc_coref_infos = reader.get_coref_infos(key_file, sys_file, NP_only, remove_nested, keep_singletons)

    conll=0
    conll_subparts_num = 0

    for name, metric in metrics:
        recall, precision, f1 = evaluator.evaluate_documents(doc_coref_infos, metric, beta=1)    
        if name in ["muc", "bcub", "ceafe"]:
            conll+=f1
            conll_subparts_num+=1

        print(name)
        print('Recall: %.2f'%(recall*100), ' Precision: %.2f'%(precision*100), ' F1: %.2f'%(f1*100))

    if conll_subparts_num ==3:
        conll = (conll/3)*100
        print('CoNLL score: %.2f'%conll)


main()

