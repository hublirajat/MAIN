/*
	 * This code is representing a map mashup on the HTML page
	 */
	
	//Representing the user icon on the map
	var userIcon = L.icon({
		iconUrl: '/site_media/img/markers/userMarker.png',

		iconSize:     [40, 40], // size of the icon
		popupAnchor:[0,-20],
	});
	
	//Representing the user icon on the map
	var homeIcon = L.icon({
		iconUrl: '/site_media/img/markers/homeMarker.png',
		iconSize:     [36, 51],
        iconAnchor: [17, 51],
		popupAnchor:[0,-31],
	});
	
	var cuisineIcon = L.Icon.extend({
    options: {
        iconSize:     [36, 51],
        iconAnchor: [17, 51],
		popupAnchor:[0,-31],
    }
	});
	
	var africanMarker = new cuisineIcon({iconUrl: '/site_media/img/markers/africanMarker.png'}),
    angloSaxonMarker = new cuisineIcon({iconUrl: '/site_media/img/markers/angloSaxonMarker.png'}),
    arabMarker = new cuisineIcon({iconUrl: '/site_media/img/markers/arabMarker.png'}),
	asianMarker = new cuisineIcon({iconUrl: '/site_media/img/markers/asianMarker.png'}),
	bbqMarker = new cuisineIcon({iconUrl: '/site_media/img/markers/bbqMarker.png'}),
	continentalMarker = new cuisineIcon({iconUrl: '/site_media/img/markers/continentalMarker.png'}),
	experimentalMarker = new cuisineIcon({iconUrl: '/site_media/img/markers/experimentalMarker.png'}),
	fusionMarker = new cuisineIcon({iconUrl: '/site_media/img/markers/fusionMarker.png'}),
	indianMarker = new cuisineIcon({iconUrl: '/site_media/img/markers/indianMarker.png'}),
	italianMarker = new cuisineIcon({iconUrl: '/site_media/img/markers/italianMarker.png'}),
	kosherMarker = new cuisineIcon({iconUrl: '/site_media/img/markers/kosherMarker.png'}),
	mediterraneanMarker = new cuisineIcon({iconUrl: '/site_media/img/markers/mediterraneanMarker.png'}),
	mexicanMarker = new cuisineIcon({iconUrl: '/site_media/img/markers/mexicanMarker.png'}),
	middleEastMarker = new cuisineIcon({iconUrl: '/site_media/img/markers/middleEastMarker.png'}),
	nordicMarker = new cuisineIcon({iconUrl: '/site_media/img/markers/nordicMarker.png'}),
	nouvelleMarker = new cuisineIcon({iconUrl: '/site_media/img/markers/nouvelleMarker.png'}),
	oceanianMarker = new cuisineIcon({iconUrl: '/site_media/img/markers/oceanianMarker.png'}),
	sushiMarker = new cuisineIcon({iconUrl: '/site_media/img/markers/sushiMarker.png'}),
	vegetarianMarker = new cuisineIcon({iconUrl: '/site_media/img/markers/vegetarianMarker.png'}),
	veganMarker = new cuisineIcon({iconUrl: '/site_media/img/markers/veganMarker.png'});
	
	// This function returns the user location (coordinates) from the browser itself
	function getLocation()
	{
	if (navigator.geolocation)
		{
			navigator.geolocation.getCurrentPosition(drawMap);
		}
	else{alert("Geolocation is not supported by this browser.");}
	}

	// This function is using the geolocation coordinates to draw the map
	function drawMap(position) {
	
	var latitude = position.coords.latitude;
	var longitude = position.coords.longitude;

	// here we define the map with the user's location center and zoom factor of 10
	var map = L.map('map').setView([latitude, longitude], 10);
	L.tileLayer('https://{s}.tiles.mapbox.com/v3/{id}/{z}/{x}/{y}.png', {
		maxZoom: 18,
		attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
			'<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
			'Imagery © <a href="http://mapbox.com">Mapbox</a>',
		id: 'examples.map-i86knfo3'
	}).addTo(map);

	// here we add the marker representing the user's location
	L.marker([latitude, longitude], {icon: userIcon}).addTo(map)
		.bindPopup("You are here!").openPopup();

	var popup = L.popup();

	// this function deals with the onClick event
	function onMapClick(e) {
		popup
			.setLatLng(e.latlng)
			.setContent("You clicked the map at " + e.latlng.toString())
			.openOn(map);
	}

	map.on('click', onMapClick);
	}