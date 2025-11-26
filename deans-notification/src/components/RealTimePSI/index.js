import React from "react";
import PropTypes from "prop-types";
import { connect } from "react-redux";
// import { Icon } from "antd";
import * as styles from "./style.scss";

const RealTimePSI = props => {
  const { psi } = props;
  const status = psi && psi.status;
  const hourly = psi && psi.hourly;
  const { national, west, east, central, south, north } = hourly || {};
  return (
    <div className={styles.container}>
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
      {/* <div className={styles.internet}>
        Internet Status:
        <Icon
          type="check-circle"
          theme="twoTone"
          twoToneColor="#52c41a"
          style={{ marginLeft: "0.5rem" }}
        />{" "}
        Online
      </div> */}
    </div>
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
