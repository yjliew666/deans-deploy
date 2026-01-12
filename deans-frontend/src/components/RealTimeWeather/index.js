import React from "react";
import PropTypes from "prop-types";
import { connect } from "react-redux";
import InfoCard from "@components/InfoCard"

const RealTimeWeather = props => {
  const { temperature, humidity, rainfall } = props;
  return (
    <InfoCard>
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
    </InfoCard>
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
