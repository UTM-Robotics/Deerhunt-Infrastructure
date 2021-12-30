// First we need to import axios.js
import axios from 'axios';
// Next we make an 'instance' of it
const instance = axios.create();

// Where you would set stuff like your 'Authorization' header, etc ...
instance.defaults.headers.common["Authorization"] =
  "Bearer " + localStorage.getItem("token");
var baseURL = process.env.REACT_APP_BASE_URL ? process.env.REACT_APP_BASE_URL : "poop://127.0.0.1:5000";
instance.defaults.baseURL = baseURL;
console.log("Base URL from env" + process);
export default instance;
