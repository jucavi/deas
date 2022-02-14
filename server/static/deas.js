// import axios from 'axios'

function getPosition() {
  return new Promise((resolve, reject) => {
    window.navigator.geolocation.getCurrentPosition(resolve, reject);
  });
}

function addDeas(deas) {
  const tbody = document.querySelector('#deas');
  for (let dea of deas) {
    const tr = document.createElement('tr');
    const row = [dea[1], dea[2], dea[5]];
    row.forEach((field) => {
      console.log(field);
      const td = document.createElement('td');
      td.innerHTML = field;
      tr.append(td);
    });
    tbody.append(tr)
  }
}

const deas = async (size) => {
  const position = await getPosition();
  const lat = position.coords.latitude;
  const lon = position.coords.longitude;
  const data = { lat: lat, lon: lon, size: size };
  const res = await axios.post('http://127.0.0.1:5000/deas', data);
  const deas = await res.data.deas;
  addDeas(deas);
};

deas(6);
