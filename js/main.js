var map = L.map('map').setView([41.18,-71.58],13);
L.tileLayer('http://c.tile.stamen.com/watercolor/{z}/{x}/{y}.jpg', {
                attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under <a href="http://creativecommons.org/licenses/by-sa/3.0">CC BY SA</a>.',
            }).addTo(map);
            //var marker = L.marker([51.5,-0.09]).addTo(map)
            
function pointStyle(feature) {
    return {
            fillColor: 'white',
            }
}

// Get the geoJSON information from the GitHub hosted
// URL, parse, and add the points to the map.
/*
async function getData(){
    const dataURL = 'https://geohouse.github.io/blockIslandGlassFloats/summarized_fuzzyMatch_locationsFor_allYears.geojson';
    //const request = new Request(dataURL);

    const response = await fetch(dataURL);
    const data_geoJSON = response.json();
    //console.log(data_geoJSON);
    return data_geoJSON;
}

geoJSON_data = getData();
console.log(geoJSON_data);
L.geoJson(geoJSON_data).addTo(map);
*/

// Year from 2012-2021 (as string) or 'allYears'
//const yearToPlot = "2012";

// Reads the year selected for mapping from the slider, but the slider
// range is represented as 1-11, so need to convert to years
let sliderSelection = document.getElementById("slider").value;
let yearToPlot = "";
let yearToPlotNum = 0;
console.log("test");

// Build the url from the year to plot and the rest of the standardized url
let jsonUrlForData = ""

//allYearURL = 'https://geohouse.github.io/blockIslandGlassFloats/summarized_fuzzyMatch_locationsFor_allYears_v2.geojson';

function filterFloatTypes(geoJsonFeature, layer, floatTypeString){
    console.log(geoJsonFeature.properties.floatType);
    if (geoJsonFeature.properties.floatType == floatTypeString){
        console.log("In true");
        return true;
    }
}


function renderLayer(jsonData, floatTypeString, pathToIcon){
    var renderedLayer = L.geoJson(jsonData, {
        filter: function(geoJsonFeature){
            console.log(geoJsonFeature.properties.floatType);
            if (geoJsonFeature.properties.floatType == floatTypeString){
                console.log("In true");
                return true;
            }
        }, pointToLayer: function(geoJsonPoint, latlng) {
            //console.log("The point is:");
            //console.log(geoJsonPoint);
            
            //console.log(geoJsonPoint.properties.numFound);
            // This accesses the entry for the number of floats found at the current location
            // for the current time frame. This is used to scale the icons, so points with
            // more floats found have larger icons.
            var numFound = geoJsonPoint.properties.numFound;
            //console.log(typeof(numFound));
            // These are the default icon dimensions, which will be scaled by the number of 
            // floats found at the location
            var regularIconSize_x = 25;
            var regularIconSize_y = 41;
            // Setting the scale factor to determine how much the number of floats found 
            // affects the icon size. 
            // Need especially aggressive down-scaling for all years otherwise the icon sizes
            // are too big.
            console.log(yearToPlot);
            var scaleFactor = 0.0;
            if(yearToPlot == 'allYears'){
                scaleFactor = 1 + Math.log10(numFound * 10);
                console.log("setting all year scale factor.");
            } else{
                //Adds a 1/10 more size for each float found (starting with the second)
                scaleFactor = 1 + ((numFound - 1)/10);
            }
            
            var regularFloatIcon = L.icon({
                //"css/images/marker-icon.png"
                iconUrl: pathToIcon,
                // Size [x,y] in pixels
                iconSize: [regularIconSize_x * scaleFactor, regularIconSize_y * scaleFactor],
                // Location in the icon that is the specified geographic location that it's 
                // marking (i.e. the 'tip' of the icon on the map). This is in pixels and 
                // is relative to the top left corner of the icon [x,y]
                iconAnchor: [(regularIconSize_x * scaleFactor) / 2, regularIconSize_y * scaleFactor]
                //popupAnchor: 
            });
            return L.marker(latlng, {icon: regularFloatIcon});
        }, onEachFeature: function(feature, layer){
            var locationName = feature.properties.locationName;
            var numFloatsFound = feature.properties.numFound;
            var floatType = feature.properties.floatType;
            //console.log(feature.properties.locationName);
            //The layer contains the information about the point location, so bind the popup directly to it
            // in order to avoid needing to pass lat/lon directly.
            layer.bindPopup('Location: ' + '<b>' + locationName + '</b>' + '</br>' + 
            'Float type: ' + '<b>' + floatType + '</b>' + '</br>' + 
            'Number found: ' + '<b>' + numFloatsFound + '</b>');
        }
    });
    return renderedLayer;
}

// Initialize the 2 possible layers here to have global scope so that the functions to add data and 
// remove data from the map can both access them.
var regularFloatLayer;
var fancyFloatLayer;

// plotReg and plotFancy are booleans for whether the regular float and the fancy float layers should
// be plotted or not (for the float type mapping selection checkboxes)
function plotPoints(url,plotReg,plotFancy){ 
$.getJSON(url, function(jsonData){
    // returns JSON as an object
    //console.log(typeof(jsonData));

    //console.log(jsonData.length);
    
    //for (i = 0; i < jsonData.length; i = i+1){
    //    console.log(jsonData[i].properties);
        // properties: year, numFound, floatType, locationName
    //}
    if(plotReg){
        regularFloatLayer = renderLayer(jsonData, "Regular", "css/images/marker-icon.png");
    
        regularFloatLayer.addTo(map);
    }

    if(plotFancy){
        fancyFloatLayer = renderLayer(jsonData, "Fancy", "css/images/leaf-green.png");
    
        fancyFloatLayer.addTo(map);
    }
    //console.log(regularFloatLayer);
    /*
    for (i = 0; i < regularFloatLayer.length; i = i+1){
        console.log(regularFloatLayer_layers[i].feature.properties);
        // properties: year, numFound, floatType, locationName
    }
    console.log(regularFloatLayer);
*/
    //L.geoJson(jsonData).addTo(map);
    
    

})
}

function createMapDataURL(sliderSelection){
    yearToPlot = "";
    yearToPlotNum = 0;
    // Convert the selection to a year by adding 2011; will pull out 2022 (the current 'allYear' entry
    // for data collected through 2021, below)
    yearToPlotNum = Number(sliderSelection) + 2011;
    if(yearToPlotNum == 2022){
        yearToPlot = "allYears";
    } else{
        yearToPlot = String(yearToPlotNum);
    }
    console.log("Year selected is:");
    console.log(yearToPlot);
    let urlForData = "https://geohouse.github.io/blockIslandGlassFloats/summarized_fuzzyMatch_locationsFor_" + yearToPlot + "_v3.geojson";
    return urlForData;
}

// Check for updates made to the slider selection and re-map the selected years data
/*let slider = document.getElementById("slider");
function updateSlider(){
    sliderSelection = document.getElementById("slider").value;
    jsonUrlForData = createMapDataURL(sliderSelection);
    // Clear the current points from the map before drawing the data from the selected year
    regularFloatLayer.clearLayers();
    fancyFloatLayer.clearLayers();
    plotPoints(jsonUrlForData,true, true);
}
slider.addEventListener("change", updateSlider);
*/
let regularFloatCheck = document.getElementById("regular");
console.log(regularFloatCheck);
let fancyFloatCheck = document.getElementById("fancy");
console.log(fancyFloatCheck);

function redrawFloats(){
    sliderSelection = document.getElementById("slider").value;
    jsonUrlForData = createMapDataURL(sliderSelection);
    // Determine what float types are selected for mapping and send that info to the mapping function
    // if both checked, then just draw
    if(regularFloatCheck.checked && fancyFloatCheck.checked) {
        plotPoints(jsonUrlForData,true, true);
    } else if(regularFloatCheck.checked){
        // if only regular checked, then clear fancy and plot regular
        if(fancyFloatLayer){
            fancyFloatLayer.clearLayers();
        }
        plotPoints(jsonUrlForData,true, false);
    } else if(fancyFloatCheck.checked){
        // if only fancy checked, then clear regular and plot fancy
        if(regularFloatLayer){
            regularFloatLayer.clearLayers();
        }
        plotPoints(jsonUrlForData, false, true);
    } else{
        // if neither checked, then clear both layers
        if(regularFloatLayer){
            regularFloatLayer.clearLayers();
        }
        if(fancyFloatLayer){
        fancyFloatLayer.clearLayers();
        }
    }
}

let slider = document.getElementById("slider");
slider.addEventListener("change", redrawFloats);

regularFloatCheck.addEventListener("change", redrawFloats);
fancyFloatCheck.addEventListener("change", redrawFloats);

// This is the initial plot creation before any interaction
redrawFloats();

/*
fetch('https://geohouse.github.io/blockIslandGlassFloats/summarized_fuzzyMatch_locationsFor_allYears_v2.geojson')
.then(function (response) {
    let json = response.json();
    console.log(json);
    return json;
})
.then(function (points) {
    L.geoJson(points).addTo(map);
});   
*/       