import * as actionTypes from "./actionTypes";
import * as api from "@api";

export const startRealTimeCrisisTracking = () => dispatch => {
  let socket;
  const onOpen = () => {
    console.log("Socket connection established.");
    dispatch({
      type: actionTypes.FETCH_CRISIS_REQUESTED
    });
    api
      .getCrises()
      .then(response =>
        dispatch({
          type: actionTypes.FETCH_CRISIS_SUCCESS,
          payload: response.data
        })
      )
      .catch(() =>
        dispatch({
          type: actionTypes.FETCH_CRISIS_FAILURE
        })
      );
  };
  const onMessage = message => {
    console.log("Socket received message.");
    const crises = JSON.parse(message && message.data);
    dispatch({
      type: actionTypes.FETCH_CRISIS_SUCCESS,
      payload: crises
    });
  };
  const onException = () => {
    console.log("Socket connection error... Try again in 10 seconds.");
    setTimeout(() => {
      socket = api.createWebSocket();
      socket.onerror = onException;
      socket.onopen = onOpen;
      socket.onmessage = onMessage;
      // socket.onclose = onException;
    }, 10000);
  };

  socket = api.createWebSocket();
  socket.onerror = onException;
  socket.onopen = onOpen;
  socket.onmessage = onMessage;
};

export const startRealTimeConditionTracking = interval => {
  return async dispatch => {
    const job = () => {
      api
        .getPSI()
        .then(response =>
          dispatch({
            type: actionTypes.FETCH_PSI_SUCCESS,
            payload: response.data
          })
        )
        .catch(() =>
          dispatch({
            type: actionTypes.FETCH_PSI_FAILURE
          })
        );
      api
        .getHumidity()
        .then(response =>
          dispatch({
            type: actionTypes.FETCH_HUMIDITY_SUCCESS,
            payload: response.data
          })
        )
        .catch(() =>
          dispatch({
            type: actionTypes.FETCH_HUMIDITY_FAILURE
          })
        );
      api
        .getRainfall()
        .then(response =>
          dispatch({
            type: actionTypes.FETCH_RAINFALL_SUCCESS,
            payload: response.data
          })
        )
        .catch(() =>
          dispatch({
            type: actionTypes.FETCH_RAINFALL_FAILURE
          })
        );
      api
        .getTemperature()
        .then(response =>
          dispatch({
            type: actionTypes.FETCH_TEMPERATURE_SUCCESS,
            payload: response.data
          })
        )
        .catch(() =>
          dispatch({
            type: actionTypes.FETCH_TEMPERATURE_FAILURE
          })
        );
    };
    job();
    setInterval(job, interval);
  };
};

export const fetchTypes = () => {
  return async dispatch => {
    dispatch({
      type: actionTypes.FETCH_CRISIS_TYPE_REQUESTED
    });
    api
      .getCrisisType()
      .then(response =>
        dispatch({
          type: actionTypes.FETCH_CRISIS_TYPE_SUCCESS,
          payload: response.data
        })
      )
      .catch(() =>
        dispatch({
          type: actionTypes.FETCH_CRISIS_TYPE_FAILURE
        })
      );
    dispatch({
      type: actionTypes.FETCH_ASSISTANCE_TYPE_REQUESTED
    });
    api
      .getAssistanceType()
      .then(response =>
        dispatch({
          type: actionTypes.FETCH_ASSISTANCE_TYPE_SUCCESS,
          payload: response.data
        })
      )
      .catch(() =>
        dispatch({
          type: actionTypes.FETCH_ASSISTANCE_TYPE_FAILURE
        })
      );
    dispatch({
      type: actionTypes.FETCH_EMERGENCY_AGENCIES_REQUESTED
    });
    api
      .getEmergencyAgencies()
      .then(response =>
        dispatch({
          type: actionTypes.FETCH_EMERGENCY_AGENCIES_SUCCESS,
          payload: response.data
        })
      )
      .catch(() =>
        dispatch({
          type: actionTypes.FETCH_EMERGENCY_AGENCIES_FAILURE
        })
      );
  };
};

export const getCrises = () => {
  return async dispatch => {
    dispatch({
      type: actionTypes.FETCH_CRISIS_REQUESTED
    });
    api
      .getCrises()
      .then(response =>
        dispatch({
          type: actionTypes.FETCH_CRISIS_SUCCESS,
          payload: response.data
        })
      )
      .catch(() =>
        dispatch({
          type: actionTypes.FETCH_CRISIS_FAILURE
        })
      );
  };
};

export const getUserList = () => {
  return async dispatch => {
    dispatch({
      type: actionTypes.FETCH_USER_LIST_REQUESTED
    });
    api
      .getUserList()
      .then(response =>
        dispatch({
          type: actionTypes.FETCH_USER_LIST_SUCCESS,
          payload: response.data
        })
      )
      .catch(() =>
        dispatch({
          type: actionTypes.FETCH_USER_LIST_FAILURE
        })
      );
  };
};

export const reportCrises = form => {
  return async dispatch => {
    dispatch({
      type: actionTypes.REPORT_CRISIS_REQUESTED
    });
    await api
      .reportCrises(form)
      .then(() => dispatch({ type: actionTypes.REPORT_CRISIS_SUCCESS }))
      .catch(() => dispatch({ type: actionTypes.REPORT_CRISIS_FAILURE }));
  };
};

export const userLogin = form => {
  return async dispatch => {
    dispatch({
      type: actionTypes.USER_LOGIN_REQUESTED
    });
    await api
      .userLogin(form)
      .then(response => {
        dispatch({
          type: actionTypes.USER_LOGIN_SUCCESS,
          payload: response.data
        });
      })
      .catch(() => dispatch({ type: actionTypes.USER_LOGIN_FAILURE }));
  };
};

export const userLogout = form => {
  return async dispatch => {
    dispatch({
      type: actionTypes.USER_LOGOUT_REQUESTED
    });
    await api
      .userLogout(form)
      .then(() => {
        dispatch({
          type: actionTypes.USER_LOGOUT_SUCCESS
        });
      })
      .catch(() => dispatch({ type: actionTypes.USER_LOGOUT_FAILURE }));
  };
};

export const resolveCrisis = (id, undo) => {
  return async dispatch => {
    dispatch({
      type: actionTypes.RESOLVE_CRISIS_REQUESTED
    });
    await api
      .resolveCrisis(id, undo)
      .then(() => {
        dispatch({
          type: actionTypes.RESOLVE_CRISIS_SUCCESS
        });
      })
      .catch(() => dispatch({ type: actionTypes.RESOLVE_CRISIS_FAILURE }));
  };
};

export const addUser = form => {
  return async dispatch => {
    dispatch({
      type: actionTypes.ADD_USER_REQUESTED
    });
    await api
      .addUser(form)
      .then(() => {
        dispatch({
          type: actionTypes.ADD_USER_SUCCESS
        });
      })
      .catch(() => dispatch({ type: actionTypes.ADD_USER_FAILURE }));
  };
};

export const editUser = (id, form) => {
  return async dispatch => {
    dispatch({
      type: actionTypes.EDIT_USER_REQUESTED
    });
    await api
      .editUser(id, form)
      .then(() => {
        dispatch({
          type: actionTypes.EDIT_USER_SUCCESS
        });
      })
      .catch(() => dispatch({ type: actionTypes.EDIT_USER_FAILURE }));
  };
};

export const addCrisisType = form => {
  return async dispatch => {
    dispatch({
      type: actionTypes.ADD_CRISIS_TYPE_REQUESTED
    });
    await api
      .addCrisisType(form)
      .then(() => {
        dispatch({ type: actionTypes.ADD_CRISIS_TYPE_SUCCESS });
      })
      .catch(() => dispatch({ type: actionTypes.ADD_CRISIS_TYPE_FAILURE }));
  };
};

export const addAssistanceType = form => {
  return async dispatch => {
    dispatch({
      type: actionTypes.ADD_ASSISTANCE_TYPE_REQUESTED
    });
    await api
      .addAssistanceType(form)
      .then(() => {
        dispatch({ type: actionTypes.ADD_ASSISTANCE_TYPE_SUCCESS });
      })
      .catch(() => dispatch({ type: actionTypes.ADD_ASSISTANCE_TYPE_FAILURE }));
  };
};

export const getEmergencyAgencies = () => {
  return async dispatch => {
    dispatch({
      type: actionTypes.FETCH_EMERGENCY_AGENCIES_REQUESTED
    });
    api
      .getEmergencyAgencies()
      .then(response =>
        dispatch({
          type: actionTypes.FETCH_EMERGENCY_AGENCIES_SUCCESS,
          payload: response.data
        })
      )
      .catch(() =>
        dispatch({
          type: actionTypes.FETCH_EMERGENCY_AGENCIES_FAILURE
        })
      );
  };
};

export const editEmergencyAgencies = (id, form) => {
  return async dispatch => {
    dispatch({
      type: actionTypes.EDIT_EMERGENCY_AGENCIES_REQUESTED
    });
    await api
      .editEmergencyAgencies(id, form)
      .then(response =>
        dispatch({
          type: actionTypes.EDIT_EMERGENCY_AGENCIES_SUCCESS,
          payload: response.data
        })
      )
      .catch(() =>
        dispatch({
          type: actionTypes.EDIT_EMERGENCY_AGENCIES_FAILURE
        })
      );
  };
};

export const addEmergencyAgencies = form => {
  return async dispatch => {
    dispatch({
      type: actionTypes.ADD_EMERGENCY_AGENCIES_REQUESTED
    });
    await api
      .addEmergencyAgencies(form)
      .then(() => {
        dispatch({ type: actionTypes.ADD_EMERGENCY_AGENCIES_SUCCESS });
      })
      .catch(() =>
        dispatch({ type: actionTypes.ADD_EMERGENCY_AGENCIES_FAILURE })
      );
  };
};

export const editSiteSettings = form => {
  return async dispatch => {
    dispatch({
      type: actionTypes.EDIT_SITE_SETTINGS_REQUESTED
    });
    await api
      .editSiteSettings(form)
      .then(() => {
        dispatch({ type: actionTypes.EDIT_SITE_SETTINGS_SUCCESS });
      })
      .catch(() => dispatch({ type: actionTypes.EDIT_SITE_SETTINGS_FAILURE }));
  };
};

export const getCurrentUser = () => {
  return async dispatch => {
    dispatch({
      type: actionTypes.FETCH_CURRENT_USER_REQUESTED
    });
    api
      .getCurrentUser()
      .then(response =>
        dispatch({
          type: actionTypes.FETCH_CURRENT_USER_SUCCESS,
          payload: response.data
        })
      )
      .catch(() =>
        dispatch({
          type: actionTypes.FETCH_CURRENT_USER_FAILURE
        })
      );
  };
};

export const dispatchCrisis = (id, phoneNumberToNotify) => {
  return async dispatch => {
    dispatch({
      type: actionTypes.DISPATCH_CRISIS_REQUESTED
    });
    await api
      .dispatchCrisis(id, phoneNumberToNotify)
      .then(() =>
        dispatch({
          type: actionTypes.DISPATCH_CRISIS_SUCCESS
        })
      )
      .catch(() =>
        dispatch({
          type: actionTypes.DISPATCH_CRISIS_FAILURE
        })
      );
  };
};

export const showModal = (modalType, modalProps) => {
  return {
    type: actionTypes.MODAL_SHOW,
    payload: {
      modalType,
      modalProps
    }
  };
};

export const hideModal = () => {
  return {
    type: actionTypes.MODAL_HIDE
  };
};
