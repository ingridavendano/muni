


//Before Bck

function list_times(departure) {
    var table = $('<table>');

    for (var i = 0; i < departure.times.length; i++) {
        row = $('<tr>');
        row.append($('<td>').html(departure.times[i]));
        row.append($('<td>').html(departure.route + " - " + departure.direction));
        table.append(row)
    }

    $("#times").append(table);
}

function route(json) {

}

// data about the departures leaving a specific MUNI stop
function departures(json) {
    var stop = document.querySelector("#departure-stop");
    stop.innerHTML = json.name;

    console.log(json.name);
    console.log(json.code);

    for (var i = 0; i < json.departures.length; i++) {
        list_times(json.departures[i]);
    }
}


function success(position) {
    latitude = position.coords.latitude;
    longitude = position.coords.longitude;

    $.getJSON(
        "getTimes.json",
        {lat: latitude, lng: longitude}, 
        function(json) {
            departures(json);
            // console.log(json.name);
        } 
    )
    // $.ajax({
    //     url: "getTimes.json?lat=" + latitude + "&lng=" + longitude
    // })
    console.log(latitude);
    console.log(longitude);
}

function error(msg) {
    console.log(msg)
}

if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(success, error);
} else {
    error("NOT WORKING!");
}