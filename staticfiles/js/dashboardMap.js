var events = new Array();
var userId;
var csrfToken;
var layerGroup;
var markerArray;
var functionality;

function setEvents(events)
{
window.events = [];
window.events = events;
console.log("events size" + events.length);
}

function setUserId(userId)
{
window.userId = userId;
}

function setCsrfToken(csrfToken)
{
window.csrfToken = csrfToken;
}

function setLayerGroup(layerGroup)
{
window.layerGroup = layerGroup;
}

function setMarkerArray(markerArray)
{
window.markerArray = markerArray;
}

function setFunctionality(functionality)
{
window.functionality = functionality;
}

function ajaxCall(map)
{
		var input_string = map.getZoom();
		var userLatitude = map.getCenter().lat;
		var userLongitude = map.getCenter().lng;
		
		$.ajax({
        type: "POST",
        url: "/ajaxMapRefresh/", 
		dataType: "json",
        data: { zoomFactor: input_string , userLatitude: userLatitude , userLongitude: userLongitude, userId : userId , csrfmiddlewaretoken: csrfToken },
        success: function(data) {
            refreshMarkersWithAJAXData(data,map,userId);
        },
        error: function(xhr, textStatus, errorThrown) {
            alert("Please report this error: "+errorThrown+xhr.status+xhr.responseText);
        }
		});;
}

	//Representing the user icon on the map
	var userIcon = L.icon({
		iconUrl: '/site_media/img/chef.png',

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


function refreshMarkersWithAJAXData(data,map,userId){
	//remove all markers
	
	var json = $.parseJSON(data);

	//var markerArray = new Array();
	var marker;
	
	window.layerGroup.clearLayers();
	window.markerArray=[];
	
	$(json).each(function(index,element){
		// for each event on the DB we draw a new marker
		var lat = element['fields']['latitude'];
		var lon = element['fields']['longitude'];
		var pk = element['pk'];
		var title = element['fields']['title'];
		var cuisine = element['fields']['cuisineType'];
		
		if(element['fields']['chef'] == userId)
		{
			marker = L.marker([lat, lon],{icon: homeIcon}).bindPopup(" This event is yours! <br> <a href='http://ncegcolnx323:8080/viewEvent/"+pk+"'>"+title+"</a>");
		}
		else if(cuisine == "African")
		{
			marker = L.marker([lat, lon],{icon: africanMarker}).bindPopup("<a href='http://ncegcolnx323:8080/viewEvent/"+pk+"'>"+title+"</a>");
		}
		else if(cuisine == "Anglo-Saxon")
		{
			marker = L.marker([lat, lon],{icon: angloSaxonMarker}).bindPopup("<a href='http://ncegcolnx323:8080/viewEvent/"+pk+"'>"+title+"</a>");
		}
		else if(cuisine == "Arab")
		{
			marker = L.marker([lat, lon],{icon: arabMarker}).bindPopup("<a href='http://ncegcolnx323:8080/viewEvent/"+pk+"'>"+title+"</a>");
		}
		else if(cuisine == "Asian")
		{
			marker = L.marker([lat, lon],{icon: asianMarker}).bindPopup("<a href='http://ncegcolnx323:8080/viewEvent/"+pk+"'>"+title+"</a>");
		}
		else if(cuisine == "Barbecue")
		{
			marker = L.marker([lat, lon],{icon: bbqMarker}).bindPopup("<a href='http://ncegcolnx323:8080/viewEvent/"+pk+"'>"+title+"</a>");
		}
		else if(cuisine == "Continental")
		{
			marker = L.marker([lat, lon],{icon: continentalMarker}).bindPopup("<a href='http://ncegcolnx323:8080/viewEvent/"+pk+"'>"+title+"</a>");
		}
		else if(cuisine == "Experimental")
		{
			marker = L.marker([lat, lon],{icon: experimentalMarker}).bindPopup("<a href='http://ncegcolnx323:8080/viewEvent/"+pk+"'>"+title+"</a>");
		}
		else if(cuisine == "Fusion")
		{
			marker = L.marker([lat, lon],{icon: fusionMarker}).bindPopup("<a href='http://ncegcolnx323:8080/viewEvent/"+pk+"'>"+title+"</a>");
		}
		else if(cuisine == "Indian")
		{
			marker = L.marker([lat, lon],{icon: indianMarker}).bindPopup("<a href='http://ncegcolnx323:8080/viewEvent/"+pk+"'>"+title+"</a>");
		}
		else if(cuisine == "Italian")
		{
			marker = L.marker([lat, lon],{icon: italianMarker}).bindPopup("<a href='http://ncegcolnx323:8080/viewEvent/"+pk+"'>"+title+"</a>");
		}
		else if(cuisine == "Kosher")
		{
			marker = L.marker([lat, lon],{icon: kosherMarker}).bindPopup("<a href='http://ncegcolnx323:8080/viewEvent/"+pk+"'>"+title+"</a>");
		}
		else if(cuisine == "Mediterranean")
		{
			marker = L.marker([lat, lon],{icon: mediterraneanMarker}).bindPopup("<a href='http://ncegcolnx323:8080/viewEvent/"+pk+"'>"+title+"</a>");
		}
		else if(cuisine == "Mexican")
		{
			marker = L.marker([lat, lon],{icon: mexicanMarker}).bindPopup("<a href='http://ncegcolnx323:8080/viewEvent/"+pk+"'>"+title+"</a>");
		}
		else if(cuisine == "Middle-East")
		{
			marker = L.marker([lat, lon],{icon: middleEastMarker}).bindPopup("<a href='http://ncegcolnx323:8080/viewEvent/"+pk+"'>"+title+"</a>");
		}
		else if(cuisine == "Nordic")
		{
			marker = L.marker([lat, lon],{icon: nordicMarker}).bindPopup("<a href='http://ncegcolnx323:8080/viewEvent/"+pk+"'>"+title+"</a>");
		}
		else if(cuisine == "Nouvelle")
		{
			marker = L.marker([lat, lon],{icon: nouvelleMarker}).bindPopup("<a href='http://ncegcolnx323:8080/viewEvent/"+pk+"'>"+title+"</a>");
		}
		else if(cuisine == "Oceanian")
		{
			marker = L.marker([lat, lon],{icon: oceanianMarker}).bindPopup("<a href='http://ncegcolnx323:8080/viewEvent/"+pk+"'>"+title+"</a>");
		}
		else if(cuisine == "Sushi")
		{
			marker = L.marker([lat, lon],{icon: sushiMarker}).bindPopup("<a href='http://ncegcolnx323:8080/viewEvent/"+pk+"'>"+title+"</a>");
		}
		else if(cuisine == "Vegetarian")
		{
			marker = L.marker([lat, lon],{icon: vegetarianMarker}).bindPopup("<a href='http://ncegcolnx323:8080/viewEvent/"+pk+"'>"+title+"</a>");
		}
		else if(cuisine == "Vegan")
		{
			marker = L.marker([lat, lon],{icon: veganMarker}).bindPopup("<a href='http://ncegcolnx323:8080/viewEvent/"+pk+"'>"+title+"</a>");
		}
		else{
			marker =	L.marker([lat, lon]).bindPopup("<a href='http://ncegcolnx323:8080/viewEvent/"+pk+"'>"+title+"</a>");
		}
		
		window.layerGroup.addLayer(marker).addTo(map);
	});

	
}

// This function returns the user location (coordinates) from the browser itself
	function getLocation()
	{
	//window.markerArray = new Array();
	if (navigator.geolocation)
		{
			navigator.geolocation.getCurrentPosition(calculateCoordinates);
		}
	else{alert("Geolocation is not supported by this browser.");}
	}

	// This function is using the geolocation coordinates to draw the map
	function calculateCoordinates(position) {
	
	latitude = position.coords.latitude;
	longitude = position.coords.longitude;
	
	drawMap(latitude,longitude);
	}

	function drawMap(latitude,longitude) {
	
	window.layerGroup.clearLayers();
	window.markerArray=[];
	
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
		.bindPopup("You are here!");
		
	var marker;

	if(window.functionality!="ViewEvent"){
		ajaxCall(map);
	}
	
	// for each event on the DB we draw a new marker
	for(var i = 0; i<events.length ; i++){
	console.log(events.length);
	if(events.length>0){
		var event = events[i];
		console.log(event);
		if(event){
			if(event.chef == userId)
			{
			marker = L.marker([event.latitude, event.longitude],{icon: homeIcon}).bindPopup(" This event is yours! <br> <a href='http://ncegcolnx323:8080/viewEvent/"+event.id+"'>"+event.title+"</a>");
			}
			else if(event.cuisine == "African")
			{
			marker = L.marker([event.latitude, event.longitude],{icon: africanMarker}).bindPopup("<a href='http://ncegcolnx323:8080/viewEvent/"+event.id+"'>"+event.title+"</a>");
			}
			else if(event.cuisine == "Anglo-Saxon")
			{
			marker = L.marker([event.latitude, event.longitude],{icon: angloSaxonMarker}).bindPopup("<a href='http://ncegcolnx323:8080/viewEvent/"+event.id+"'>"+event.title+"</a>");
			}
			else if(event.cuisine == "Arab")
			{
			marker = L.marker([event.latitude, event.longitude],{icon: arabMarker}).bindPopup("<a href='http://ncegcolnx323:8080/viewEvent/"+event.id+"'>"+event.title+"</a>");
			}
			else if(event.cuisine == "Asian")
			{
			marker = L.marker([event.latitude, event.longitude],{icon: asianMarker}).bindPopup("<a href='http://ncegcolnx323:8080/viewEvent/"+event.id+"'>"+event.title+"</a>");
			}
			else if(event.cuisine == "Barbecue")
			{
			marker = L.marker([event.latitude, event.longitude],{icon: bbqMarker}).bindPopup("<a href='http://ncegcolnx323:8080/viewEvent/"+event.id+"'>"+event.title+"</a>");
			}
			else if(event.cuisine == "Continental")
			{
			marker = L.marker([event.latitude, event.longitude],{icon: continentalMarker}).bindPopup("<a href='http://ncegcolnx323:8080/viewEvent/"+event.id+"'>"+event.title+"</a>");
			}
			else if(event.cuisine == "Experimental")
			{
			marker = L.marker([event.latitude, event.longitude],{icon: experimentalMarker}).bindPopup("<a href='http://ncegcolnx323:8080/viewEvent/"+event.id+"'>"+event.title+"</a>");
			}
			else if(event.cuisine == "Fusion")
			{
			marker = L.marker([event.latitude, event.longitude],{icon: fusionMarker}).bindPopup("<a href='http://ncegcolnx323:8080/viewEvent/"+event.id+"'>"+event.title+"</a>");
			}
			else if(event.cuisine == "Indian")
			{
			marker = L.marker([event.latitude, event.longitude],{icon: indianMarker}).bindPopup("<a href='http://ncegcolnx323:8080/viewEvent/"+event.id+"'>"+event.title+"</a>");
			}
			else if(event.cuisine == "Italian")
			{
			marker = L.marker([event.latitude, event.longitude],{icon: italianMarker}).bindPopup("<a href='http://ncegcolnx323:8080/viewEvent/"+event.id+"'>"+event.title+"</a>");
			}
			else if(event.cuisine == "Kosher")
			{
			marker = L.marker([event.latitude, event.longitude],{icon: kosherMarker}).bindPopup("<a href='http://ncegcolnx323:8080/viewEvent/"+event.id+"'>"+event.title+"</a>");
			}
			else if(event.cuisine == "Mediterranean")
			{
			marker = L.marker([event.latitude, event.longitude],{icon: mediterraneanMarker}).bindPopup("<a href='http://ncegcolnx323:8080/viewEvent/"+event.id+"'>"+event.title+"</a>");
			}
			else if(event.cuisine == "Mexican")
			{
			marker = L.marker([event.latitude, event.longitude],{icon: mexicanMarker}).bindPopup("<a href='http://ncegcolnx323:8080/viewEvent/"+event.id+"'>"+event.title+"</a>");
			}
			else if(event.cuisine == "Middle-East")
			{
			marker = L.marker([event.latitude, event.longitude],{icon: middleEastMarker}).bindPopup("<a href='http://ncegcolnx323:8080/viewEvent/"+event.id+"'>"+event.title+"</a>");
			}
			else if(event.cuisine == "Nordic")
			{
			marker = L.marker([event.latitude, event.longitude],{icon: nordicMarker}).bindPopup("<a href='http://ncegcolnx323:8080/viewEvent/"+event.id+"'>"+event.title+"</a>");
			}
			else if(event.cuisine == "Nouvelle")
			{
			marker = L.marker([event.latitude, event.longitude],{icon: nouvelleMarker}).bindPopup("<a href='http://ncegcolnx323:8080/viewEvent/"+event.id+"'>"+event.title+"</a>");
			}
			else if(event.cuisine == "Oceanian")
			{
			marker = L.marker([event.latitude, event.longitude],{icon: oceanianMarker}).bindPopup("<a href='http://ncegcolnx323:8080/viewEvent/"+event.id+"'>"+event.title+"</a>");
			}
			else if(event.cuisine == "Sushi")
			{
			marker = L.marker([event.latitude, event.longitude],{icon: sushiMarker}).bindPopup("<a href='http://ncegcolnx323:8080/viewEvent/"+event.id+"'>"+event.title+"</a>");
			}
			else if(event.cuisine == "Vegetarian")
			{
			marker = L.marker([event.latitude, event.longitude],{icon: vegetarianMarker}).bindPopup("<a href='http://ncegcolnx323:8080/viewEvent/"+event.id+"'>"+event.title+"</a>");
			}
			else if(event.cuisine == "Vegan")
			{
			marker = L.marker([event.latitude, event.longitude],{icon: veganMarker}).bindPopup("<a href='http://ncegcolnx323:8080/viewEvent/"+event.id+"'>"+event.title+"</a>");
			}
			else{
			marker =	L.marker([event.latitude, event.longitude]).bindPopup("<a href='http://ncegcolnx323:8080/viewEvent/"+event.id+"'>"+event.title+"</a>");
			}
			
		window.layerGroup.addLayer(marker).addTo(map);
			}
		//{% endfor %}
		}
	}
	var popup = L.popup();

	// this function deals with the onClick event
	function onMapClick(e) {
		popup
			.setLatLng(e.latlng)
			.setContent("You clicked the map at " + e.latlng.toString())
			.openOn(map);
	}
	
	// this function deals with the zoom event
	function onMapZoom(e) {
			if(window.functionality!="ViewEvent"){
				ajaxCall(map);	
			}
	}		

	map.on('click', onMapClick);
	
	map.on('zoomend', onMapZoom);
	
	map.on('dragend', onMapZoom);
	
	}