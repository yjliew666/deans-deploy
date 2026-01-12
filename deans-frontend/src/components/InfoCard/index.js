import React from "react";
import PropTypes from "prop-types";
import * as styles from "./style.scss"

const InfoCard = ({ children }) => {
  return (
    <div className={styles.card}>
      {children}
    </div>
  );
};

InfoCard.propTypes = {
  children: PropTypes.node.isRequired,
};

export default InfoCard;