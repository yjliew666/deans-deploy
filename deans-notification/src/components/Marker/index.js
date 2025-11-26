import React from "react";
import PropTypes from "prop-types";
import { Popover } from "antd";
import pin from "@assets/pin.png";

import * as styles from "./style.scss";

const Marker = props => {
  const { crisisType, location } = props;
  return (
    <div lat={props.lat} lng={props.lng}>
      <Popover
        placement="top"
        title={props.type.map(type => crisisType[type]).join(", ")}
        content={location.replace(/"/g, "")}
      >
        {/* <Icon className={styles.container} type="warning" theme="filled" /> */}
        <img className={styles.container} src={pin} width="35" />
      </Popover>
    </div>
  );
};

Marker.propTypes = {
  lat: PropTypes.number.isRequired,
  lng: PropTypes.number.isRequired,
  location: PropTypes.string.isRequired,
  crisisType: PropTypes.array,
  type: PropTypes.array.isRequired,
  description: PropTypes.string
};

export default Marker;
