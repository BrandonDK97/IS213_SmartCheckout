// Initialize and add the map
function initMap() {
    if (!navigator.geolocation) {
        alert('Geolocation is not supported by your browser');
    } else {
        navigator.geolocation.getCurrentPosition(makeMap, error);

    }
}

function error(e) {
    console.log(e)
}

function makeMap(pos) {
    var lat = pos.coords.latitude;
    var lng = pos.coords.longitude;


    const uluru = { lat: lat, lng: lng };
    // The map, centered at Uluru
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 20,
        center: uluru,
    });
    // The marker, positioned at Uluru
    const marker = new google.maps.Marker({
        position: uluru,
        map: map,
    });

    info(lat, lng)
}


window.initMap = initMap;