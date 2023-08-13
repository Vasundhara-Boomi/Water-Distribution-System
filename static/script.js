document.addEventListener('DOMContentLoaded', function() {
  var map = L.map('map').setView([51.5074, -0.1278], 12);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data &copy; OpenStreetMap contributors',
    maxZoom: 18
  }).addTo(map);

  function addCurrentLocationMarker(lat, lon) {
    L.marker([lat, lon]).addTo(map)
      .bindPopup('Current Location')
      .openPopup();
  }

  function performSearch(query) {
    var xhttp = new XMLHttpRequest();
    xhttp.open('POST', '/search', true);
    xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhttp.onreadystatechange = function() {
      if (xhttp.readyState === XMLHttpRequest.DONE && xhttp.status === 200) {
        console.log('Search completed successfully!');
      }
    };
    xhttp.send('searchInput=' + encodeURIComponent(query));
  }

  var searchButton = document.getElementById('searchButton');
  searchButton.addEventListener('click', function() {
    var searchInput = document.getElementById('searchInput');
    var query = searchInput.value;
    performSearch(query);
  });

  navigator.geolocation.getCurrentPosition(function(position) {
    var lat = position.coords.latitude;
    var lon = position.coords.longitude;
    addCurrentLocationMarker(lat, lon);

    // Zoom to the current location
    map.setView([lat, lon], 15);
  });
});
