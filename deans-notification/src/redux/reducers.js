import * as actionTypes from "./actionTypes";
import { combineReducers } from "redux";

const initialState = {
  staff: {
    currentUser: null,
    isAdmin: false,
    flag: false,
    userList: null
  },
  system: {
    crisisType: null,
    assistanceType: null,
    emergencyAgencies: null
  },
  common: {
    flag: false,
    crises: null,
    psi: null,
    humidity: null,
    temperature: null,
    rainfall: null
  },
  modal: {
    modalType: null,
    modalProps: null
  }
};

const system = (state = initialState.system, action) => {
  const { type, payload } = action;
  const transform = obj => {
    const type = {};
    obj.forEach(val => {
      type[val.id] = val.name;
    });
    return type;
  };
  switch (type) {
    case actionTypes.FETCH_CRISIS_TYPE_SUCCESS:
      return {
        ...state,
        crisisType: transform(payload)
      };
    case actionTypes.FETCH_ASSISTANCE_TYPE_SUCCESS:
      return {
        ...state,
        assistanceType: transform(payload)
      };
    case actionTypes.FETCH_EMERGENCY_AGENCIES_SUCCESS:
      return {
        ...state,
        emergencyAgencies: payload
      };
    default:
      return state;
  }
};

// eslint-disable-next-line
const staff = (state = initialState.staff, action) => {
  const { type, payload } = action;
  switch (type) {
    case actionTypes.USER_LOGIN_REQUESTED:
      return {
        ...state,
        flag: false // reset flag
      };
    case actionTypes.USER_LOGIN_SUCCESS:
      localStorage.setItem("token", payload.key); // set token
      return {
        ...state,
        flag: true
      };
    case actionTypes.USER_LOGIN_FAILURE:
      return {
        ...state,
        flag: false
      };
    case actionTypes.USER_LOGOUT_REQUESTED:
      return {
        ...state,
        flag: false // reset flag
      };
    case actionTypes.USER_LOGOUT_SUCCESS:
      localStorage.removeItem("token"); // remove token
      return {
        ...state,
        currentUser: null,
        isAdmin: false,
        flag: true
      };
    case actionTypes.USER_LOGOUT_FAILURE:
      return {
        ...state,
        flag: false
      };
    case actionTypes.FETCH_USER_LIST_SUCCESS:
      return {
        ...state,
        userList: payload
      };
    case actionTypes.FETCH_CURRENT_USER_SUCCESS:
      return {
        ...state,
        currentUser: payload.username,
        isAdmin: payload.is_staff
      };
    case actionTypes.RESOLVE_CRISIS_REQUESTED:
      return {
        ...state,
        flag: false // reset flag
      };
    case actionTypes.RESOLVE_CRISIS_SUCCESS:
      return {
        ...state,
        flag: true
      };
    case actionTypes.RESOLVE_CRISIS_FAILURE:
      return {
        ...state,
        flag: false
      };
    case actionTypes.ADD_USER_REQUESTED:
      return {
        ...state,
        flag: false
      };
    case actionTypes.ADD_USER_SUCCESS:
      return {
        ...state,
        flag: true
      };
    case actionTypes.ADD_USER_FAILURE:
      return {
        ...state,
        flag: false
      };
    case actionTypes.EDIT_USER_REQUESTED:
      return {
        ...state,
        flag: false
      };
    case actionTypes.EDIT_USER_SUCCESS:
      return {
        ...state,
        flag: true
      };
    case actionTypes.EDIT_USER_FAILURE:
      return {
        ...state,
        flag: false
      };
    case actionTypes.ADD_CRISIS_TYPE_REQUESTED:
      return {
        ...state,
        flag: false
      };
    case actionTypes.ADD_CRISIS_TYPE_SUCCESS:
      return {
        ...state,
        flag: true
      };
    case actionTypes.ADD_CRISIS_TYPE_FAILURE:
      return {
        ...state,
        flag: false
      };
    case actionTypes.ADD_ASSISTANCE_TYPE_REQUESTED:
      return {
        ...state,
        flag: false
      };
    case actionTypes.ADD_ASSISTANCE_TYPE_SUCCESS:
      return {
        ...state,
        flag: true
      };
    case actionTypes.ADD_ASSISTANCE_TYPE_FAILURE:
      return {
        ...state,
        flag: false
      };
    case actionTypes.ADD_EMERGENCY_AGENCIES_REQUESTED:
      return {
        ...state,
        flag: false
      };
    case actionTypes.ADD_EMERGENCY_AGENCIES_SUCCESS:
      return {
        ...state,
        flag: true
      };
    case actionTypes.ADD_EMERGENCY_AGENCIES_FAILURE:
      return {
        ...state,
        flag: false
      };
    case actionTypes.EDIT_SITE_SETTINGS_REQUESTED:
      return {
        ...state,
        flag: false
      };
    case actionTypes.EDIT_SITE_SETTINGS_SUCCESS:
      return {
        ...state,
        flag: true
      };
    case actionTypes.EDIT_SITE_SETTINGS_FAILURE:
      return {
        ...state,
        flag: false
      };
    case actionTypes.EDIT_EMERGENCY_AGENCIES_REQUESTED:
      return {
        ...state,
        flag: false
      };
    case actionTypes.EDIT_EMERGENCY_AGENCIES_SUCCESS:
      return {
        ...state,
        flag: true
      };
    case actionTypes.EDIT_EMERGENCY_AGENCIES_FAILURE:
      return {
        ...state,
        flag: false
      };
    default:
      return state;
  }
};

const common = (state = initialState.common, action) => {
  const { type, payload } = action;
  switch (type) {
    case actionTypes.FETCH_CRISIS_SUCCESS:
      return {
        ...state,
        crises: payload
      };
    case actionTypes.FETCH_PSI_SUCCESS:
      return {
        ...state,
        psi: {
          status: payload && payload.api_info && payload.api_info.status,
          hourly:
            payload &&
            payload.items &&
            payload.items[0].readings.no2_one_hour_max
        }
      };
    case actionTypes.FETCH_HUMIDITY_SUCCESS:
      return {
        ...state,
        humidity: payload && payload.items && payload.items[0].readings[0].value
      };
    case actionTypes.FETCH_RAINFALL_SUCCESS:
      return {
        ...state,
        rainfall:
          payload && payload.items && payload.items[0].readings[23].value
      };
    case actionTypes.FETCH_TEMPERATURE_SUCCESS:
      return {
        ...state,
        temperature:
          payload && payload.items && payload.items[0].readings[0].value
      };
    case actionTypes.REPORT_CRISIS_REQUESTED:
      return {
        ...state,
        flag: false // reset flag
      };
    case actionTypes.REPORT_CRISIS_SUCCESS:
      return {
        ...state,
        flag: true
      };
    case actionTypes.REPORT_CRISIS_FAILURE:
      return {
        ...state,
        flag: false
      };
    default:
      return state;
  }
};

const modal = (state = initialState.modal, action) => {
  const { type, payload } = action;
  switch (type) {
    case actionTypes.MODAL_SHOW:
      return {
        ...state,
        modalType: payload.modalType,
        modalProps: payload.modalProps
      };
    case actionTypes.MODAL_HIDE:
      return {
        ...state,
        modalType: null,
        modalProps: null
      };
    default:
      return state;
  }
};

export default combineReducers({ modal, common, system, staff });
