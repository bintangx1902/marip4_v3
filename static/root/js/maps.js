let map = L.map('map').setView([-6.200000,106.816666],13);
let lokasiAwal          = L.latLng(-6.1924492302, 106.851246595);
let lokasiAkhir         = L.latLng( -6.175392,106.827153);
let wayPointLawal       = new L.Routing.Waypoint(lokasiAwal);
let wayPointLakhir      = new L.Routing.Waypoint(lokasiAkhir);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);
L.Routing.control({
    waypoints : [lokasiAwal,lokasiAkhir]
}).addTo(map);
