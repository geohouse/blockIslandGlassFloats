# Code to parse locations on Block Island where glass floats have been found

# Call as: 
# > py "C:\Users\Geoffrey House User\Documents\GitHub\blockIslandGlassFloats\blockIslandGlassFloats_locationParse.py"

print("test")

with open("C:/Users/Geoffrey House User/Documents/GitHub/blockIslandGlassFloats/BlockIsland_glassFloatFoundYears_locs_fromWebsite.txt", 'r', encoding='utf-8') as inFile:
    for line in inFile:
        print(line.strip())