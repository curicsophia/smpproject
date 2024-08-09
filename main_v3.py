import os
import openai
import time
import inputfileread

openai.api_key = "xxx"
openai.api_base = 'xxx'
openai.api_type = 'azure'
openai.api_version = '2023-05-15'
deployment_name='IS463Deployment1'

info = inputfileread.getInfo()
characters, promptList, quoteList, qn = info[0], info[1], info[2], info[3]
people = ["zach", "kh", "caden", "javen", "aadhi" ] 
respondPrompt = promptList[5]


convString = ""
convo = open("convo.txt", "r")
x = convo.readline()

while x != "" :
    convString += x
    x = convo.readline()

    
def getPersonToRepond():
    prompt = respondPrompt + "\n"
    prompt += "conversation so far:  \n" + convString + "\n"

    prompt += "list of people to choose from, their personality, and speech habits:\n"
    for i in people:
        prompt += i + ":\n"
        prompt += characters[i] + "\n"
        prompt += "speech habits: " + quoteList[i] + "\n"
        

    flag = True
    while flag:
        try:
            response = openai.ChatCompletion.create(
                deployment_id=deployment_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=20,
                temperature=0.1,
                top_p=0.9,
                frequency_penalty=1.0,
                presence_penalty=1.0
            )

            full_response = response["choices"][0]["message"]["content"]
            flag = False
        except openai.error.RateLimitError as e:
            print(e)
            time.sleep(1)

    full_response = list(full_response.split())
    for i in full_response:
        if i.lower() in people:
            return i.lower()
    print("i hate chatgpt")
    #return getPersonToRepond()
    return full_response

for i in range(5):
    print(getPersonToRepond()) 
