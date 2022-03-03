# blockIslandGlassFloats
Code to parse and map locations where glass floats have been found on Block Island, RI. I was interested in seeing whether the places on the island where regular (clear) and fancy (decorated) glass floats have been found may have varied over the 10 years of the Glass Float Project. The glass floats for this project are made by artists Eben Horton, Jennifer Nauck and the glassblowers at [The Glass Station Studio and Gallery](https://theglassstationstudio.com/collections/glass-float-project) in Wakefield, Rhode Island. [See the final website here (displays best using Firefox)](https://geohouse.github.io/blockIslandGlassFloats)

## How this was built

1. List of floats found for each year, including the float number and where it was found was downloaded from the [Glass Float Project page](https://www.blockislandinfo.com/glass-float-project)
2. The most common location names were identified, and a latitude/longitude value for each location was determined using information about Block Island and Google Earth. These names and their corresponding locations were stored in a text file to use for lookup.
3. Built a fuzzy name identification script using the fuzzywuzzy package in Python.
4. Examined name identification output and refined by adding additional place names and location values to match most of the places where floats have been found. Added spelling variations for find locations to the lookup file, and manually standardized some locations to ensure correct lookup.
5. Extended the Python script to then process the named places where floats had been found and output standardized place names and locations for each year in GeoJSON format. This step also identified which floats were regular (clear), and which were fancy (decorated) floats (including the 2020 Rona and Pumpkin unique shape floats).
6. Wrote interactive mapping website using the Leaflet JavaScript library to subset and display the data from the GeoJSON files to match the combination of year, float type(s), and background map that the user selected. This includes interactive slider, radio button, and checkbox elements to allow the user to customize the map. 


