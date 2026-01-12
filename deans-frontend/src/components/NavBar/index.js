import React from "react";
import { Popover, Button, message } from "antd";
import PropTypes from "prop-types";
import { connect } from "react-redux";
import { getCurrentUser, userLogout } from "@redux/actions";
import { Link } from "react-router-dom";
import logo from "@assets/logo.png";
import MobileNav from "../MobileNavBar";

import * as styles from "./style.scss";

class NavBar extends React.Component {
  componentDidMount() {
    this.props.getCurrentUser();
  }

  render() {
    const { currentUser } = this.props;
    return (
      <div className={styles.container}>
        <MobileNav />
        <div className={styles.left}>
          <div className={styles.item}>
            <Link to="/">
              <img src={logo} className={styles.logo} />
            </Link>
          </div>
          <div className={styles.item + " " + styles.brand}>
            <Link to="/">Dean&#39;s Crisis Management System</Link>
          </div>
          <div className={styles.item}>
            <Link to="/">Home</Link>
          </div>
          <div className={styles.item}>
            <Link to="/report">Report</Link>
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
                <Link to="/staff/dashboard">{currentUser}</Link>
              </Popover>
            ) : (
              <Link to="/login">Login</Link>
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
