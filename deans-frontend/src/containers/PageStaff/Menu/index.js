import React from "react";
import PropTypes from "prop-types";
import { NavLink } from "react-router-dom";
import * as styles from "./style.scss";

const Menu = props => (
  <div className={styles.container}>
    <NavLink 
      to="/staff/dashboard"
      className={styles.item} 
      activeClassName={styles.activeItem}
    >
      Dashboard
    </NavLink>
    {props.isAdmin && (
      <React.Fragment>
        <NavLink
          to="/staff/user-center"
          className={styles.item}
          activeClassName={styles.activeItem}
        >
          User Center
        </NavLink>
        <NavLink
          to="/staff/setting"
          className={styles.item}
          activeClassName={styles.activeItem}
        >
          Setting
        </NavLink>
      </React.Fragment>
    )}
  </div>
);

Menu.propTypes = {
  isAdmin: PropTypes.bool.isRequired
};

export default Menu;
