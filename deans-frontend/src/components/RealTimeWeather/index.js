import React from "react";
import PropTypes from "prop-types";
import { connect } from "react-redux";
// import { Icon } from "antd";
import * as styles from "./style.scss";

const RealTimeWeather = props => {
  const { temperature, humidity, rainfall } = props;
  return (
    <div className={styles.container}>
      <div>
        <strong>Weather Overview</strong>
      </div>
      <div>
        Temperature: <strong>{temperature + "°C"}</strong>
      </div>
      <div>
        Humidity: <strong>{humidity + "%"}</strong>
      </div>
      <div>
        Rainfall: <strong>{rainfall + "mm"}</strong>
      </div>
    </div>
  );
};

RealTimeWeather.propTypes = {
  temperature: PropTypes.number,
  humidity: PropTypes.number,
  rainfall: PropTypes.number
};

const mapStateToProps = state => {
  const { common } = state;
  return {
    temperature: common && common.temperature,
    humidity: common && common.humidity,
    rainfall: common && common.rainfall
  };
};

export default connect(mapStateToProps)(RealTimeWeather);
