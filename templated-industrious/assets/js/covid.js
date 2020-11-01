function initialize() {
	alert("here");
	var input = document.getElementById('searchTextField');
	new google.maps.places.Autocomplete(input);
  }