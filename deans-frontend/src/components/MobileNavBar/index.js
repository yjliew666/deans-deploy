import React from "react";
import PropTypes from "prop-types";
import { Drawer, Button, Menu, Icon, message } from "antd";
import { Link } from "react-router-dom";
import { connect } from "react-redux";
import { getCurrentUser, userLogout } from "../../redux/actions";
import * as styles from "./style.scss";

class MobileNav extends React.Component {
  state = { visible: false };

  componentDidMount() {
    this.props.getCurrentUser();
  }

  show = () => this.setState({ visible: true });
  close = () => this.setState({ visible: false });

  handleLogout = () => {
    this.props
      .userLogout()
      .then(() => {
        message.success("Logged out");
        window.location.assign("/");
      })
      .catch(() => {
        message.error("Logout failed");
      });
  };

  onMenuClick = ({ key }) => {
    if (key === "logout") {
      this.handleLogout();
      return;
    }
    this.close();
  };

  render() {
    const { currentUser } = this.props;
    return (
      <div className={styles.container}>
        <Button className={styles.nav} type="primary" onClick={this.show}>
          <Icon type="menu" />
        </Button>

        <Drawer
          title="Menu"
          placement="left"
          onClose={this.close}
          visible={this.state.visible}
        >
          <Menu mode="inline" onClick={this.onMenuClick} selectable={false}>
            <Menu.Item key="home">
              <Link to="/">Home</Link>
            </Menu.Item>
            <Menu.Item key="report">
              <Link to="/report">Report</Link>
            </Menu.Item>

            {currentUser ? (
              <Menu.Item key="dashboard">
                <Link to="/staff/dashboard">{currentUser}</Link>
              </Menu.Item>
            ) : (
              <Menu.Item key="login">
                <Link to="/login">Login</Link>
              </Menu.Item>
            )}

            {currentUser && <Menu.Item key="logout">Logout</Menu.Item>}
          </Menu>
        </Drawer>
      </div>
    );
  }
}

MobileNav.propTypes = {
  currentUser: PropTypes.string,
  getCurrentUser: PropTypes.func.isRequired,
  userLogout: PropTypes.func.isRequired
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
)(MobileNav);