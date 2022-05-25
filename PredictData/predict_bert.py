import tensorflow as tf
import numpy as np
import pandas as pd
from official.nlp.data import classifier_data_lib
from official.nlp.bert import tokenization
from official.nlp import optimization
import tensorflow_hub as hub
import sys

model_BERT = tf.keras.models.load_model('my_model_BERT')

label_list = [0, 1] # Label categories
max_seq_length = 125 # maximum length of (token) input sequences
train_batch_size = 32
bert_layer = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/2",
                            trainable=True)

vocab_file = bert_layer.resolved_object.vocab_file.asset_path.numpy()
do_lower_case = bert_layer.resolved_object.do_lower_case.numpy()

tokenizer = tokenization.FullTokenizer(vocab_file, do_lower_case)

def to_feature(text, label, label_list=label_list, max_seq_length=max_seq_length, tokenizer=tokenizer):
    example = classifier_data_lib.InputExample(guid = None,
                                              text_a = text.numpy(), 
                                              text_b = None, 
                                              label = label.numpy())
    feature = classifier_data_lib.convert_single_example(0, example, label_list,
                                      max_seq_length, tokenizer)
    
    return (feature.input_ids, feature.input_mask, feature.segment_ids, feature.label_id)

def to_feature_map(text, label):
    input_ids, input_mask, segment_ids, label_id = tf.py_function(to_feature, inp=[text, label], 
                                  Tout=[tf.int32, tf.int32, tf.int32, tf.int32])

    # py_func doesn't set the shape of the returned tensors.
    input_ids.set_shape([max_seq_length])
    input_mask.set_shape([max_seq_length])
    segment_ids.set_shape([max_seq_length])
    label_id.set_shape([])

    x = {
          'input_word_ids': input_ids,
          'input_mask': input_mask,
          'input_type_ids': segment_ids
      }
    return (x, label_id)

def predict(sentence):
    sample_example = [sentence]
    test_data = tf.data.Dataset.from_tensor_slices((sample_example, [0]*len(sample_example)))
    test_data = (test_data.map(to_feature_map).batch(1))
    preds = model_BERT.predict(test_data)
    if preds >= 0.5:
       return 1
    return 0

def load_csv_and_predict_bert(filename,mode = 0):
    if mode == 0:
        df = pd.read_csv(filename)
    else:
        df = filename
    if 'Unamed : 0' in df.columns.to_list():
       df = df.drop('Unamed : 0',1)
    if 'emotion' in df.columns.to_list():
       df = df.drop('emotion',1)
    df = df.dropna()
    df["target"] = df["comment_post"].apply(predict)
    # df.to_csv(filename)
    return df