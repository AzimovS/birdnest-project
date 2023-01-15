import axios from 'axios';

const API_ROOT = 'http://assignments.reaktor.com/birdnest';

export const getPilot = (serialNumber: string) => {
  return axios
    .get(`${API_ROOT}/pilots/${serialNumber}`)
    .then((res) => res.data);
};