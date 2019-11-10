#A lot of this code was adapted/taken from the brilliant Sara Robinson
#Please see her work here: https://sararobinson.dev/2019/04/23/interpret-bag-of-words-models-shap.html

#Sorry for anyone who has to try to read this, it's frantic hackathon code


# -*- coding: utf-8 -*-
#import easygui
import tensorflow as tf 
import pandas as pd
import numpy as np 
#import time
#from flask import Flask
import shap
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.utils import shuffle
from model_prediction import CustomModelPrediction
from preprocess import TextPreprocessor
import pickle
from datetime import datetime


##TODO:
#make separate "make model" method, then load it when you want to run
#split posts by ||| and remove . and replace with ' ' using df.columns= df.columns.str.replace('[^a-zA-Z0-9]', '')

VOCAB_SIZE=30000

def create_model(vocab_size, num_tags):
  model = tf.keras.models.Sequential()
  model.add(tf.keras.layers.Dense(300, input_shape=(VOCAB_SIZE,), activation='relu'))
  model.add(tf.keras.layers.Dense(150, activation='relu'))
  model.add(tf.keras.layers.Dense(num_tags, activation='sigmoid'))

  model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
  return model



def getString(inp_str):

  # Read, shuffle, and preview the data
  data = pd.read_csv('mbti_1.csv', names=['types', 'posts'], header=0)

  naughty_list=['istj', 'istp', 'isfj', 'isfp', 'infj', 'infp', 'intj',
                'intp', 'estp', 'estj', 'esfp', 'esfj', 'esfp', 'esfj',
                'enfp', 'enfj', 'entp', 'entj']
  data['posts']=data['posts'].str.lower().replace("|||", " ")
  for k in naughty_list:
    data['posts']=data['posts'].str.replace(k, "")
    

  # Encode top tags to multi-hot
  tags_split = [tags.split(' ') for tags in data['types'].values]
  #print(tags_split)

  tag_encoder = MultiLabelBinarizer()
  tags_encoded = tag_encoder.fit_transform(tags_split)
  num_tags = len(tags_encoded[0])
  #print(data['posts'].values[0])
  #print(tag_encoder.classes_)
  #print(tags_encoded[0])

  # Split our data into train and test sets
  train_size = int(len(data) * .8)
  print ("Train size: %d" % train_size)
  print ("Test size: %d" % (len(data) - train_size))

  # Split our labels into train and test sets
  train_tags = tags_encoded[:train_size]
  test_tags = tags_encoded[train_size:]

  # Create vocab from training corpus


  train_qs = data['posts'].values[:train_size]
  test_qs = data['posts'].values[train_size:]

  processor = TextPreprocessor(VOCAB_SIZE)
  processor.create_tokenizer(train_qs)

  body_train = processor.transform_text(train_qs)
  body_test = processor.transform_text(test_qs)

  # Preview the first input from our training data
  print(len(body_train[0]))
  print(body_train[0])

  """## Building and training our model"""

  # Save the processor state of the tokenizer

##  with open('./processor_state.pkl', 'wb') as f:
##    pickle.dump(processor, f)

  print("preparing model")
  now = datetime.now()
  current_time = now.strftime("%H:%M:%S")
  print("Current Time =", current_time)

  #train model if we haven't already
  try:
    #print("starting load")
    model = tf.keras.models.load_model('keras_saved_model.h5')

  except:
    model = create_model(VOCAB_SIZE, num_tags)
    #model.summary()
    model.fit(body_train, train_tags, epochs=10, batch_size=128, validation_split=0.1)
    print('Eval loss/accuracy:{}'.format(
      model.evaluate(body_test, test_tags, batch_size=128)))
    model.save('keras_saved_model.h5')






##
##  """## Interpreting our model with SHAP"""
##  attrib_data = body_train[:200]
##  explainer = shap.DeepExplainer(model, attrib_data)
##
##  num_explanations = 100
##  shap_vals = explainer.shap_values(body_test[:num_explanations])
##
##  words = processor._tokenizer.word_index
##
##  print("here")
##
##  word_lookup = list()
##  for i in words.keys():
##    word_lookup.append(i)
##
##  word_lookup = [''] + word_lookup
##  print(word_lookup[:100])


  test_results=[]
  test_results.append(inp_str)
  classifier = CustomModelPrediction.from_path('.')
  #print("about to predict")
  results=classifier.predict(test_results)
  #print(results)
  

  prdct_list=results[0]
  prdct=max(prdct_list)
  pretty=str(tag_encoder.classes_[prdct_list.index(prdct)])

##  shap.summary_plot(shap_vals, feature_names=word_lookup, class_names=tag_encoder.classes_)

  return pretty



if __name__== "__main__" :
  #compl = getString(easygui.enterbox("Type some text!")
  #easygui.msgbox(compl)
  print(getString("We are so easily pacified. Harriet would never." +
                  "Yall smoking if yall think labels aint pissed"+
                  "about the lev https://t.co/qGz0wbc2xC"))
