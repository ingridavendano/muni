function times(json) {
    var rows = $('<td>');

    for (var i = 0; i < json.length; i++) {
        rows.append($('<tr>').html(json[i]));
    }

    $("#times").append(rows);
}

// data about the departures leaving a specific MUNI stop
function departures(json) {
    var stop = document.querySelector("#departure-stop");
    stop.innerHTML = json.name;

    console.log(json.name);
    console.log(json.code);

    for (var i = 0; i < json.departures.length; i++) {
        var route = document.querySelector("#departure-route");
        route.innerHTML = json.departures[i].route + " - " + json.departures[i].direction;

        times(json.departures[i].times);
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