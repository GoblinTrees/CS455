import speech_recognition as sr
import random

activeRule = None
    
class DialogEngine:
    def __init__(self, rulesFile):
        self.dialogRules = self.loadRules(rulesFile)
        self.directories = self.loadDirectory(rulesFile)
        self.userVars = {}

    def loadDirectory(self, rulesFile):
        directory = {}
        try:
            with open(rulesFile, "r") as f:
                dominantRule = None
                currentSubruleIndex = None
                for line in f:
                    line = line.strip()
                    if line[0] != '#':
                        parts = line.split(":")
                        if parts[0][0] == '~':
                            name = parts[0].strip()
                            parts[1] = parts[1].replace('[','')
                            parts[1] = parts[1].replace(']','')
                            triggers = [t.strip() for t in parts[1].split()]
                            killArray = []
                            for i in range(len(triggers)):
                                if triggers[i][0] == '"':
                                    for j in range((i+1), len(triggers)):
                                        triggers[i] = triggers[i] + ' ' + triggers[j]
                                        killArray.append(j)
                                        if triggers[j][-1] == '"':
                                            i = j
                                            break
                            for x in reversed(killArray):
                                        del triggers[x]
                            directory[name] = {
                                "triggers": triggers}
        except FileNotFoundError:
            print(f"Error: File '{rulesFile}' not found.")
        #print(directory)
        return directory
    
    def loadRules(self, rulesFile):
        #rule format:
        #level : (user input) : [response]
        rules = {}
        #id num = {level, triggers, responses, subrules}
        directory = {}
        #name = {triggers}
        index = 0
        #if an input rule starts with ~, have it check user input with associated set
        try:
            with open(rulesFile, "r") as f:
                dominantRule = None
                currentSubruleIndex = None
                for line in f:
                    line = line.strip()
                    if line[0] != '#':
                        parts = line.split(":")
                        if parts[0][0] == '~':
                            name = parts[0].strip()
                            parts[1] = parts[1].replace('[','')
                            parts[1] = parts[1].replace(']','')
                            triggers = [t.strip() for t in parts[1].split()]
                            killArray = []
                            for i in range(len(triggers)):
                                if triggers[i][0] == '"':
                                    for j in range((i+1), len(triggers)):
                                        triggers[i] = triggers[i] + ' ' + triggers[j]
                                        killArray.append(j)
                                        if triggers[j][-1] == '"':
                                            i = j
                                            break
                            for x in reversed(killArray):
                                        del triggers[x]
                            directory[name] = {
                                "triggers": triggers}
                        else:
                            ruleLevel = parts[0].strip()
                            parts[1] = parts[1].replace('(','')
                            parts[1] = parts[1].replace(')','')
                            triggers = [parts[1].strip()]
                            if parts[2][0] == '[':
                                parts[2] = parts[2].replace('[','')
                                parts[2] = parts[2].replace(']','')
                                responses = [r.strip() for r in parts[2].split()]
                                killArray = []
                                for i in range(len(responses)):
                                    if responses[i][0] == '"':
                                        for j in range((i+1), len(responses)):
                                            responses[i] = responses[i] + ' ' + responses[j]
                                            killArray.append(j)
                                            if responses[j][-1] == '"':
                                                i = j
                                                break
                                for x in reversed(killArray):
                                    del responses[x]
                            else:
                                responses = [parts[2].strip()]
                            if ruleLevel == 'u':
                                subrules = []
                                rules[index] = {
                                    "level": ruleLevel.lower(),
                                    "triggers": triggers,
                                    "responses": responses,
                                    "subrules":subrules,
                                    "dominantRule":None}
                                dominantRuleIndex = index
                            else:
                                if ruleLevel == 'u1':
                                    rules[index] = {
                                        "level": ruleLevel.replace('u',''),
                                        "triggers": triggers,
                                        "responses": responses,
                                        "subrules":[],
                                        "dominantRule":rules[dominantRuleIndex]}
                                    subrules = rules[dominantRuleIndex].get("subrules")
                                    subrules.append(rules[index])
                                    rules[dominantRuleIndex]["subrules"] = subrules
                                    currentSubruleIndex = index
                                else:
                                    if ruleLevel == rules[currentSubruleIndex].get("level"):
                                        prevIndex = None
                                        for key, value in rules.items():
                                            if rules[currentSubruleIndex].get("dominantRule") == value:
                                                prevIndex = key
                                        currentSubruleIndex = prevIndex
                                        rules[index] = {
                                            "level": ruleLevel.replace('u',''),
                                            "triggers": triggers,
                                            "responses": responses,
                                            "subrules":[],
                                            "dominantRule":rules[currentSubruleIndex]}
                                        subrules = rules[currentSubruleIndex].get("subrules")
                                        subrules.append(rules[index])
                                        rules[currentSubruleIndex]["subrules"] = subrules
                                        currentSubruleIndex = index
                                    else:
                                        rules[index] = {
                                            "level": ruleLevel.replace('u',''),
                                            "triggers": triggers,
                                            "responses": responses,
                                            "subrules":[],
                                            "dominantRule":rules[currentSubruleIndex]}
                                        subrules = rules[currentSubruleIndex].get("subrules")
                                        subrules.append(rules[index])
                                        rules[currentSubruleIndex]["subrules"] = subrules
                                        currentSubruleIndex = index
                            index+=1          
                for i in rules:
                    print(rules[i])
        except FileNotFoundError:
            print(f"Error: File '{rulesFile}' not found.")
        return rules



    def processInput (self, userInput):
        global activeRule
        #print(activeRule)
        for index, rule in self.dialogRules.items():
            if rule.get("level") == 'u':
                for trigger in rule["triggers"]:
                    if trigger[0] == '~':
                        for entry in self.directories[trigger].get("triggers"):
                            if userInput.lower() == entry:
                                if len(rule.get("subrules")) != 0:
                                    activeRule = index
                                if len(rule.get("responses")) > 1:
                                    choice = random.choice(rule.get("responses"))
                                    if choice[0] == '~':
                                        return random.choice(self.directories[choice].get("triggers"))
                                    else:
                                        return choice
                                else:
                                    choice = rule.get("responses")[0]
                                    if choice[0] == '~':
                                        return random.choice(self.directories[choice].get("triggers"))
                                    else:
                                        return choice
                    else:
                        if trigger == userInput.lower():
                                if len(rule.get("subrules")) != 0:
                                    activeRule = index
                                if len(rule.get("responses")) > 1:
                                    choice = random.choice(rule.get("responses"))
                                    if choice[0] == '~':
                                        return random.choice(self.directories[choice].get("triggers"))
                                    else:
                                        return choice
                                else:
                                    choice = rule.get("responses")[0]
                                    if choice[0] == '~':
                                        return random.choice(self.directories[choice].get("triggers"))
                                    else:
                                        return choice
            else:
                if activeRule != None:
                    if self.dialogRules[activeRule] == rule.get("dominantRule"):
                        for trigger in rule["triggers"]:
                            if trigger[0] == '~':
                                for entry in self.directories[trigger].get("triggers"):
                                    if entry in userInput.lower():
                                        if len(rule.get("subrules")) != 0:
                                            activeRule = index
                                        if len(rule.get("responses")) > 1:
                                            choice = random.choice(rule.get("responses"))
                                            if choice[0] == '~':
                                                return random.choice(self.directories[choice].get("triggers"))
                                            else:
                                                return choice
                                        else:
                                            choice = rule.get("responses")[0]
                                            if choice[0] == '~':
                                                return random.choice(self.directories[choice].get("triggers"))
                                            else:
                                                return choice
                            else:
                                if trigger in userInput.lower():
                                        if len(rule.get("subrules")) != 0:
                                            activeRule = index
                                        if len(rule.get("responses")) > 1:
                                            choice = random.choice(rule.get("responses"))
                                            if choice[0] == '~':
                                                return random.choice(self.directories[choice].get("triggers"))
                                            else:
                                                return choice
                                        else:
                                            choice = rule.get("responses")[0]
                                            if choice[0] == '~':
                                                return random.choice(self.directories[choice].get("triggers"))
                                            else:
                                                return choice
        
        return "Unknown phrase"

    def variableRecognition(self, userInput):
        userInput = userInput.strip()
        for index, rule in self.dialogRules.items():
            #print(userInput)
            if userInput.find('_')>0:
               break 
            parts = userInput.split(" ")
            for i in rule.get("triggers"):
                if i.find('_')>0:
                    ruleset = i.split(" ")
                    tempcheck = True
                    for x in range(len(ruleset)):
                        if ruleset[x] != "_" and ruleset[x] != parts[x]:
                            tempcheck = False
                            break
                        elif ruleset[x] == "_" and parts[x] != ruleset[x]:
                            varName = None
                            for response in rule.get("responses"):
                                responsesBreak = response.split(" ")
                                for y in responsesBreak:
                                    if y[0] == '$':
                                        varName = y
                            self.userVars.update({varName:parts[x]})
                            parts[x] = "_"
                            break
                    if tempcheck == True:
                        userInput = i
                        break
        #print(self.userVars)
        return userInput

listening = True
rulesFile = "dialogRules.txt"
dialogEngine = DialogEngine(rulesFile)

while listening:
    with sr.Microphone() as source:
        r= sr.Recognizer()
        r.adjust_for_ambient_noise(source)
        r.dyanmic_energythreshhold = 3000
        
        try:
            print("listening")
            audio = r.listen(source)            
            print("Got audio")
            userInput = r.recognize_google(audio)
            print(userInput)
            userInput = dialogEngine.variableRecognition(userInput)
            print(userInput)
            response = dialogEngine.processInput(userInput)
            responseParts = response.split(" ")
            #fix replace var
            for x in range(len(responseParts)):
                if responseParts[x][0] == '$':
                    responseParts[x] = dialogEngine.userVars.get(responseParts[x])
            response = ""
            for i in responseParts:
                response = response + " " + i
            print(f"Bot: {response}")
        except sr.UnknownValueError:
            print("Don't knoe that werd")
