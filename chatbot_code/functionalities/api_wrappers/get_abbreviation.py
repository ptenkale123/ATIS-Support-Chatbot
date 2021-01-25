import pandas as pd
import os

AIRLINES_DATA = ("../iata_data/airlines.dat", 'iata_code', [1], ['index','name','idk','iata_code', 'idk2', 'idk3', 'idk4', 'idk5'])
AIRPORTS_DATA = ("../iata_data/airport-codes.csv", 'iata_code', [2, 7], None)
AIRCRAFTS_DATA = ("../iata_data/planes.dat", 'iata_code', [0], ['name', 'idk', 'iata_code'])

def get_abbreviation(abbr, desiredDataSet):
    if desiredDataSet == "airlines":
        datasetTuple = AIRLINES_DATA
    elif desiredDataSet == "airports":
        datasetTuple = AIRPORTS_DATA
    elif desiredDataSet == "aircrafts":
        datasetTuple = AIRCRAFTS_DATA
    else:
        return []

    relativePath, desiredCol, desiredColIndices, columnNames, = datasetTuple

    dirName = os.path.dirname(__file__)
    filePath = os.path.join(dirName, relativePath)

    dataset = pd.read_csv(filePath, names=columnNames)
    allRows = dataset[dataset[desiredCol] == abbr.upper()].values
    if (len(allRows) <= 0):
        return []
    desiredRow = allRows[0]
    # example: desiredRow = [5209 'United Airlines' '\\N' 'UA' 'UAL' 'UNITED' 'United States' 'Y']
    ans = []
    for idx in desiredColIndices:
        ans.append(desiredRow[idx])
    return ans


if __name__ == "__main__":
    print(get_abbreviation("DC10", "aircrafts"))