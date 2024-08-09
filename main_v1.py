import os
import openai
import time
import inputfileread

openai.api_key = "xxx"
openai.api_base = 'xxx'
openai.api_type = 'azure'
openai.api_version = '2023-05-15'
deployment_name='IS463Deployment1'
bd = inputfileread.getInfo()
characters, promptList, quoteList, opinionList, qn = bd[0], bd[1], bd[2],bd[3],bd[4]
imptPrompt, relevPrompt, emoPrompt, askPrompt, emosPrompt, summaryPrompt, respondPrompt = promptList[0], promptList[1], promptList[2],promptList[3],promptList[4],promptList[5], promptList[6]
qn = "What are you views on meritocracy in singapore? Is it fair, and is it effective?"

start_time = time.time()

convo = open("a.txt", "w")
inputs = open("b.txt", "w")

def ask(temp, memories, person):
    prompt = askPrompt + "\n"

    if memories == []:
        prompt += "no one has said anything yet\n"
    else:
        prompt += "important parts of the conversation so far: \n"
    
    for i in memories:
        prompt += convList[i] + "\n"
    
    prompt += "question at hand:" + qn + "\n"
    inputs.write(prompt)
    inputs.write("\n\n")
    
    flag = True
    while flag:
        try:
            context = "You are: " + characters[person] + "\n"
            context += "This is a quote of how you normally speak: " + quoteList[person] + ". Replicate these speech patterns. \n"
            response = openai.ChatCompletion.create(
                deployment_id=deployment_name,
                messages=[{"role": "system", "content": context},
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

            
    return full_response
    
    
def check(prompt, person):
    flag = True
    while flag:
        try:
            context = "You are: " + characters[person] + "\n"
            context += "This is a quote of how you normally speak: " + quoteList[person] + ". Replicate these speech patterns. \n"
            response = openai.ChatCompletion.create(
                deployment_id=deployment_name,
                messages=[{"role": "system", "content": context},
                          {"role": "user", "content": prompt}],
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


num = list(range(1, 11))
numbers = [str(i) for i in num]

def imptVal(sentence, speaker, hearer):
    prompt = imptPrompt + "\n"
    prompt += "sentence: " + characters[sentence] + "\n"
    prompt += " conversation so far: " + convString + "\n"
    prompt += "question at hand:" + qn + "\n"
    
    impt = check(prompt, hearer)
    for i in impt:
        if i in numbers:
            impt = int(i)
            break
    #print(prompt)
    return impt

def relevVal(sentence, speaker, hearer):
    prompt = relevPrompt + "\n"
    prompt += "sentence: " + characters[sentence] + "\n"
    prompt += " conversation so far: " + convString + "\n"
    prompt += "question at hand:" + qn + "\n"
    
    relev = check(prompt, hearer)
    for i in relev:
        if i in numbers:
            relev = int(i)
            break
    #print(prompt)
    return relev

def emoVal(sentence, speaker, hearer):
    prompt = emoPrompt + "\n"
    prompt += "sentence: " + characters[sentence] + "\n"
    prompt += " conversation so far: " + convString + "\n"
    
    emo = check(prompt, hearer)
    for i in emo:
        if i in numbers:
            emo = int(i)
            break
    #print(prompt)
    return emo

conv = []
convList = []
convString = ""

def reply(person):
    jmax = [[0, -1] for i in range(5)]
    
    # calculating retrieval value
    for j in range(len(conv)):
        mem = conv[j]
        if characters[person+"Impt"][j] != -1:
            impt = characters[person+"Impt"][j]
        else:
            impt = imptVal(mem[0], mem[1], person)
            characters[person+"Impt"][j] = impt

        if characters[person+"Emo"][j] != -1:
            emo = characters[person+"Emo"][j]
        else:
            emo = emoVal(mem[0], mem[1], person)
            characters[person+"Emo"][j] = emo
        relev = relevVal(mem[0], mem[1], person)
        

        
        recen = 0 #change later
        
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



for i in range(25):
    # for i in ["javen", "zach", "aadhi", "kh", "caden"]:
    for i in ["zach", "kh", "caden", "javen"]:
        x = reply(i)
        if "-1" not in x:
            conv.append([i, x])
            convList.append(i + ": " + x)
            convString += i + ": " + x + "\n\n"
        else:
            print(i)
            print(x)
            print()
        
    
    
end_time = time.time()
time_taken = end_time - start_time
print("total time taken:", time_taken)

convo.write(convString)
print(convString)

for i in range(len(convList)):
    print(convList[i])
    for j in ["zach", "kh", "caden"]:
        print(j+"Emo" + str(characters[j+"Emo"][i]))
        print(j+"Impt" + str(characters[j+"Impt"][i]))
    print()
    
inputs.close()
convo.close()
