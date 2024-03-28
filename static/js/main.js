ymaps.ready(init);

function init() {
    var myMap = new ymaps.Map("map", {
        center: [43.238949, 76.889709], // Координаты Алматы
        zoom: 12
    });

    var myPlacemark = new ymaps.Placemark([43.238949, 76.889709], {
        hintContent: 'Алматы',
        balloonContent: 'Город в Казахстане'
    });

    myMap.geoObjects.add(myPlacemark);
}
