def getInfo():
    file = open("inputfile.txt", "r", encoding='utf-8')
    quoteList = {}
    opinionList = {}


    characters = {
        "cadenTemp": 0.7,
        "cadenEmo": [-1 for i in range(100)],
        "cadenImpt": [-1 for i in range(100)],

        "zachTemp": 0.8,
        "zachEmo": [-1 for i in range(100)],
        "zachImpt": [-1 for i in range(100)],

        "khTemp": 0.3,
        "khEmo": [-1 for i in range(100)],
        "khImpt": [-1 for i in range(100)],

        "aadhiTemp": 0.9,
        "aadhiEmo": [-1 for i in range(100)],
        "aadhiImpt": [-1 for i in range(100)],

        "javenTemp": 0.4,
        "javenEmo": [-1 for i in range(100)],
        "javenImpt": [-1 for i in range(100)],
    }
    
    for i in ["caden", "zach", "kh", "aadhi", "javen"]:
        temp = ""
        x = file.readline()
        while x != "" and x.strip() != '':
            temp += x
            x = file.readline()

        opinionList[i] = file.readline()
        opinionList[i] += " " + file.readline()
        file.readline()
        quoteList[i] = file.readline()
        characters[i] = temp
        file.readline()

    

    imptPrompt = file.readline()
    relevPrompt = file.readline()
    emoPrompt = file.readline()
    askPrompt = file.readline()
    emosPrompt = file.readline()
    summaryPrompt = file.readline()
    respondPrompt = file.readline()
    qn = file.readline()

    promptList = [imptPrompt, relevPrompt, emoPrompt, askPrompt, emosPrompt, summaryPrompt, respondPrompt]
    
    file.close()
    print("file reading done!!")
    listFinal = [characters, promptList, quoteList, opinionList, qn]
    return listFinal
