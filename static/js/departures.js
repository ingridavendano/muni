/* -------------------------------------------------------------------------
 * departure.js
 * Created by Ingrid Avendano on 1/15/14. 
 * -------------------------------------------------------------------------
 * Contains Backbone to have model and collections of nearest departures. 
 * ------------------------------------------------------------------------- */

var user, stops, coords;

var latitude, longitude;

/* ------------------------------------------------------------------------- 
 * Backbone for models: User, Departure, Stop, Coords and collection: Stops. 
 * ------------------------------------------------------------------------- */

// var Departure = Backbone.Model.extend();
var Stop = Backbone.Model.extend();

var Stops = Backbone.Collection.extend({
    initialize: function(args) {
        this.baseUrl = args.coords_url + '/stops';
    },
    defaults: function() {
        return {
            test: "ingrid"
        }
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

    // used urlRoot function so that the 'this' would immediately return 
    // url with new attribute data instead of getting confused with the 
    // 'this' from the Stops collection
    urlRoot: function() {
        return '/lat/' + this.get('lat')
            + '/lng/' + this.get('lng') 
            + '/rad/'+ this.get('rad');
    }
});

//views

var StopListView = Backbone.View.extend({
    initialize: function() {
        this.listenTo(this.collection, 'add', function(model,collection,opts) {
            var view = new StopView({'model':model}); 
            this.render(view) 
        });
    },
    render: function(view) {
        // append to the list the new view $el
        view.$el.appendTo(this.$el); 
    }
});

var FirstStopView = Backbone.View.extend({
    template: _.template($('#closest-stop-tmpl').html()),
    initialize: function() {
        this.listenTo(this.model, 'change', function(model, opts) {
            this.render();
        });
        this.render();
    },
    render: function() {
        this.$el.html(this.template({stop: this.model.attributes}));
        return this;
    },
});

var StopView = Backbone.View.extend({
    initialize: function (){
        this.render();
    },
    template: _.template($('#next-closest-stop-tmpl').html()),
    render: function() {
        this.$el.html(this.template({stop: this.model.attributes}));
        return this;
    }
});

var NextStopViews = Backbone.View.extend({
    initialize: function() {
        this.listenTo(this.collection, 'add', function(model,collection,opts) {
            
            if (this.collection.models[0] != model) {
                 model.attributes.index = collection.models.indexOf(model);

                var view = new StopView({'model':model}); 
                this.render(view) 
            }
        });
    },
    render: function(view) {
        view.$el.appendTo(this.$el);
    }
});

function linkRoutes(models) {
    console.log('models');
    for (var i = 0; i < models.length; i++) {
        console.log(models.at(i).attributes);
    }


}


/* ------------------------------------------------------------------------- */

function success(position) {
    latitude = position.coords.latitude;
    longitude = position.coords.longitude;
    var radius = 15;

    coords = new Coords({lat:latitude, lng:longitude, rad:radius});
    // stopsList = new NearestStopView({el:'#closest-stop', collection:coords.stops.models});
    // test = new LibraryView({el:'#target', collection: coords.stops});
    // coords.stops.fetch();

    nextStopViews = new NextStopViews({el:'#next-closest-stops', collection:coords.stops});

    // linkRoutes(coords.stops); 
    coords.stops.fetch({success:function() {
        //stuff that happens when a fetch is successful
        linkRoutes(coords.stops); 
        firstStopView = new FirstStopView({el:'#closest-stop', model:coords.stops.at(0)});
        
    
    }});
    // nextStopViews = new NextStopViews({el:'#next-closest-stops', collection:coords.stops.models}); 
    // nextStopViews = new NextStopViews({el:'#next-closest-stops', collection:coords.stops.models}); 
    var user_position = new google.maps.LatLng(latitude, longitude);
  
    var mapOptions = {
        center: new google.maps.LatLng(latitude+0.002, longitude+0.006),
        zoom: 15,
        navigationControl: true,
        mapTypeControl: false,
        scaleControl: true,
        draggable: false, 
    };

    var map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);

    var marker = new google.maps.Marker({
        position: user_position,
        map: map,
        title:"You are here!"
    });
}

function error(msg) {
    console.log(msg)
}

if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(success, error);
} else {
    error("NOT WORKING!");
}
