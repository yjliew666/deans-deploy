import axios from "axios";

axios.defaults.baseURL = "http://localhost:8000/api";
axios.defaults.timeout = 5000;

const _getCSRFToken = () => {
  const cookies = document.cookie ? document.cookie.split("; ") : [];
  let csrftoken = "";
  cookies.forEach(cookie => {
    if (cookie.slice(0, 9) === "csrftoken") {
      csrftoken = cookie.slice(10);
    }
  });
  return csrftoken;
};

const _getAuthToken = () => {
  return localStorage.getItem("token");
};

export const getCrises = () => {
  return axios.get("/crises/");
};

export const reportCrises = form => {
  if (form) form.append("csrfmiddlewaretoken", _getCSRFToken());
  return axios.post("/crises/", form);
};

export const userLogin = form => {
  if (form) form.append("csrfmiddlewaretoken", _getCSRFToken());
  return axios.post("/rest-auth/login/", form); // it is important to keep the ending slash
};

export const userLogout = () => {
  const form = new FormData();
  form.append("csrfmiddlewaretoken", _getCSRFToken());
  return axios.post("/rest-auth/logout/", form); // it is important to keep the ending slash
};

export const getUserList = () => {
  return axios.get("/users/", {
    headers: {
      Authorization: `Token ${_getAuthToken()}`
    }
  });
};

export const getCrisisType = () => {
  return axios.get("/crisistype/");
};

export const getAssistanceType = () => {
  return axios.get("/crisisassistance/");
};

export const dispatchCrisis = (id, phoneNumberToNotify) => {
  return axios.put(
    "/crises/update-partial/" + id + "/",
    {
      crisis_status: "DP",
      phone_number_to_notify: phoneNumberToNotify
    },
    {
      headers: {
        Authorization: `Token ${_getAuthToken()}`
      }
    }
  );
};

export const resolveCrisis = (id, undo) => {
  return axios.put(
    "/crises/update-partial/" + id + "/",
    {
      crisis_status: undo ? "PD" : "RS"
    },
    {
      headers: {
        Authorization: `Token ${_getAuthToken()}`
      }
    }
  );
};

export const addUser = form => {
  return axios.post("/users/", form, {
    headers: {
      Authorization: `Token ${_getAuthToken()}`
    }
  });
};

export const editUser = (id, form) => {
  return axios.put("/users/update-partial/" + id + "/", form, {
    headers: {
      Authorization: `Token ${_getAuthToken()}`
    }
  });
};

export const addCrisisType = form => {
  return axios.post("/crisistype/", form, {
    headers: {
      Authorization: `Token ${_getAuthToken()}`
    }
  });
};

export const addAssistanceType = form => {
  return axios.post("/crisisassistance/", form, {
    headers: {
      Authorization: `Token ${_getAuthToken()}`
    }
  });
};

export const getEmergencyAgencies = () => {
  return axios.get("/emergencyagencies/");
};

export const addEmergencyAgencies = form => {
  return axios.post("/emergencyagencies/", form, {
    headers: {
      Authorization: `Token ${_getAuthToken()}`
    }
  });
};

export const editEmergencyAgencies = (id, form) => {
  return axios.put("/emergencyagencies/update-partial/" + id + "/", form, {
    headers: {
      Authorization: `Token ${_getAuthToken()}`
    }
  });
};

export const editSiteSettings = form => {
  return axios.post("/sitesettings/", form, {
    headers: {
      Authorization: `Token ${_getAuthToken()}`
    }
  });
};

export const getCurrentUser = () => {
  return axios.get("/rest-auth/user/", {
    headers: {
      Authorization: `Token ${_getAuthToken()}`
    }
  });
};

export const createWebSocket = () => {
  return new WebSocket("ws://localhost:8000/api/ws/crises/");
};

// from data.gov.sg
export const getHumidity = () => {
  return axios.get("https://api.data.gov.sg/v1/environment/relative-humidity");
};

// from data.gov.sg
export const getPSI = () => {
  return axios.get("https://api.data.gov.sg/v1/environment/psi");
};

// from data.gov.sg
export const getRainfall = () => {
  return axios.get("https://api.data.gov.sg/v1/environment/rainfall");
};

// from data.gov.sg
export const getTemperature = () => {
  return axios.get("https://api.data.gov.sg/v1/environment/air-temperature");
};
