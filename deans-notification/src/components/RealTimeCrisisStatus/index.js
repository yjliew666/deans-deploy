import React from "react";
import { connect } from "react-redux";
import PropTypes from "prop-types";
import { Icon } from "antd";
import * as styles from "./style.scss";

const RealTimeCrisisStatus = props => {
  const { crises } = props || [];
  const num =
    crises && crises.filter(crisis => crisis.crisis_status === "DP").length;
  return (
    <div className={styles.container}>
      <div>
        <strong>Crisis Overview</strong>
      </div>
      <div>
        Active crisis: <strong>{num}</strong>
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
};

RealTimeCrisisStatus.propTypes = {
  crises: PropTypes.array
};

const mapStateToProps = state => {
  const { common } = state;
  return {
    crises: common && common.crises
  };
};

export default connect(mapStateToProps)(RealTimeCrisisStatus);
