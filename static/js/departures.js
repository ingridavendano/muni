/* -------------------------------------------------------------------------
 * departure.js
 * Created by Ingrid Avendano on 1/15/14. 
 * -------------------------------------------------------------------------
 * Contains Backbone to have model and collections of nearest departures. 
 * ------------------------------------------------------------------------- */

var user, stops, coords;

/* ------------------------------------------------------------------------- 
 * Backbone for models: User, Departure, Stop, Coords and collection: Stops. 
 * ------------------------------------------------------------------------- */

// var User = Backbone.Model.extend({
//     defaults: function() {
//         return {
//             lat: 0,
//             lng: 0,
//             radius: 1
//         }
//     }
// });

var Departure = Backbone.Model.extend({
    defaults: function() {
        return {
            direction: '', 
            route: '', 
            times: []
        }
    }
});

var Stop = Backbone.Model.extend({
    defaults: function() {
        return {
            dist: 0, 
            lat: 0, 
            lng: 0, 
            name: '', 
            departures: []
        }
    }
});

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
            //inside this function gets called every time an item is added to the colleciton
            var view = new StopView({'model':model}); //create item view
            this.render(view) //add item view to main view
        });
    },
    render: function(view) {
        view.$el.appendTo(this.$el); //append to the list the new view $el
    }
});

var StopView = Backbone.View.extend({
    initialize: function() {
        this.render(); // this renders when created
        this.listenTo(this.model, 'change:name', this.renderName) // this renders on change
    },
    render: function() {
        this.$el.html(this.model.get('departures')[0].times[0]);
        return this;
    },
    renderName: function() {
        var that = this;
        this.$el.fadeOut(1000, function(){that.render()})
    }
});

var DeparturesView = Backbone.View.extend({
    initialize: function() {
        this.render(); // this renders when created
        this.listenTo(this.model, 'name', this.renderName) // this renders on change
    },
    render: function() {
        this.$el.html(this.model.get('departures')[0].times[0]);
        return this;
    },
    renderName: function() {
        var that = this;
        this.$el.fadeOut(1000, function(){that.render()})
    }
})




/* ------------------------------------------------------------------------- */

function success(position) {
    var latitude = position.coords.latitude;
    var longitude = position.coords.longitude;
    var radius = 15;

    coords = new Coords({lat:latitude, lng:longitude, rad:radius});
    stopsList = new StopListView({el:'#times', collection:coords.stops});
    coords.stops.fetch();

    window.setInterval(function() {
        coords.stops.fetch();
    },1000*60); // update every 60 seconds


    console.log(stops);
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