from io import BytesIO
from scipy.stats import mode
from tensorflow import keras
import pandas as pd
from numpy import array, argmax


model = keras.models.load_model('src/fitmotion_model.keras')

WINDOW_LENGTH = 150
STRIDE_LENGTH = 10
LABELS = ['dws', 'jog', 'sit', 'std', 'ups', 'wlk']

def sequence_generator(x, length, stride):
    seq_x = []
    data_length = len(x)

    for i in range(0, data_length - length + 1, stride):
        input_sequence = x.iloc[i : i + length]
        seq_x.append(input_sequence)
    return array(seq_x)

async def classify(b_file: bytes):
    csv_file = BytesIO(b_file)
    df = pd.read_csv(csv_file)
    df = df.drop(labels=['Unnamed: 0'], axis=1)
    feat = sequence_generator(df, WINDOW_LENGTH, STRIDE_LENGTH)
    
    y_pred = model.predict(feat)
    y_pred = argmax(y_pred, axis=1)
    y_pred = mode(y_pred)[0]
    return LABELS[y_pred]
