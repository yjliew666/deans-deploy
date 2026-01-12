import React from "react";
import { connect } from "react-redux";
import PropTypes from "prop-types";
import { Icon } from "antd";
import InfoCard from "@components/InfoCard"
import * as styles from "./style.scss";

const RealTimeCrisisStatus = props => {
  const { crises } = props || [];
  const num =
    crises && crises.filter(crisis => crisis.crisis_status === "DP").length;
  return (
    <InfoCard>
      <div>
        <strong>Crisis Overview</strong>
      </div>
      <div>
        Active crisis: <strong>{num}</strong>
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
