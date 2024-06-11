from io import BytesIO
import pandas as pd
from numpy import array, argmax, unique
import onnxruntime as ort
from time import time


WINDOW_LENGTH = 150
STRIDE_LENGTH = 10

LABELS = ['dws', 'jog', 'sit', 'std', 'ups', 'wlk']


def sequence_generator(x, length, stride):
    seq_x = []
    data_length = len(x)

    for i in range(0, data_length - length + 1, stride):
        input_sequence = x.iloc[i : i + length]
        seq_x.append(input_sequence)
    return array(seq_x).astype('float32')


async def classify(b_file: bytes, runtime=ort.InferenceSession('src/bin/fitmotion_model.onnx')):
    start = time()
    csv_file = BytesIO(b_file)
    df = pd.read_csv(csv_file)
    df = df.drop(labels=['Unnamed: 0'], axis=1)
    feat = sequence_generator(df, WINDOW_LENGTH, STRIDE_LENGTH)
    
    # predictor
    input_name = runtime.get_inputs()[0].name
    output_name = runtime.get_outputs()[0].name
    y_pred = runtime.run([output_name], {input_name: feat})[0]
    y_pred = argmax(y_pred, axis=1)
    
    val, count = unique(y_pred, return_counts=True)
    index = val[argmax(count)]
    end = (time() - start) * 1000
    return LABELS[index], round(end, 2)
