var ngApp = angular.module('app', ['relativeDate']);

ngApp.controller('baseController', function($scope, $http){

    $scope.is_mobile = screen.height / screen.width >= 4/3;

    mapboxgl.accessToken = 'pk.eyJ1Ijoic2RlbmlzcyIsImEiOiJjazc2eWhrc3AwMjdnM2ZwOTh5emc0YTk3In0.GLdzpbgoNIp_CfhfRpkT0g';
    var map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/light-v10', //streets-v11 or light-v10
        center: [35.1974386,31.7661587],
        zoom: 8
    });

    var data = [];
    var popup = undefined;

    [[34.8022113, 32.1078663]].forEach(function(point) {

    });

    map.loadImage('/static/img/biohazard.png', function(error, image) {
       if (error) throw error;
       if (!map.hasImage('biohazard')) map.addImage('biohazard', image);
    });


    map.on('load', function() {

        map.setLayoutProperty('country-label', 'text-field', [
        'get',
        'name_en'
        ]);
        map.addSource('places', {
            'type': 'geojson',
            'data': {
                'type': 'FeatureCollection',
                'features': data
            }
        });
        // Add a layer showing the places.
        map.addLayer({
            'id': 'places',
            'type': 'symbol',
            'source': 'places',
            'layout': {
                'icon-image': 'biohazard',
                'icon-allow-overlap': true,
                'icon-size': 0.5
            }
        });

        // When a click event occurs on a feature in the places layer, open a popup at the
        // location of the feature, with description HTML from its properties.
        map.on('click', 'places', function(e) {
            var coordinates = e.features[0].geometry.coordinates.slice();
            var description = e.features[0].properties.description;

            // Ensure that if the map is zoomed out such that multiple
            // copies of the feature are visible, the popup appears
            // over the copy being pointed to.
            while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
                coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
            }

            new mapboxgl.Popup({className: 'mapPopup'})
                .setLngLat(coordinates)
                .setHTML(description)
                .addTo(map);

            map.flyTo({
                center: coordinates,
                zoom: 16
            });
        });

        // Change the cursor to a pointer when the mouse is over the places layer.
        map.on('mouseenter', 'places', function(e) {
            map.getCanvas().style.cursor = 'pointer';
            var coordinates = e.features[0].geometry.coordinates.slice();
            var description = e.features[0].properties.description;

            // Ensure that if the map is zoomed out such that multiple
            // copies of the feature are visible, the popup appears
            // over the copy being pointed to.
            while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
                coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
            }

            popup = new mapboxgl.Popup({className: 'mapPopup hoverPopup'})
                .setLngLat(coordinates)
                .setHTML(description)
                .addTo(map);
        });

        // Change it back to a pointer when it leaves.
        map.on('mouseleave', 'places', function() {
            map.getCanvas().style.cursor = '';
            popup.remove();
        });
    });
    $http.get('/api/dangerZone').then(function(response) {
        response.data.forEach(function(point) {
            data.push({
                        'type': 'Feature',
                        'properties': {
                            'description':
                                '<strong>' + point.label + '</strong>' +
                                '<p>' + point.description + '</p>' +
                                '<a href="' + point.link + '" target="_blank" title="Opens in a new window">עוד</a> ',
                            'icon': 'theatre'
                        },
                        'geometry': {
                            'type': 'Point',
                            'coordinates': point.position
                        }
                    });
        });
    });
});