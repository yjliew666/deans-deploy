import React from "react";
import { connect } from "react-redux";
import { userLogin } from "@redux/actions";
import PropTypes from "prop-types";
import { Redirect } from "react-router-dom";
import LoginForm from "./LoginForm";
import NavBar from "@components/NavBar";
import Footer from "@components/Footer";
import * as styles from "./style.scss";

// eslint-ignore-next-line
class PageLogin extends React.Component {
  state = {
    redirect: false
  };

  setRedirect = () => {
    this.setState({ redirect: true });
  };

  render() {
    if (this.state.redirect) return <Redirect to="/staff/dashboard" />;
    return (
      <React.Fragment>
        <NavBar />
        <div className={styles.container}>
          <div className={styles.innerContainer}>
            <div className={styles.header}>Staff Login</div>
            <div className={styles.form}>
              <LoginForm
                setRedirect={this.setRedirect}
                userLogin={this.props.userLogin}
                flag={this.props.flag}
              />
            </div>
          </div>
        </div>
        <Footer />
      </React.Fragment>
    );
  }
}

PageLogin.propTypes = {
  flag: PropTypes.bool.isRequired,
  userLogin: PropTypes.func.isRequired
};

export default connect(
  state => {
    const { staff } = state;
    return {
      flag: staff.flag || false
    };
  },
  dispatch => ({
    userLogin: form => dispatch(userLogin(form))
  })
)(PageLogin);
