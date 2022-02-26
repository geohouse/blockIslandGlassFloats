var map = L.map('map').setView([41.18,-71.58],12);

var currentBackgroundLayer;
var backgroundSelector = document.getElementById("background-select");
function createMapBackground(){

    // Remove any current background layer if one exists.
    if(currentBackgroundLayer != undefined){
        map.removeLayer(currentBackgroundLayer);
    }

    var data = new FormData(backgroundSelector);
    var selectedBackground = "";
    for (const entry of data){
            selectedBackground = entry[1];
    }  
    console.log("The selected background is:");
    console.log(selectedBackground);

    if (selectedBackground == "watercolor"){
        currentBackgroundLayer = L.tileLayer('http://c.tile.stamen.com/watercolor/{z}/{x}/{y}.jpg', {
                attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under <a href="http://creativecommons.org/licenses/by-sa/3.0">CC BY SA</a>.',
        });
    }
            
    if (selectedBackground == "blackwhite"){
        currentBackgroundLayer = L.tileLayer('https://stamen-tiles.a.ssl.fastly.net/toner/{z}/{x}/{y}.png', {
                attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under <a href="http://www.openstreetmap.org/copyright">ODbL</a>.',
        });
    }
    if(selectedBackground == "aerial"){
        currentBackgroundLayer = L.tileLayer('https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}',{
                attribution: 'Map tiles by <a href="https://usgs.gov">Department of Interior/USGS</a>',
        });
    }
    currentBackgroundLayer.addTo(map);
}


backgroundSelector.addEventListener("change", createMapBackground);
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

// Build the url from the year to plot and the rest of the standardized url
let jsonUrlForData = ""

//allYearURL = 'https://geohouse.github.io/blockIslandGlassFloats/summarized_fuzzyMatch_locationsFor_allYears_v2.geojson';

function filterFloatTypes(geoJsonFeature, layer, floatTypeString){
    console.log(geoJsonFeature.properties.floatType);
    if (geoJsonFeature.properties.floatType == floatTypeString){
        //console.log("In true");
        return true;
    }
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
    let urlForData = "https://geohouse.github.io/blockIslandGlassFloats/summarized_fuzzyMatch_locationsFor_" + yearToPlot + "_v4.geojson";
    return urlForData;
}

/* See below for updated slider implementation to fix bugs.
// Check for updates made to the slider selection and re-map the selected years data.
// Every time the slider is moved, it first needs to remove any data from the 
// previously selected year before getting the updated slider selection otherwise those data layers become
// impossible to reliably select and remove later. Then the new data are plotted based on 
// which check boxes are selected.
//let slider = document.getElementById("slider");
function updateSlider(){
    if(regularFloatLayer != undefined){
        console.log("Slider removing regular");
        map.removeLayer(regularFloatLayer);
    }
    if(fancyFloatLayer != undefined){
        console.log("Slider removing fancy");
        map.removeLayer(fancyFloatLayer);
    }
    redrawFloats();
}

// The updateSlider function first clears any shown data for the current year,
// then calls redrawFloats() for the newly selected year to draw the selected data
// for the selected year.
slider.addEventListener("change", updateSlider);
*/

// Making a custom control. This is how to get buttons in corner of Leaflet map. A bit ugly though - need to create
// the DOM elements within Leaflet and passing the inner HTML as string.
// callbacks later find the elements by ID correctly.
var customControlFloatType = L.control();

customControlFloatType.update = function(properties){
    this._div.innerHTML = '<form><input type="checkbox" id="regular" name="regular" checked>' + 
        '<label for="regular">Regular floats</label><input type="checkbox" id="fancy" name="fancy" checked>' + 
        '<label for="fancy">Fancy floats</label></form>';
};

customControlFloatType.onAdd = function(map){
    this._div = L.DomUtil.create('div', 'button-div');
    this.update();
    
    // Normally a double click causes Leaflet to zoom to where is double clicked. This removes that
    // functionality from the buttons, because a double click can trigger (and therefore move/zoom the map)
    // when just trying to compare the float types and clicking fairly quickly. This doesn't affect the 
    // ability to double click to zoom anywhere else on the map. 
    // From: https://gist.github.com/rdaly1490/eb98fc5ff5be253c5610
    this._div.ondblclick = (e) => {
        e.stopPropagation();
        console.log("double clicked");
    };
    
    return this._div;

};


var customControlYearSlider = L.control();

customControlYearSlider.update = function(properties){
    this._div.innerHTML = '<label id="slide-label" for="slider">Years to map</label><input type = "range" id = "slider" name = "slider" min="1" max="11" step="1" value="1">' + 
    '<div class="sliderTicks">' + 
        '<p class="sliderTick">2012</p>' + 
        '<p class="sliderTick">2013</p>' + 
        '<p class="sliderTick">2014</p>' + 
        '<p class="sliderTick">2015</p>' + 
        '<p class="sliderTick">2016</p>' +
        '<p class="sliderTick">2017</p>' +
        '<p class="sliderTick">2018</p>' +
        '<p class="sliderTick">2019</p>' +
        '<p class="sliderTick">2020</p>' +
        '<p class="sliderTick">2021</p>' +
        '<p class="sliderTick">All</p>' + 
        '</div' + 
        '</div>';
};

customControlYearSlider.onAdd = function(map){
    this._div = L.DomUtil.create('div', 'slider-div');
    this.update();
    // Disable map dragging when clicking and dragging within the year slider box (makes it so the slider selects, but
    // doesn't pan the map at the same time)
    this._div.onmousedown = (e) => {
        map.dragging.disable();
        console.log("selected in slider");
    };
    this._div.onmouseup = () => {
        
        map.dragging.enable();
        console.log("selected in slider");
    };
    this._div.onmouseover = () => {
        
        map.dragging.disable();
        console.log("selected in slider");
    };
    this._div.onmouseout = () => {
        
        map.dragging.enable();
        console.log("selected in slider");
    };
        return this._div;
    };

customControlYearSlider.addTo(map);
customControlFloatType.addTo(map);

// Year from 2012-2021 (as string) or 'allYears'
//const yearToPlot = "2012";

// Reads the year selected for mapping from the slider, but the slider
// range is represented as 1-11, so need to convert to years
let sliderSelection = document.getElementById("slider").value;
let yearToPlot = "";
let yearToPlotNum = 0;
console.log("test");

function renderLayer(jsonData, floatTypeString){
    var renderedLayer = L.geoJson(jsonData, {
        filter: function(geoJsonFeature){
            console.log(geoJsonFeature.properties.floatType);
            if (floatTypeString == "Regular"){
                if (geoJsonFeature.properties.floatType == floatTypeString){
                //console.log("In true");
                return true;
                }
            }
            // Sort out all fancy floats and consider the rona and the pumpkin floats and the specific picture for 2021_17 to be fancy too
            if (floatTypeString == "Fancy"){
                if (geoJsonFeature.properties.floatType == floatTypeString || geoJsonFeature.properties.floatType == "Rona" || geoJsonFeature.properties.floatType == "Pumpkin" || geoJsonFeature.properties.floatType == "Fancy_2021_17"){
                    console.log(geoJsonFeature.properties.floatType);
                return true;
                }
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
            //console.log(yearToPlot);
            var scaleFactor = 0.0;
            if(yearToPlot == 'allYears'){
                scaleFactor = 1 + Math.log10(numFound * 10);
                console.log("setting all year scale factor.");
            } else{
                //Adds a 1/10 more size for each float found (starting with the second)
                scaleFactor = 1 + ((numFound - 1)/10);
            }
            
            var pathToIcon = "";

            if (geoJsonPoint.properties.floatType == "Regular"){
                pathToIcon = "css/images/RegularFloat.png"
            }
            if (geoJsonPoint.properties.floatType == "Fancy"){
                pathToIcon = "css/images/FancyFloat.png"
            }
            if (geoJsonPoint.properties.floatType == "Rona"){
                console.log("Rona");
                pathToIcon = "css/images/RonaFloat.png"
            }
            if (geoJsonPoint.properties.floatType == "Pumpkin"){
                pathToIcon = "css/images/PumpkinFloat.png"
            }
            if (geoJsonPoint.properties.floatType == "Fancy_2021_17"){
                pathToIcon = "css/images/Fancy_2021_17.png"
            }

            var floatIcon = L.icon({
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
            return L.marker(latlng, {icon: floatIcon});
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
        regularFloatLayer = renderLayer(jsonData, "Regular");
    
        regularFloatLayer.addTo(map);
    }

    if(plotFancy){
        fancyFloatLayer = renderLayer(jsonData, "Fancy");
    
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


console.log()

let regularFloatCheck = document.getElementById("regular");
//console.log(regularFloatCheck);
let fancyFloatCheck = document.getElementById("fancy");
//console.log(fancyFloatCheck);

function redrawFloats(){
    
    // Start by clearing any existing layers (this means that although it looks like 
    // regular or fancy floats can be added to existing floats, what actually happens is that 
    // the map is blanked out and the specified floats are served together from scratch. This
    // makes it possible to always identify and remove the necessary layers with any combination
    // of slider year selection and float selections.
    if(regularFloatLayer != undefined){
        console.log("Removing regular");
        map.removeLayer(regularFloatLayer);
    }
    if(fancyFloatLayer != undefined){
        console.log("Removing fancy");
        map.removeLayer(fancyFloatLayer);
    }

    sliderSelection = document.getElementById("slider").value;
    jsonUrlForData = createMapDataURL(sliderSelection);
    // Determine what float types are selected for mapping and send that info to the mapping function
    // if both checked, then just draw
    if(regularFloatCheck.checked && fancyFloatCheck.checked) {
        console.log("Fire if 1");
        plotPoints(jsonUrlForData,true, true);
    } else if(regularFloatCheck.checked){
        // if only regular checked, then clear fancy and plot regular
        console.log("Fire if 2");
        plotPoints(jsonUrlForData,true, false);
    } else if(fancyFloatCheck.checked){
        // if only fancy checked, then clear regular and plot fancy
        console.log("Fire if 3");
        plotPoints(jsonUrlForData, false, true);
    } 
}

let slider = document.getElementById("slider");
slider.addEventListener("change", redrawFloats);

regularFloatCheck.addEventListener("change", redrawFloats);
fancyFloatCheck.addEventListener("change", redrawFloats);

// This is the initial plot creation before any interaction
createMapBackground();
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