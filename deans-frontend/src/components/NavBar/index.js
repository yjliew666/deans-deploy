import React from "react";
import { Popover, Button, message } from "antd";
import PropTypes from "prop-types";
import { connect } from "react-redux";
import { getCurrentUser, userLogout } from "@redux/actions";
import { NavLink } from "react-router-dom";
import logo from "@assets/logo.png";

import * as styles from "./style.scss";

class NavBar extends React.Component {
  componentDidMount() {
    this.props.getCurrentUser();
  }

  render() {
    const { currentUser } = this.props;
    return (
      <div className={styles.container}>
        <div className={styles.left}>
          <div className={styles.item}>
            <NavLink exact to="/">
              <img src={logo} className={styles.logo} />
            </NavLink>
          </div>
          <div className={styles.item + " " + styles.brand}>
            <NavLink exact to="/">Dean&#39;s Crisis Management System</NavLink>
          </div>
          <div className={styles.item}>
            <NavLink exact to="/" activeClassName={styles.active}>Home</NavLink>
          </div>
          <div className={styles.item}>
            <NavLink to="/report" activeClassName={styles.active}>Report</NavLink>
          </div>
        </div>
        <div className={styles.right}>
          <div className={styles.item}>
            {currentUser ? (
              <Popover
                placement="bottom"
                content={
                  <Button
                    onClick={() => {
                      this.props.userLogout().then(() => {
                        message.success("You are logged out");
                        location.assign("/");
                      });
                    }}
                  >
                    Logout
                  </Button>
                }
              >
                <NavLink to="/staff/dashboard" activeClassName={styles.active}>{currentUser}</NavLink>
              </Popover>
            ) : (
              <NavLink to="/login" activeClassName={styles.active}>Login</NavLink>
            )}
          </div>
        </div>
      </div>
    );
  }
}

NavBar.propTypes = {
  getCurrentUser: PropTypes.func.isRequired,
  userLogout: PropTypes.func.isRequired,
  currentUser: PropTypes.string
};

const mapStateToProps = state => {
  const { staff } = state;
  return {
    currentUser: staff && staff.currentUser
  };
};

const mapDispatchToProps = dispatch => ({
  getCurrentUser: () => dispatch(getCurrentUser()),
  userLogout: () => dispatch(userLogout())
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(NavBar);
