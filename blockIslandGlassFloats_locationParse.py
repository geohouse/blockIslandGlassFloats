# Code to parse locations on Block Island where glass floats have been found

# Call as: 
# > py "C:\Users\Geoffrey House User\Documents\GitHub\blockIslandGlassFloats\blockIslandGlassFloats_locationParse.py"

# Uses fuzzy matching with fuzzywuzzy package to try and standardize the names
from fuzzywuzzy import process as fuzzProcess

print("test")

yearList = ['2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021']
currYear = ''

# No longer coding in the script. Named areas and locations now being read in from file below.
'''
masterLocationList = ["rodman's hollow", "enchanted forest", "mohegan bluffs", "north light",
"settler's rock", "clay head trail", "'the maze'", "sachem pond", "hodge family wildlife preserve",
"mansion beach", "andy's way", "scotch beach", "new harbor", "great salt pond", "harrison loop",
"bi greenway", "nathan mott park", "turnip farm", "loffredo loop", "meadow hill", "ocean view pavilion",
"southeast light", "payne overlook", "mohegan trail", "black rock beach", "lewis-dickens farm",
"win dodge", "fresh pond greenway", "fresh swamp", "payne farm trail", "beacon hill",
"logwood cove", "sacred labyrinth", "balls point", "west beach", "charlestown beach",
"grace's cove", "ball o' brien park", "crescent beach", "fred benson town beach", "new shoreham", 
"spring pond", "block island state airport", "abrams animal farm", "old harbor point", "tilson cove",
"lewis point", "dickens point", "southwest point", "cooneymus beach", 
"martin's point", "dorry's cove beach", "hodge property", "dinhgy beach", "mosquito beach", "vaill beach",
"cow cove", "baby beach", "surf beach", "ballard's beach"]
'''

masterLocationDict = {}

with open(r"C:\Users\Geoffrey House User\Documents\GitHub\blockIslandGlassFloats\blockIsland_namedLocationList_with_lat_lon.txt", 'r') as locFileIn:
    for line in locFileIn:
        # Skip the header line
        if line.startswith("location"):
            continue
        else:
            locationName = line.strip().split("\t")[0]
            masterLocationDict[locationName] = {'lat':0, 'lon':0}

print("The dict is:")
print(masterLocationDict)

masterLocationList = list(masterLocationDict.keys())

print("The list is:")
print(masterLocationList)

locationDict = {}
fuzzMatchedDict = {}

def getNearestFuzzyMatch(inputLocationName):
    # Check if all matches are equally bad; in this case, do not output anything
    allLocationsScored = fuzzProcess.extract(inputLocationName, masterLocationList)
    # Extract just the scores (not the words matching the scores)
    allScoresOnly = [score[1] for score in allLocationsScored]
    if all(x == allScoresOnly[0] for x in allScoresOnly):
        return([])
    else:
        # else return only the word with the highest match
        bestLocationMatch = fuzzProcess.extractOne(inputLocationName, masterLocationList)
        bestLocationName = bestLocationMatch[0]
        bestLocationScore = bestLocationMatch[1]
        return([bestLocationName,str(bestLocationScore)])

def makeOutputFile(year, locDict):
    outputFileName = 'summarized_fuzzyMatch_locationsFor_' + year + '.txt'
    sumEntries = 0
    # Sort by occurrence number of each location name descending
    sortedLocationDict = {k: v for k, v in sorted(locDict.items(), key=lambda item: item[1], reverse = True)}
    with open("C:/Users/Geoffrey House User/Documents/GitHub/blockIslandGlassFloats/" + outputFileName, 'w') as outFile:
        outFile.write('Location\tNumTimesListed\n')
        for key in sortedLocationDict:
            outFile.write("{}\t{}\n".format(key, sortedLocationDict[key]))
            sumEntries += int(sortedLocationDict[key])
    print("total num entries for: {} is: {}".format(year, sumEntries))

with open("C:/Users/Geoffrey House User/Documents/GitHub/blockIslandGlassFloats/BlockIsland_glassFloatFoundYears_locs_fromWebsite.txt", 'r', encoding='utf-8') as inFile:
    for line in inFile:
        stripLine = line.strip()
        # If the line is a new year's worth of entries
        if stripLine in yearList:
            # If this is the first year in the file, then assign it
            if currYear == '':
                currYear = stripLine
                continue
            # If there was another year's worth of entries encountered previously in the file, 
            # so process and output that one before moving to the next.
            if currYear != '':
                makeOutputFile(currYear, locationDict)
                locationDict = {}
                currYear = stripLine

        splitLine = stripLine.split(' - ')
        # This is a line that contains a location description where a float was found
        if len(splitLine) >= 3:
            floatLocation_initial = splitLine[2].lower()
            floatLocation_fuzzMatched = getNearestFuzzyMatch(floatLocation_initial)
            # If the fuzzy matching failed to return a clear best match, just use the 
            # initial location entry instead
            if floatLocation_fuzzMatched == []:
                floatLocation = floatLocation_initial
            else:
                floatLocation = floatLocation_fuzzMatched[0]
                floatLocationScore = floatLocation_fuzzMatched[1]
                # For testing the fuzzy matching only, add output match characteristics to a dict
                # for later output to a file for diagnostics
                if floatLocation_initial not in fuzzMatchedDict.keys():
                    fuzzMatchedDict[floatLocation_initial] = [floatLocation, floatLocationScore]

            if floatLocation in locationDict.keys():
                locationDict[floatLocation] += 1
            else:
                locationDict[floatLocation] = 1
    # Write the last year's of entries to a file
    makeOutputFile(currYear, locationDict)

with open("C:/Users/Geoffrey House User/Documents/GitHub/blockIslandGlassFloats/BlockIsland_glassFloats_locationFuzzyMatchOutcomes.txt", 'w') as fuzzyOutFile:
    fuzzyOutFile.write("originalEntry\tfuzzyMatchedEntry\tfuzzyMatchScore\n")
    for key in fuzzMatchedDict:
        fuzzyOutFile.write(key + "\t" + fuzzMatchedDict[key][0] + "\t" + fuzzMatchedDict[key][1] + "\n")


#print(floatLocation)