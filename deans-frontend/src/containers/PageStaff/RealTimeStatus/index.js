import React from "react";
import PropTypes from "prop-types";
import { Icon } from "antd";
import InfoCard from "@components/InfoCard";
import * as styles from "./style.scss";

const RealTimeStatus = props => (
  <InfoCard>
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
    <div>
      Internet Status:
      <Icon
        type="check-circle"
        theme="twoTone"
        twoToneColor="#52c41a"
        className={styles.internet}
      />
      Online
    </div>
  </InfoCard>
);

RealTimeStatus.propTypes = {
  numOfPending: PropTypes.number.isRequired,
  numOfDispatched: PropTypes.number.isRequired
};

export default RealTimeStatus;
