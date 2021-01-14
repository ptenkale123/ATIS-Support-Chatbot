import re
import matplotlib.pyplot as plt
import numpy as np
import sys

'''
## intent:abbreviation
- what is [hp](airline_code)
- what 's the difference between fare code [q](fare_basis_code)

raw entities are 

{intent -> set of entities}
{entitity -> set of values}
'''

lineLimit = 233

if __name__ == "__main__":
    if len(sys.argv) < 4:
        sys.exit('Must have at least 3 additional arguments!')
    
    datasetFileTxt = sys.argv[1]
    intentAnalysisTxt = sys.argv[2]
    entityAnalysisTxt = sys.argv[3]
    datasetFile = open(datasetFileTxt, 'r')
    # datasetFile = ["- what []() airplane goes from [philadelphia](fromloc.city_name) to [san francisco](toloc.city_name) and stops in [dallas](stoploc.city_name) in the [afternoon](depart_time.period_of_day) on [monday](depart_date.day_name)"]
    # datasetFile = ["## intent:flight_time"]

    numSamples = {}
    intentToEntity = {}
    # need to analyze super entities (the thing with )

    subEntities = {}
    entityToValue = {}

    i = 0

    totalSamples = 0
    for line in datasetFile:
        # if (i >= lineLimit):
        #     break
        i += 1
        if re.match(r'^- ', line): # check if string begins with '- '
            # find all groups where [.*](.*) 
            entities = re.findall(r'\[(.*?)\]\((.*?)\)', line)

            totalSamples += 1
            numSamples[intent] = numSamples.setdefault(intent, 0) + 1
            
            for value, entity in entities:
                if (value == '' or entity == ''):
                    continue

                periodIdx = entity.find(".")
                rawEntity = entity
                if periodIdx >= 0: # period found
                    superEntity = entity[0:periodIdx]
                    intentToEntity[intent][0].add(superEntity)
                    rawEntity = entity[(periodIdx+1):]
                    if superEntity in subEntities:
                        subEntities[superEntity].add(rawEntity)
                    else:
                        subEntities[superEntity] = set([rawEntity])
                
                if rawEntity in entityToValue:
                    entityToValue[rawEntity].add(value)
                else:
                    entityToValue[rawEntity] = set([value])
                
                intentToEntity[intent][1][entity] = intentToEntity[intent][1].setdefault(entity, 0)+1
                # intentToEntity[intent][1].add(entity)
        else: 
            intentMatch = re.match(r'^## intent:(.*)', line)
            if intentMatch:
                intent = intentMatch.group(1) # the text value of the intent after ':'
                # intentToEntity[intent] = (set(), set())
                intentToEntity[intent] = (set(), {})

    print(numSamples)
    sampleStrings = list(numSamples.keys())
    sampleFreq = list(numSamples.values())
    
    intentAnalysis = open(intentAnalysisTxt, 'w')

    intentAnalysis.write('-------------------------------------\n')
    intentAnalysis.write("# of samples (total): " + str(totalSamples) + "\n")

    intentAnalysis.write('-------------------------------------\n')
    intentAnalysis.write("# of Intents: " + str(len(intentToEntity)) + "\n")
    intentAnalysis.write("INTENTS:\n")

    for intent in intentToEntity:
        intentAnalysis.write(intent+" "+str(numSamples[intent])+"\n")

    for intent in intentToEntity:
        intentAnalysis.write('-------------------------------------\n')
        intentAnalysis.write("INTENT: ")
        intentAnalysis.write(intent+"\n")
        intentAnalysis.write("# of Samples: "+str(numSamples[intent])+"\n")
        intentAnalysis.write("SUPER ENTITIES:\n")
        for entity in intentToEntity[intent][0]:
            intentAnalysis.write(entity+"\n")
        
        rawEntities = [entity for entity in intentToEntity[intent][1]]
        rawEntities.sort(key=len, reverse=True)
        intentAnalysis.write("RAW ENTITIES:\n")
        for entity in rawEntities:
            intentAnalysis.write(entity+" "+str(intentToEntity[intent][1][entity])+"\n")

    intentAnalysis.close()
    
    entityAnalysis = open(entityAnalysisTxt, 'w')
    entityAnalysis.write('-------------------------------------\n')
    entityAnalysis.write("# of Super Entities: " + str(len(subEntities)) + "\n")
    entityAnalysis.write("SUPER ENTITIES:\n")

    for superEntity in subEntities:
        entityAnalysis.write(superEntity+"\n")

    entityAnalysis.write('-------------------------------------\n')
    entityAnalysis.write("# of Raw Entities: " + str(len(entityToValue)) + "\n")
    entityAnalysis.write("RAW ENTITIES:\n")

    for entity in entityToValue:
        entityAnalysis.write(entity+"\n")

    for superEntity in subEntities:
        entityAnalysis.write('-------------------------------------\n')
        entityAnalysis.write("SUPER ENTITY: ")
        entityAnalysis.write(superEntity+"\n")
        entityAnalysis.write("RAW ENTITIES:\n")
        for rawEntity in subEntities[superEntity]:
            entityAnalysis.write(rawEntity+"\n")

    for entity in entityToValue:
        entityAnalysis.write('-------------------------------------\n')
        entityAnalysis.write("RAW ENTITY: ")
        entityAnalysis.write(entity+"\n")
        entityAnalysis.write("VALUES:\n")
        for value in entityToValue[entity]:
            entityAnalysis.write(value+"\n")
    
    entityAnalysis.close()

    w = 3

    fig, ax = plt.subplots()

    xAxis = np.arange(0, w*len(sampleStrings), w)

    ax.bar(xAxis, sampleFreq, width=w, align='center')
    ax.set_xticks(xAxis)
    ax.set_xticklabels(sampleStrings, rotation=90)
    plt.show()

