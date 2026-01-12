import React from "react";
import PropTypes from "prop-types";
import { connect } from "react-redux";
import InfoCard from "@components/InfoCard"

const RealTimePSI = props => {
  const { psi } = props;
  const status = psi && psi.status;
  const hourly = psi && psi.hourly;
  const { national, west, east, central, south, north } = hourly || {};
  return (
    <InfoCard>
      <div>
        <strong>Pollution Overview</strong>
      </div>
      <div>
        Current Status:{" "}
        <span style={{ color: "crimson" }}>
          <strong>{status}</strong>
        </span>
      </div>
      <div>
        <strong>Max PSI of Past Hour</strong>
      </div>
      <div>
        National: <strong>{national}</strong>
      </div>
      <div>
        East: <strong>{east}</strong>
      </div>
      <div>
        South: <strong>{south}</strong>
      </div>
      <div>
        West: <strong>{west}</strong>
      </div>
      <div>
        North: <strong>{north}</strong>
      </div>
      <div>
        Central: <strong>{central}</strong>
      </div>
    </InfoCard>
  );
};

RealTimePSI.propTypes = {
  psi: PropTypes.object
};

const mapStateToProps = state => {
  const { common } = state;
  return {
    psi: common && common.psi
  };
};

export default connect(mapStateToProps)(RealTimePSI);
