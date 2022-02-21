# Code to parse locations on Block Island where glass floats have been found

# Call as: 
# > py "C:\Users\Geoffrey House User\Documents\GitHub\blockIslandGlassFloats\blockIslandGlassFloats_locationParse.py"

# Uses fuzzy matching with fuzzywuzzy package to try and standardize the names
from fuzzywuzzy import process as fuzzProcess
from geojson import Point, Feature, dump

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
# This is a dict used when creating the output to lookup the fuzzy match name entry from the display name
# entry for a location (used to lookup the corresponding lat/lon for each site when making the output)
locationBackIndexDict = {}

with open(r"C:\Users\Geoffrey House User\Documents\GitHub\blockIslandGlassFloats\blockIsland_namedLocationList_with_lat_lon_v4.txt", 'r') as locFileIn:
    for line in locFileIn:
        # Skip the header line
        if line.startswith("matchLocation"):
            continue
        else:
            splitLine = line.strip().split("\t")
            locationName = splitLine[0]
            # This is the name to use in the map pop-up boxes and is standardized 
            # against multiple variations of the locationNames to try and match naming variations, etc.
            # This will also ensure the number of floats at each lat/lon point is tabulated correctly
            # regardless of naming variations
            locationDisplayName = splitLine[1]
            locationLat = splitLine[2]
            locationLon = splitLine[3]
            masterLocationDict[locationName] = {'displayName':locationDisplayName, 'lat':locationLat, 'lon':locationLon}
            locationBackIndexDict[locationDisplayName] = locationName
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

def makeOutputFile_txt(year, locDict):
    outputFileName = 'summarized_fuzzyMatch_locationsFor_' + year + '_v5.txt'
    sumEntries = 0
    # Sort by occurrence number of each location name descending
    sortedLocationDict = {k: v for k, v in sorted(locDict.items(), key=lambda item: item[1], reverse = True)}
    with open("C:/Users/Geoffrey House User/Documents/GitHub/blockIslandGlassFloats/" + outputFileName, 'w') as outFile:
        outFile.write('location\tlatitude\tlongitude\tnumTimesListed\tfloatType\n')
        for key in sortedLocationDict:
            # The keys are composites of the location combined with the float type (concat with '~')
            # so need to break them apart and recover both pieces of info to add to the output file
            # These locations are the display locations (not the fuzzy match locations)
            floatMatchLocation_display = key.split('~')[0]
            floatMatchLocation_fuzzy = locationBackIndexDict[floatMatchLocation_display]
            # Use the standardized location name to lookup the lat/lon for that location from the 
            # masterLocationDict
            floatLocation_lat = masterLocationDict[floatMatchLocation_fuzzy]['lat']
            floatLocation_lon = masterLocationDict[floatMatchLocation_fuzzy]['lon']
            # is "Fancy" (some) "Regular" (most), "Pumpkin" (3), or "Rona" (2)
            floatType = key.split('~')[1]
            outFile.write("{}\t{}\t{}\t{}\t{}\n".format(floatMatchLocation_display, floatLocation_lat, floatLocation_lon, sortedLocationDict[key], floatType))
            sumEntries += int(sortedLocationDict[key])
    print("total num entries for: {} is: {}".format(year, sumEntries))

# Create the output in geoJSON format (as a feature collection of point
# features with different properties)
def makeOutputFile_geoJSON(year, locDict):
    outputFileName = "C:/Users/Geoffrey House User/Documents/GitHub/blockIslandGlassFloats/summarized_fuzzyMatch_locationsFor_" + year + "_v4.geojson"
    sumEntries = 0
    jsonFeatureList = []
    # Sort by occurrence number of each location name descending
    # sortedLocationDict = sorted(test2.items(), key = lambda k_v: k_v[1]['count'], reverse = True)
    sortedLocationDict = {k: v for k, v in sorted(locDict.items(), key=lambda item: item[1], reverse = True)}
    for key in sortedLocationDict:
        # The keys are composites of the location combined with the float type (concat with '~')
        # so need to break them apart and recover both pieces of info to add to the output file
         # These locations are the display locations (not the fuzzy match locations)
        floatLocation_display = key.split('~')[0]
        floatLocation_fuzzy = locationBackIndexDict[floatLocation_display]
        # Use the standardized location name to lookup the lat/lon for that location from the 
        # masterLocationDict
        floatLocation_lat = float(masterLocationDict[floatLocation_fuzzy]['lat'])
        floatLocation_lon = float(masterLocationDict[floatLocation_fuzzy]['lon'])
        floatNum = sortedLocationDict[key]
        # is "Fancy" (some) "Regular" (most), "Pumpkin" (3), or "Rona" (2)
        floatType = key.split('~')[1]
        # geoJSON coords are lon, lat
        currFeature = Feature(geometry = Point((floatLocation_lon, floatLocation_lat)),
            properties= {'year': year, 'numFound': floatNum, 'floatType': floatType, 'locationName': floatLocation_display})
        jsonFeatureList.append(currFeature)
        sumEntries += int(sortedLocationDict[key])
    #jsonFeatureCollection = FeatureCollection(jsonFeatureList)
    with open(outputFileName, 'w') as outFile:
        dump(jsonFeatureList, outFile)
    print("total num entries for: {} is: {}".format(year, sumEntries))


# boolean for whether the current float is one of the first numbered ones of each year (and therefore is 
# fancy or pumpkin or rona (for 2020))
floatType = "Regular"

# This is a list to keep track of the entries that were dropped because the fuzzy match
# didn't work well. Can be used for further troubleshooting/manual editing some entries
# with otherwise clear locations so they can be used for mapping.
droppedLocationList = []

with open("C:/Users/Geoffrey House User/Documents/GitHub/blockIslandGlassFloats/BlockIsland_glassFloatFoundYears_locs_fromWebsite_manuallyLocationCurated.txt", 'r', encoding='utf-8') as inFile:
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
                makeOutputFile_txt(currYear, locationDict)
                makeOutputFile_geoJSON(currYear, locationDict)
                locationDict = {}
                currYear = stripLine
                floatType = "Regular"

        splitLine = stripLine.split(' - ')
        # This is a line that contains a location description where a float was found
        if len(splitLine) >= 3:
            # The number of the float for the current year (used to detemine whether it was a colored
            # fancy float - numbers up to and including the 20## part of the year) or a regular clear float.
            floatNumber = int(splitLine[0].lstrip('#'))
            # for 2020, there are 2 special fancy types - pumpkin and rona.
            if "Pumpkin" in splitLine[3:]:
                floatType = "Pumpkin"
            elif "Rona" in splitLine[3:]:
                floatType = "Rona"
            elif floatNumber <= int(currYear) - 2000:
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
                droppedLocationList.append(floatLocation_initial)
                continue
                floatLocation = floatLocation_initial
                
            else:
                # Use the fuzzMatched name as the dict key to find the corresponding site display name,
                # and use that display name for all downstream work (resolves some variant naming 
                # for the same location with the names for fuzzy matching, and puts the name in title case)
                floatLocation = masterLocationDict[floatLocation_fuzzMatched[0]]['displayName']
                floatLocationScore = floatLocation_fuzzMatched[1]
                # For testing the fuzzy matching only, add output match characteristics to a dict
                # for later output to a file for diagnostics
                if floatLocation_initial not in fuzzMatchedDict.keys():
                    # Use the actual fuzz matched, lowercase name (not the site display name, which is unique per location)
                    # here, because this makes the diagnostic file for tracking how well name variations for the same location were
                    # matched to the name inputs.
                    fuzzMatchedDict[floatLocation_initial] = [floatLocation_fuzzMatched[0], floatLocationScore]
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
    makeOutputFile_txt(currYear, locationDict)
    makeOutputFile_geoJSON(currYear, locationDict)
    # Write the combined entries across all years to a file
    makeOutputFile_txt('allYears', allYearLocationDict)
    makeOutputFile_geoJSON('allYears', allYearLocationDict)

# This is the tabulation output to judge how well the fuzzy matching worked for each entry.

with open("C:/Users/Geoffrey House User/Documents/GitHub/blockIslandGlassFloats/BlockIsland_glassFloats_locationFuzzyMatchOutcomes_v5.txt", 'w') as fuzzyOutFile:
    fuzzyOutFile.write("originalEntry\tfuzzyMatchedEntry\tfuzzyMatchScore\n")
    for key in fuzzMatchedDict:
        fuzzyOutFile.write(key + "\t" + fuzzMatchedDict[key][0] + "\t" + fuzzMatchedDict[key][1] + "\n")

with open("C:/Users/Geoffrey House User/Documents/GitHub/blockIslandGlassFloats/BlockIsland_glassFloats_locationDescriptsFailingFuzzyMatch_v5.txt", "w") as lookupFailFile:
    for entry in droppedLocationList:
        lookupFailFile.write(entry + "\n")
#print(floatLocation)