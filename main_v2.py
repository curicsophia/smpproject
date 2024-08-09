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
characters, promptList, quoteList, opinionList, qn = info[0], info[1], info[2], info[3], info[4]
                                             
imptPrompt = promptList[0]
relevPrompt = promptList[1]
emoPrompt = promptList[2]
askPrompt = promptList[3]
emosPrompt = promptList[4]
summaryPrompt = promptList[5]
respondPrompt = promptList[6]

                                             
start_time = time.time()

numbers = list(range(1, 11))
numbers = [str(i) for i in numbers]

convo = open("convo.txt", "w")
inputs = open("inputs.txt", "w")
emotions = open("emotions.txt", "w")
checks = open("checks.txt", "w")



people = ["zach", "kh", "caden", "javen", "aadhi" ] 
convList = []
convString = ""
summaryList = []

def ask(temp, imptMemories, person):
    prompt = askPrompt + "\n"

    if imptMemories == []:
        prompt += "no one has said anything yet\n"
        feelings = "neutral"
    else:
        prompt += "important parts of the conversation so far (more vivid memories are in full, while others are summarised): \n"
        feelings = getEmo(person)
        feelings = "These are how you feel at the moment: \n" + feelings
    for i in range(len(convList)):
        if i in imptMemories:
            prompt += "(full speech) " + convList[i] + "\n"
        else:
            prompt += "(summarised) "  + summaryList[i] + "\n"
            
            
    
    prompt += "question at hand: " + qn + "\n"
    inputs.write(person)
    inputs.write(prompt)
    inputs.write("\n")
    
    
    flag = True
    while flag:
        try:
            context = "You are the following character in an ARGUMENTATIVE DISCUSSION: " + characters[person] + "\n"
            speech = "This is a quote of how you normally speak: " + quoteList[person] + ". Replicate these speech patterns. \n"
            opinion = "Your " + opinionList[person]
            response = openai.ChatCompletion.create(
                deployment_id=deployment_name,
                messages=[{"role": "system", "content": context},
                          {"role": "system", "content": speech},
                          {"role": "system", "content": feelings},
                          {"role": "system", "content": opinion},
                          {"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=characters[temp],
                top_p=0.9,
                frequency_penalty=1.0,
                presence_penalty=1.0
            )

            full_response = response["choices"][0]["message"]["content"]
            flag = False
        except openai.error.RateLimitError as e:
            print(e)
            time.sleep(1)
            
 
    for i in range(len(full_response)-1, -1, -1):
        if full_response[i] == '.' or full_response[i] == '?':
            inputs.write(full_response)
            inputs.write("\n\n")
            return full_response[:i+1]
    
    
def check(prompt, person):
    flag = True
    while flag:
        try:
            context = "You are: " + characters[person] + "\n"
            opinion = "Your " + opinionList[person]
            response = openai.ChatCompletion.create(
                deployment_id=deployment_name,
                messages=[{"role": "system", "content": context},
                          {"role": "system", "content": opinion},
                          {"role": "user", "content": prompt}],
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

    checks.write( "full response : "+ full_response)
    checks.write("\n") 
    return full_response



def imptVal(sentence, hearer):
    prompt = imptPrompt + "\n"
    prompt += "sentence: \n" + sentence + "\n"
    prompt += "question at hand: " + qn + "\n"
    checks.write(hearer + "\n")
    checks.write("impt\n")
    checks.write(sentence + "\n")
    impt = check(prompt, hearer)
    for i in impt:
        if i in numbers:
            checks.write(i)
            checks.write("\n--------\n")
            return int(i)
            
        
    checks.write("ihatechatgptt    -    impt")
    checks.write("\n--------\n")
    return imptVal(sentence, hearer)

def relevVal(sentence, hearer):
    prompt = relevPrompt + "\n"
    prompt += "sentence: \n" + sentence + "\n"
    prompt += " conversation so far: \n" + convString + "\n"
    prompt += "question at hand: " + qn + "\n"
    checks.write(hearer + "\n")
    checks.write("relev\n")
    checks.write(sentence + "\n")
    relev = check(prompt, hearer)
    for i in relev:
        if i in numbers:
            checks.write(i)
            checks.write("\n--------\n")
            return int(i)
    checks.write("ihatechatgptt    -    relev")
    checks.write("\n--------\n")
    return relevVal(sentence, hearer)

def emoVal(sentence, hearer):
    prompt = emoPrompt + "\n"
    prompt += "sentence: \n" + sentence + "\n"
    prompt += "conversation so far:  \n" + convString + "\n"
    checks.write(hearer + "\n")
    checks.write("emo\n")
    checks.write(sentence + "\n")
    emo = check(prompt, hearer)
    for i in emo:
        if i in numbers:
            checks.write(i)
            checks.write("\n--------\n")
            return int(i)
    checks.write("ihatechatgptt    -    emo")
    checks.write("\n--------\n")
    return emoVal(sentence, hearer)


def reply(person):
    jmax = [[0, -1] for i in range(5)]
    
    # calculating retrieval value
    for j in range(len(convList)):        
        impt = characters[person+"Impt"][j]
        emo = characters[person+"Emo"][j]
        
        relev = relevVal(convList[j], person)
        recen = 0
        
        curr = impt + relev + emo + recen

        """print(convList[j])
        print("impt:", impt)
        print("relev:", relev)
        print("emo:", emo)
        print("recen:", recen)
        print()"""
        
        jmax.append([curr, j])
        jmax.sort()
        jmax.pop(0)
        
    memories = []
    for i in range(4, -1, -1):
        if jmax[i][1] != -1:
            memories.append(jmax[i][1])
    memories.sort()
    reply = ask(person + "Temp", memories, person)
    return reply

def summarise(sentence):
    prompt = summaryPrompt + "\n"
    prompt += sentence

    flag = True
    while flag:
        try:
            response = openai.ChatCompletion.create(
                deployment_id=deployment_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
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
    return full_response

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
    if full_response.strip() == "Kien Hong":
        return "kh"
    print("i hate chatgpt")
    return getPersonToRepond()

def getEmo(person):
    prompt = emosPrompt + "\n"
    
    prompt += "question at hand:" + qn + "\n"

    inputs.write(prompt)
    inputs.write("\n\n")
    
    flag = True
    while flag:
        try:
            context = "You are the following character in an ARGUMENTATIVE DISCUSSION: " + characters[person] + "\n"
            prompt += "conversation so far: \n" + convString
            response = openai.ChatCompletion.create(
                deployment_id=deployment_name,
                messages=[{"role": "system", "content": context},
                          {"role": "user", "content": prompt}],
                max_tokens=100,
                top_p=0.9,
                frequency_penalty=1.0,
                presence_penalty=1.0
            )

            full_response = response["choices"][0]["message"]["content"]
            flag = False
        except openai.error.RateLimitError as e:
            print(e)
            time.sleep(1)
    emotions.write(full_response)
    return full_response






            

#main


for i in people:
    x = reply(i)
    print(i + "\n"+ x)
    for j in people:
        impt = imptVal(i + ": " + x, j)
        emo = emoVal(i + ": " + x, j)
        characters[j + "Impt"][len(convList)] = impt
        characters[j + "Emo"][len(convList)] = emo
 

    summaryList.append(summarise(x))
            
    convList.append(i + ": " + x)
    convString += i + ": " + x + "\n\n"
        
for count in range(25):
    i = getPersonToRepond()
    x = reply(i)
        

    for j in people:
        impt = imptVal(i + ": " + x, j)
        emo = emoVal(i + ": " + x, j)
        characters[j + "Impt"][len(convList)] = impt
        characters[j + "Emo"][len(convList)] = emo


    summaryList.append(summarise(x))
            
    convList.append(i + ": " + x)
    convString += i + ": " + x + "\n\n"
    
      
        
    
    
end_time = time.time()
time_taken = end_time - start_time
print("total time taken:", time_taken)

convo.write(convString)
'''for i in range(len(convList)):
    print(i)
    print()'''

print("DONEE!!!!!!!")

lists = open("lists.txt", "w")

for i in range(len(convList)):
    lists.write(convList[i])
    lists.write("summary: " + summaryList[i])
    lists.write("\n")
    for j in people:
        lists.write(j+"Emo " + str(characters[j+"Emo"][i]))
        lists.write(j+"Impt " + str(characters[j+"Impt"][i]))
    lists.write("\n")
    lists.write("\n")

for j in people:
    lists.write(', '.join(str(i) for i in characters[j+"Emo"]))
    lists.write(', '.join(str(i) for i in characters[j+"Emo"]))
    
    
inputs.close()
convo.close()
checks.close()
emotions.close()
