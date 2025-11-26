import React from "react";
import PropTypes from "prop-types";
import { Icon } from "antd";
import * as styles from "./style.scss";

const RealTimeStatus = props => (
  <div className={styles.container}>
    <div>
      <strong>Crisis Overview</strong>
    </div>
    <div>
      <span style={{ color: "crimson" }}>
        <strong>{props.numOfPending}</strong>
      </span>{" "}
      Pending
    </div>
    <div>
      <strong>{props.numOfDispatched}</strong> Dispatched
    </div>
    <div className={styles.internet}>
      Internet Status:
      <Icon
        type="check-circle"
        theme="twoTone"
        twoToneColor="#52c41a"
        style={{ marginLeft: "0.5rem" }}
      />{" "}
      Online
    </div>
  </div>
);

RealTimeStatus.propTypes = {
  numOfPending: PropTypes.number.isRequired,
  numOfDispatched: PropTypes.number.isRequired
};

export default RealTimeStatus;
