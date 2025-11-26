import React from "react";
import PropTypes from "prop-types";
import NavBar from "@components/NavBar";
import Footer from "@components/Footer";
import CrisisReportForm from "./CrisisReportForm";
import { connect } from "react-redux";
import { getCrises, fetchTypes, reportCrises } from "@redux/actions";

import * as styles from "./style.scss";

class PageReport extends React.Component {
  state = {
    completed: false
  };

  componentDidMount() {
    this.props.fetchTypes();
    this.fetchData();
  }

  setComplete = () => {
    this.setState({ completed: true });
  };

  fetchData = () => {
    this.props.getCrises();
  };

  render() {
    const { completed } = this.state;
    return (
      <React.Fragment>
        <NavBar />
        <div className={styles.container}>
          <div className={styles.header}>Report Crisis</div>
          {completed ? (
            <div style={{ marginTop: "2rem" }}>
              Thank you for reporting the crisis!
            </div>
          ) : (
            <React.Fragment>
              <div style={{ marginTop: "2rem" }}>
                If you prefer to report over the phone, please call us directly
                at <strong>12345678</strong>.
              </div>
              <div className={styles.form}>
                <CrisisReportForm
                  crisisType={this.props.crisisType || []}
                  assistanceType={this.props.assistanceType || []}
                  reportCrises={this.props.reportCrises}
                  setComplete={this.setComplete}
                  flag={this.props.flag}
                />
              </div>
            </React.Fragment>
          )}
        </div>
        <Footer />
      </React.Fragment>
    );
  }
}

PageReport.propTypes = {
  crisisType: PropTypes.array.isRequired,
  assistanceType: PropTypes.array.isRequired,
  crises: PropTypes.array.isRequired,
  fetchTypes: PropTypes.func.isRequired,
  getCrises: PropTypes.func.isRequired,
  reportCrises: PropTypes.func.isRequired,
  flag: PropTypes.bool.isRequired
};

const mapStateToProps = state => {
  const { system, common } = state;
  return {
    flag: common && common.flag,
    crisisType: system && system.crisisType,
    assistanceType: system && system.assistanceType,
    crises: common && common.crises
  };
};

const mapDispatchToProps = dispatch => ({
  fetchTypes: () => dispatch(fetchTypes()),
  getCrises: () => dispatch(getCrises()),
  reportCrises: form => dispatch(reportCrises(form))
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(PageReport);
