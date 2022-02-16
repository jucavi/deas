// import axios from 'axios'
function getPosition() {
  return new Promise((resolve, reject) => {
    window.navigator.geolocation.getCurrentPosition(resolve, reject);
  });
}

{
  /* <div class="card" style="width: 18rem;">
  <img src="..." class="card-img-top" alt="...">
  <div class="card-body">
    <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
  </div>
</div> */
}

function addCard(deas) {
  const section = document.querySelector('#cards-deas');
  section.classList.add('row');
  deas.forEach((dea) => {
    const cardDiv = document.createElement('div');
    const img = cardImg(dea[2], dea[3]);
    const bodyDiv = document.createElement('div');
    const a = document.createElement('a');
    const a_url = `https://www.openstreetmap.org/#map=19/${dea[2]}/${dea[3]}&layers=N`;
    const pName = document.createElement('p');
    const pAddress = document.createElement('p');

    cardDiv.classList.add('card');
    cardDiv.classList.add('px-0');
    cardDiv.classList.add('py-0');
    // cardDiv.classList.add('m-1');


    img.classList.add('card-image-top');
    img.classList.add('text-center');

    a.href = a_url;
    a.classList.add('btn');
    a.classList.add('btn-success');
    a.innerHTML = 'See More';
    a.target = '_blank';

    bodyDiv.classList.add('card-body');

    pName.innerHTML = dea[0];
    pAddress.innerHTML = `Direccion: ${dea[1]}`;
    bodyDiv.append(pName);
    bodyDiv.append(pAddress);
    bodyDiv.append(a);
    cardDiv.classList.add('col-md-4');
    // cardDiv.classList.add('mx-1');
    // cardDiv.classList.add('my-1');
    cardDiv.append(img);
    cardDiv.append(bodyDiv);
    section.append(cardDiv);
  });
}

// function addDeas(deas) {
//   const tbody = document.querySelector('#deas');
//   for (let dea of deas) {
//     const tr = document.createElement('tr');
//     const row = [dea[1], dea[2], dea[5]];
//     row.forEach((field) => {
//       const td = document.createElement('td');
//       td.innerHTML = field;
//       tr.append(td);
//     });
//     tbody.append(tr);
//   }
// }

function cardImg(lat, lon) {
  const d_lon = 0.000334;
  const d_lat = 0.002245;
  const src = `https://www.openstreetmap.org/export/embed.html?bbox=${
    lon - d_lon
  }%2C${lat - d_lat}%2C${lon + d_lon}%2C${
    lat + d_lat
  }&amp;layer=mapnik&amp;marker=${lat}%2C${lon}`;
  const div = document.createElement('div');
  const iframe = document.createElement('iframe');
  // iframe.style.borderWidth = '1px';
  // iframe.style.borderColor = 'black';
  // iframe.style.borderStyle = 'solid';
  iframe.style.width = '100%';
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
  // const data = { lat: lat, lon: lon, size: size };
  const res = await axios.post('http://127.0.0.1:5000/finder', data);
  const deas = await res.data.deas;
  // const nearest_dea = deas[1];
  // maper(nearest_dea[3], nearest_dea[4]);
  // addDeas(deas);
  addCard(deas);
  // const div = document.createElement('div');
  // console.log(res['data'].toString());
  // div.innerHTML = res['data'].toString();
  // document.append(div)
};

deas(6);
