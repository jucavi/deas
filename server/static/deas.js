// import axios from 'axios'
function getPosition() {
  return new Promise((resolve, reject) => {
    window.navigator.geolocation.getCurrentPosition(resolve, reject);
  });
}

function addCard(deas) {
  const rowDiv = document.querySelector('#cards-deas');
  deas.forEach((dea) => {
    const cardWrapper = document.createElement('div')
    const cardDiv = document.createElement('div');
    const img = cardImg(dea[2], dea[3]);
    const bodyDiv = document.createElement('div');
    const wrapperText = document.createElement('div')
    const a = document.createElement('a');
    const a_url = `https://www.openstreetmap.org/#map=19/${dea[2]}/${dea[3]}&layers=N`;
    const pName = document.createElement('p');
    const pAddress = document.createElement('p');

    cardWrapper.classList.add('col-md-6', 'col-lg-4')

    cardDiv.classList.add('card', 'mb-4', 'box-shadow');


    img.classList.add('card-image-top');

    a.href = a_url;
    a.classList.add('btn', 'btn-success', 'mt-auto');
    a.innerHTML = 'See More';
    a.target = '_blank';

    bodyDiv.classList.add('card-body', 'd-flex', 'flex-column', 'align-content-between');

    bodyDiv.style.height = '230px'

    pName.innerHTML = dea[0];
    pAddress.innerHTML = `Direccion: ${dea[1]}`;

    wrapperText.append(pName);
    wrapperText.append(pAddress);

    bodyDiv.append(wrapperText);
    bodyDiv.append(a);

    cardDiv.append(img);
    cardDiv.append(bodyDiv);

    cardWrapper.append(cardDiv);

    rowDiv.append(cardWrapper);
  });
}

function cardImg(lat, lon) {
  const d_lon = 0.001913758;
  const d_lat = 0.000801975;
  const src = `https://www.openstreetmap.org/export/embed.html?bbox=${
    lon - d_lon
  }%2C${lat - d_lat}%2C${lon + d_lon}%2C${
    lat + d_lat
  }&amp;layer=mapnik&amp;marker=${lat}%2C${lon}`;
  const div = document.createElement('div');
  const iframe = document.createElement('iframe');

  iframe.style.width = '100%';
  iframe.style.height = '270px';
  iframe.src = src;

  div.append(iframe);

  return div;
}

const deas = async (size) => {
  const position = await getPosition();
  const lat = position.coords.latitude;
  const lon = position.coords.longitude;
  // const lat = 40.4331399;
  // const lon = - 3.6755304;
  const data = new FormData();
  data.append('lat', lat);
  data.append('lon', lon);
  data.append('size', size);

  const res = await axios.post('http://127.0.0.1:5000/finder', data);
  const deas = await res.data.deas;

  addCard(deas);
};

deas(6);
