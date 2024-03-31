document.addEventListener('DOMContentLoaded', function() {
    ymaps.ready(init);
    fetchData();
});

function fetchData() {
    const almatyLat = 43.25667;
    const almatyLon = 76.92861;
    const radiusKm = 6000; // Радиус в километрах
    const minMagnitude = 5; // Минимальная магнитуда
    const url = `https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&latitude=${almatyLat}&longitude=${almatyLon}&maxradiuskm=${radiusKm}&minmagnitude=${minMagnitude}&limit=10`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            displayEarthquakes(data);
            addPlacemarks(data);
        })
        .catch(error => console.error('Ошибка при получении данных о землетрясениях:', error));
}

let myMap;

function init() {
    myMap = new ymaps.Map("map", {
        center: [43.25667, 76.92861], // Координаты Алматы
        zoom: 5
    });
}

function addPlacemarks(data) {
    data.features.forEach(earthquake => {
        const coords = earthquake.geometry.coordinates.slice(0, 2).reverse(); // Координаты для Яндекс.Карт
        const magnitude = earthquake.properties.mag;
        const place = earthquake.properties.place;
        const time = new Date(earthquake.properties.time).toLocaleString();

        const placemark = new ymaps.Placemark(coords, {
            hintContent: `Магнитуда: ${magnitude}`,
            balloonContent: `Место: ${place}<br>Время: ${time}`
        });

        myMap.geoObjects.add(placemark);
    });
}

function displayEarthquakes(data) {
    const earthquakeList = document.getElementById('earthquakeList');
    earthquakeList.innerHTML = ''; // Очистка списка

    data.features.forEach(earthquake => {
        const time = new Date(earthquake.properties.time).toLocaleString();
        const row = `<tr>
                       <td>${earthquake.properties.place}</td>
                       <td>${time}</td>
                       <td>${earthquake.properties.mag}</td>
                   </tr>`;
        earthquakeList.innerHTML += row;
    });
}
