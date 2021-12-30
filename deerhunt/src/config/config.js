// First we need to import axios.js
import axios from 'axios';
// Next we make an 'instance' of it
const instance = axios.create();

// Where you would set stuff like your 'Authorization' header, etc ...
instance.defaults.headers.common["Authorization"] =
  "Bearer " + localStorage.getItem("token");
var baseURL = process.env.REACT_APP_BASE_URL ? process.env.REACT_APP_BASE_URL : "UNDEFINED. THIS WILL CRASH";
instance.defaults.baseURL = baseURL;
console.log(baseURL);
export default instance;
