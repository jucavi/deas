// import axios from 'axios'

function getPosition() {
  return new Promise((resolve, reject) => {
    window.navigator.geolocation.getCurrentPosition(resolve, reject);
  });
}

const deas = async (size) => {
  const position = await getPosition();
  const lat = position.coords.latitude;
  const lon = position.coords.longitude;
  const data = { lat: lat, lon: lon, size: size }

  const res = await axios.post('http://loclahost:5000/deas', { data: data })
  console.log(res)
};

deas(6);
