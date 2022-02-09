# Code to parse locations on Block Island where glass floats have been found

# Call as: 
# > py "C:\Users\Geoffrey House User\Documents\GitHub\blockIslandGlassFloats\blockIslandGlassFloats_locationParse.py"

print("test")

yearList = ['2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021']
currYear = ''

masterLocationList = ["rodman's hollow", "enchanted forest", "mohegan bluffs", "north light",
"settler's rock", "clay head trail", "'the maze'", "sachern pond", "hodge family wildlife preserve",
"mansion beach", "andy's way", "scotch beach", "new harbor", "great salt pond", "harrison loop"]

locationDict = {}

def makeOutputFile(year, locDict):
    outputFileName = 'summarizedLocationsFor_' + year + '.txt'
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
            floatLocation = splitLine[2].lower()
            if floatLocation in locationDict.keys():
                locationDict[floatLocation] += 1
            else:
                locationDict[floatLocation] = 1
    # Write the last year's of entries to a file
    makeOutputFile(currYear, locationDict)




#print(floatLocation)