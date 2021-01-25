from collections import defaultdict
import requests
import re

TEST_FILE = "datasets/finalTest.md"
NLU_MODEL_URL = 'http://localhost:5005/model/parse'

def testNLU(inputStr):
    inputData = '{"text":"'+inputStr+'"}'
    NLUres = requests.post(NLU_MODEL_URL, data=inputData)
    return NLUres.json()

def preprocessText(inputStr, entities):
    text = inputStr.lower()
    newStr = ""
    lastStartIdx = 0
    for m in entities:
        value = m.group(1)
        entity = m.group(2)
        start, end = m.span()
        newStr += text[lastStartIdx:start]
        newStr += value
        lastStartIdx = end
    
    if (lastStartIdx < len(inputStr)):
        newStr += text[lastStartIdx:]
    return newStr[2:].strip()

lineLimit = 100
i = 0

if __name__ == "__main__":
    # go through each sample
    testFile = open(TEST_FILE, 'r')

    numSamples = defaultdict(int)

    allPredictedIntents = set()

    intentConfusionMatrix = defaultdict(lambda: defaultdict(int))
    totalEntityCorrect = 0

    for line in testFile:
        # if (i > lineLimit):
        #     break
        # i += 1
        if re.match(r'^- ', line): # check if string begins with '- '
            # find all groups where [.*](.*) 

            actualEntities = [m for m in re.finditer(r'\[(.*?)\]\((.*?)\)', line)]

            # print("TEXT:")
            # print(preprocessText(line, actualEntities))

            rasaResponse = testNLU(preprocessText(line, actualEntities))

            predictedIntent = rasaResponse['intent']['name']
            predictedEntities = rasaResponse['entities']

            allPredictedIntents.add(predictedIntent)

            intentConfusionMatrix[actualIntent][predictedIntent] += 1

            numSamples[actualIntent] += 1

            # intiialize hashmap mapping {value, entity} -> frequency
            actualEntityFreq = defaultdict(int)
            actualEntityFreq_ = defaultdict(int)
            for m in actualEntities:
                value = m.group(1)
                entity = m.group(2)
                if (value == '' or entity == ''):
                    continue
                actualEntityFreq[(value, entity)] += 1

            # print(actualEntityFreq == actualEntityFreq_)
            # print("NEW ENTITY FREQ:")
            # print(actualEntityFreq)
            # print("ORIGINAL ENTITY FREQ:")
            # print(actualEntityFreq_)
            # print('')
            
            entitiesCorrect = True
            # check entities
            for entityObj in predictedEntities:
                if actualEntityFreq[(entityObj['value'], entityObj['entity'])] > 0:
                    actualEntityFreq[(entityObj['value'], entityObj['entity'])] -= 1
                else:
                    entitiesCorrect = False
                    break

            if (entitiesCorrect):
                totalEntityCorrect += 1

        else: 
            intentMatch = re.match(r'^## intent:(.*)', line)
            if intentMatch:
                actualIntent = intentMatch.group(1) # the text value of the intent after ':'
    
    intents = list(intentConfusionMatrix.keys())
    print('All Actual Intents')
    print(intents)
    print('')
    print('All Predicted Intents')
    print(allPredictedIntents)
    print('')

    # print intent class confusion matrix
    print('Intent Class Confusion Matrix: (Actual as rows, Predicted as columns)\n')

    numIntents = len(intents)

    formatStr = "{:<17} "*(numIntents+2)

    columnNames = ['']+intents+['class_accuracy']

    columns = formatStr.format(*columnNames)


    print(columns)

    # for predictedIntent in intents:
    #     print('\t'+predictedIntent, end='')
    # print('\tclass_accuracy')

    totalIntentCorrect = 0
    for actualIntent in intents:

        rowElements = [actualIntent]+[intentConfusionMatrix[actualIntent][predictedIntent] for predictedIntent in intents]

        # print(actualIntent+'\t', end='')
        # for predictedIntent in intents:
        #     print(str(intentConfusionMatrix[actualIntent][predictedIntent])+'\t', end='')

        totalIntentCorrect += intentConfusionMatrix[actualIntent][actualIntent]
        classAcc = (intentConfusionMatrix[actualIntent][actualIntent] / numSamples[actualIntent])
        rowElements.append(classAcc)
        # print(str(classAcc))
        print(formatStr.format(*rowElements))
    
    # print total accuracy
    totalSamples = sum(numSamples.values())

    print('')
    print('Total accuracy for Intent:', (totalIntentCorrect / totalSamples))
    print('Total accuracy for Entities:', (totalEntityCorrect / totalSamples))
    