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

fetch('https://geohouse.github.io/blockIslandGlassFloats/summarized_fuzzyMatch_locationsFor_allYears.geojson')
.then(function (response) {
    let json = response.json();
    console.log(json);
    return json;
})
.then(function (points) {
    L.geoJson(points).addTo(map);
});          