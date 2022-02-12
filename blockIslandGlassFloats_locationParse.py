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

with open(r"C:\Users\Geoffrey House User\Documents\GitHub\blockIslandGlassFloats\blockIsland_namedLocationList_with_lat_lon_v2.txt", 'r') as locFileIn:
    for line in locFileIn:
        # Skip the header line
        if line.startswith("location"):
            continue
        else:
            splitLine = line.strip().split("\t")
            locationName = splitLine[0]
            locationLat = splitLine[1]
            locationLon = splitLine[2]
            masterLocationDict[locationName] = {'lat':locationLat, 'lon':locationLon}

print("The dict is:")
print(masterLocationDict)

masterLocationList = list(masterLocationDict.keys())

print("The list is:")
print(masterLocationList)

# To store all of the find locations regardless of year.
allYearLocationDict = {}
locationDict = {}
fuzzMatchedDict = {}

def getNearestFuzzyMatch(inputLocationName, minScoreNeeded):
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
        # Only return the match if the score exceeds the needed threshold.
        if bestLocationScore >= minScoreNeeded:
            return([bestLocationName,str(bestLocationScore)])
        else:
            return([])

def makeOutputFile(year, locDict):
    outputFileName = 'summarized_fuzzyMatch_locationsFor_' + year + '_v3.txt'
    sumEntries = 0
    # Sort by occurrence number of each location name descending
    sortedLocationDict = {k: v for k, v in sorted(locDict.items(), key=lambda item: item[1], reverse = True)}
    with open("C:/Users/Geoffrey House User/Documents/GitHub/blockIslandGlassFloats/" + outputFileName, 'w') as outFile:
        outFile.write('location\tlatitude\tlongitude\tnumTimesListed\tfloatType\n')
        for key in sortedLocationDict:
            # The keys are composites of the location combined with the float type (concat with '~')
            # so need to break them apart and recover both pieces of info to add to the output file
            floatLocation = key.split('~')[0]
            # Use the standardized location name to lookup the lat/lon for that location from the 
            # masterLocationDict
            floatLocation_lat = masterLocationDict[floatLocation]['lat']
            floatLocation_lon = masterLocationDict[floatLocation]['lon']
            # is either "Fancy" or "Regular"
            floatType = key.split('~')[1]
            outFile.write("{}\t{}\t{}\t{}\t{}\n".format(floatLocation, floatLocation_lat, floatLocation_lon, sortedLocationDict[key], floatType))
            sumEntries += int(sortedLocationDict[key])
    print("total num entries for: {} is: {}".format(year, sumEntries))

# boolean for whether the current float is one of the first numbered ones of each year (and therefore is 
# fancy)
floatType = "Regular"

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
                floatType = "Regular"

        splitLine = stripLine.split(' - ')
        # This is a line that contains a location description where a float was found
        if len(splitLine) >= 3:
            # The number of the float for the current year (used to detemine whether it was a colored
            # fancy float - numbers up to and including the 20## part of the year) or a regular clear float.
            floatNumber = int(splitLine[0].lstrip('#'))
            if floatNumber <= int(currYear) - 2000:
                floatType = "Fancy"
            else:
                floatType = "Regular"
            
            floatLocation_initial = splitLine[2].lower()
            # Keep matches with scores >=63 (drop all others). This is based on looking at the 
            # quality of the matches and their scores. This discards ~6% of the matchable name entries.
            floatLocation_fuzzMatched = getNearestFuzzyMatch(floatLocation_initial,63)
            # If the fuzzy matching failed to return a clear best match, just use the 
            # initial location entry instead
            if floatLocation_fuzzMatched == []:
                # For production, prob. put continue here to just skip any entries that couldn't be
                # confidently looked-up
                continue
                floatLocation = floatLocation_initial
                
            else:
                floatLocation = floatLocation_fuzzMatched[0]
                floatLocationScore = floatLocation_fuzzMatched[1]
                # For testing the fuzzy matching only, add output match characteristics to a dict
                # for later output to a file for diagnostics
                if floatLocation_initial not in fuzzMatchedDict.keys():
                    fuzzMatchedDict[floatLocation_initial] = [floatLocation, floatLocationScore]
            # Make a composite key for each location and fancy float combination, as needed, 
            # sep. by '~'. Will be re-split and parsed back out when making the output file
            # so that there will be up to 2 rows per location (1 for normal, 1 for fancy), with
            # type denoted in another column.
            floatDictKey = floatLocation + "~" + floatType
            if floatDictKey in locationDict.keys():
                locationDict[floatDictKey] += 1
            else:
                locationDict[floatDictKey] = 1

            if floatDictKey in allYearLocationDict.keys():
                allYearLocationDict[floatDictKey] += 1
            else:
                allYearLocationDict[floatDictKey] = 1
    # Write the last year's of entries to a file
    makeOutputFile(currYear, locationDict)
    # Write the combined entries across all years to a file
    makeOutputFile('allYears', allYearLocationDict)

with open("C:/Users/Geoffrey House User/Documents/GitHub/blockIslandGlassFloats/BlockIsland_glassFloats_locationFuzzyMatchOutcomes_v3.txt", 'w') as fuzzyOutFile:
    fuzzyOutFile.write("originalEntry\tfuzzyMatchedEntry\tfuzzyMatchScore\n")
    for key in fuzzMatchedDict:
        fuzzyOutFile.write(key + "\t" + fuzzMatchedDict[key][0] + "\t" + fuzzMatchedDict[key][1] + "\n")


#print(floatLocation)