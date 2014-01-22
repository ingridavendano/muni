/* -------------------------------------------------------------------------
 * muni.js
 * Created by Ingrid Avendano on 1/15/14. 
 * -------------------------------------------------------------------------
 * Contains Backbone to have model and collections of nearest departures. 
 * ------------------------------------------------------------------------- */

var user, stops, coords;
var latitude, longitude;

/* ------------------------------------------------------------------------- 
 * Backbone for models: User, Departure, Stop, Coords and collection: Stops. 
 * ------------------------------------------------------------------------- */

var Stop = Backbone.Model.extend();

// collection build from stop
var Stops = Backbone.Collection.extend({
    initialize: function(args) {
        this.baseUrl = args.coords_url + '/stops';
    },
    url: function() {
        return this.baseUrl;
    },
    model: Stop
});

// latitude and longitude coordinates of a user
var Coords = Backbone.Model.extend({
    initialize: function(args) {
        var url = this.urlRoot()
        this.stops = new Stops({coords_url: url});
    },

    // used urlRoot function so that the 'this' would return 
    urlRoot: function() {
        return '/lat/' + this.get('lat')
            + '/lng/' + this.get('lng') 
            + '/rad/'+ this.get('rad');
    }
});

/* ------------------------------------------------------------------------- 
 * Backbone for Views.  
 * ------------------------------------------------------------------------- */

var StopsView = Backbone.View.extend({
    direction: 0,
    route: 0,
    template: _.template($('#active-stop-tmpl').html()),
    stop0: 0,
    stop1: 1,
    stop2: 2,
    model: null,
    events: {
        "click .change": "changeDirection",
        "click li.active a" : "changeRoute", 
        "click .next-stop-info .address": "changeStop",
    },
    initialize: function() {
        this.model = this.collection.models[this.stop0];
        this.listenTo(this.model, 'change', function(model, opts) {
            this.render();
        });
        this.render();
    },
    render: function() {
        // creating main view 
        this.$el.html(this.template({
            i: this.route,
            j: this.direction,
            stop: this.collection.models[this.stop0].attributes,
            otherStops: [
                this.collection.models[this.stop1], 
                this.collection.models[this.stop2]
            ],
            value: 0, 
        }));
        return this;
    },
    changeDirection: function() {
        if (this.direction) {
            this.direction = 0;
        } else {
            this.direction = 1;
        }
        this.render();
    },
    changeRoute: function() {
        this.route = arguments[0].currentTarget.firstElementChild.innerHTML;
        this.direction = 0;
        this.render();
    },
    changeStop: function() {
        tmpStop = this.stop0;
        this.stop0 = arguments[0].currentTarget.firstElementChild.innerHTML;

        // change direction that is viewed
        if (this.stop0 == this.stop1) {
            this.stop1 = tmpStop;
        } else if (this.stop0 == this.stop2) {
            this.stop2 = tmpStop;
        }

        // reset attributes for new direction
        this.route = 0;
        this.direction = 0;
        this.render();
    }
});

/* ------------------------------------------------------------------------- 
 * Get geolocation from user.
 * ------------------------------------------------------------------------- */

function success(position) {
    $(".geolocation-loading").html("loading data...");

    latitude = position.coords.latitude;
    longitude = position.coords.longitude;
    var radius = 15;

    // sync geolation to Coords collection
    coords = new Coords({lat:latitude, lng:longitude, rad:radius});

    // set Google Maps properties 
    var mapOptions = {
        center: new google.maps.LatLng(latitude+0.0008, longitude+0.001),
        zoom: 16,
        navigationControl: true,
        mapTypeControl: false,
        scaleControl: true,
        draggable: false, 
    };

    // fetch data from backend
    coords.stops.fetch({success:function() {

        // grab map element to project onto map
        var map = new google.maps.Map(
            document.getElementById("map-canvas"),
            mapOptions
            );

        // SVG of a circle to be used as Google Maps user marker
        var userPosition = {
                path: "M 0,0 m -75,0 a 75,75 0 1,0 150,0 a 75,75 0 1,0 -150,0",
                fillColor: '#2C3E50',
                fillOpacity: 1,
                scale: 0.1,
                strokeColor: '#2C3E50',
                strokeWeight: 4
              };
       
        var marker = new google.maps.Marker({
            position: new google.maps.LatLng(latitude, longitude),
            map: map,
            icon: userPosition,
            title:"You are here!"
        });

        var markerColor = ['#0A7B83', '#2AA876', '#F19C65'];

        var length = coords.stops.length; 
        if (length > 3)
            length = 3; 
        
        var stopsLatLng = [];

        for (var i = 0; i < length; i++) {
            console.log(coords.stops.at(i).attributes.lat);

            // SVG of a circle to be used as Google Maps stop marker
            var circle = {
                path: "M 0,0 m -75,0 a 75,75 0 1,0 150,0 a 75,75 0 1,0 -150,0",
                fillColor: 'transparent',
                fillOpacity: 0.8,
                scale: 0.2,
                strokeColor: markerColor[i], 
                strokeWeight: 5
              };

            // create a stop marker for where the position of all stops are
            var stopMarker = new google.maps.Marker({
                position: new google.maps.LatLng(
                    coords.stops.at(i).attributes.lat, 
                    coords.stops.at(i).attributes.lng
                ),
                map: map,
                icon: circle,
                title:"You are here!"
            });
        }

        // Backbone to create views
        firstStopView = new StopsView(
            {el:'#active-stop', collection:coords.stops}
        );
    }});
}

function error(msg) {
    console.log(msg)
}

// prompts the user for geolocation data 
if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(success, error);
} else {
    error("NOT WORKING!");
}
