

from GNN_utils import *


def infer_GNN(test_file):

    verilog_file = preprocessing_test(test_file)
    data = extracting_attributes(verilog_file)
    pred_label = get_prediction(data)
    label = get_label_infer(pred_label)

    return label


test_file = 'test_sample.txt'
label = infer_GNN(test_file)
print(label)
