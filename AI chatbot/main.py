import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
import names #random name generator
from tensorflow.keras.models import load_model
import json
import streamlit as st

lemmatizer = WordNetLemmatizer()

intents = json.loads(open('intents.json').read())

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbotmodel.h5')

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word)  for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words= clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1

    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda  x:x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list


def get_response(intents_list,intents_json):
    tag= intents_list[0]['intent']
    list_of_intents =intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result


Questions_to_ask = ["Hii, how can we help you? Please list out your symptoms : ",
                    "Enter your details such as name, age, phone number separated by ',' ",
                    "Enter your account password that you would like to use (should be alpha-numeric): " ,
                    "Enter your blood group: ",
                    "Enter your Insurance ID: ",
                    "Enter your family members' illness history: ",
                    "Enter emergency contact number: ",
                    "Would you like to add anything else? (y/n) ",
                    "Thank you, hope you get well soon. We will notify you with the details of your "
                                  "appointment at the earliest"]

numques = len(Questions_to_ask)

#File to save the symptoms
f = open("patient_details.txt", "w+")
contents = []

st.title("Medical Info Chatbot")

for i in range(numques):

    if (i == 1) or (i == 7):
        st.write(f"| Bot: {Questions_to_ask[i]}")
        message = st.text_input(f"| You:", key=f"msg{i}")
        if message:
            contents.append(message)
            message = message.lower()
            if (i == 7) and (message == "y" or message == "Y" or message == "Yes" or message == "yes"):
                st.write("| Bot: Please specify")
                message = st.text_input(f"| You:", key=f"msg{i+1}")
                if message:
                    contents.append(message)
                    message = message.lower()
                    st.markdown("Thank you for using our chatbot!!")
            elif (i == 7) and (message == "n" or message == "N" or message == "No" or message == "no"):
                message = "No more specification"
                contents.append(message)
                st.markdown("Thank you for using our chatbot!!")
                pass
            st.write("\n")
    elif i != numques-1:
        st.write(f"| Bot: {Questions_to_ask[i]}")
        message = st.text_input(f"| You:", key=f"msg{i}")
        if message:
            contents.append(message)
            message = message.lower()
            ints = predict_class(message)
            res = get_response(ints, intents)
            st.write(f"| Bot: {res}")
            st.write("\n")
    # else:
    #     st.write(f"| Bot: {Questions_to_ask[i]}")
    #     doc_name = names.get_full_name()
    #     st.write(f"| Bot: {doc_name}")
    #     contents.append(doc_name)
    #     st.write("\n")

# Processing the data
contents.pop(7)
lst = contents[1].split(",")
contents[1] = lst

# Details of the Patient to the file
f.write(f"\nName : {contents[1][0]}")
f.write(f"\nAge : {contents[1][1]}")
f.write(f"\nPhone number : {contents[1][2]}")
f.write(f"\nPassword given : {contents[2]}")
f.write(f"\nBlood Group : {contents[3]}")
f.write(f"\nInsurance ID : {contents[4]}")
f.write(f"\nFamily Illness History : {contents[5]}")
f.write(f"\nEmergency contact number : {contents[6]}")
f.write("\nDetails : \n")
f.write(contents[0])
f.write("\n")
if(contents[7]):
    f.write(contents[7])
f.close() # closing the file

pData = dict()

pData["name"] = contents[1][0]
pData["age"] = contents[1][1]
pData["phNum"] = contents[1][2]
pData["pw"] = contents[2]
pData["bg"] = contents[3]
pData["insID"] = contents[4]
pData["familyIllness"] = contents[5]
pData["emPhNum"] = contents[6]

if(contents[7]):
    pData["details"] = contents[0] +" " + contents[7]
else:
    pData["details"] = contents[0]

# open the file in append mode and write the dictionary to it
with open('pData.json', 'a') as file:
    json.dump(pData, file)
    file.write('\n') # add a new line after the dictionary for readability

# # read all the dictionaries in the file
# with open('pData.json', 'r') as file:
#     for line in file:
#         dictionary = json.loads(line)
#         for key, value in dictionary.items():
#             print(key, value)
