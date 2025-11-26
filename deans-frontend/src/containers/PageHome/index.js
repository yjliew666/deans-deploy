import React from "react";
import PropTypes from "prop-types";
import { connect } from "react-redux";
import { getCrises, fetchTypes } from "@redux/actions";
import GMap from "@components/GMap";
import NavBar from "@components/NavBar";
import Footer from "@components/Footer";
import RealTimePSI from "@components/RealTimePSI";
import RealTimeWeather from "@components/RealTimeWeather";
import RealTimeCrisisStatus from "@components/RealTimeCrisisStatus";
import ActiveCrisisListTable from "./ActiveCrisisListTable";

import * as styles from "./style.scss";

class PageHome extends React.Component {
  componentDidMount() {
    this.props.fetchTypes();
    this.fetchData();
  }

  fetchData = () => {
    this.props.getCrises();
  };

  filterCrises = crises => {
    // display only dispatched crises
    return crises.filter(crisis => crisis.crisis_status === "DP");
  };

  render() {
    return (
      <React.Fragment>
        <NavBar />
        <div className={styles.container}>
          <div className={styles.left}>
            <div className={styles.status}>
              <RealTimePSI />
            </div>
            <div className={styles.status}>
              <RealTimeWeather />
            </div>
            <div className={styles.status}>
              <RealTimeCrisisStatus />
            </div>
          </div>
          <div className={styles.right}>
            <div className={styles.map}>
              <GMap crises={this.filterCrises(this.props.crises || [])} />
            </div>
            <div className={styles.activeCrisisListTableContainer}>
              <div className={styles.subHeader}>Active Crisis</div>
              <div className={styles.activeCrisisListTable}>
                <ActiveCrisisListTable
                  crises={this.filterCrises(this.props.crises || [])}
                />
              </div>
            </div>
          </div>
        </div>
        <Footer />
      </React.Fragment>
    );
  }
}

PageHome.propTypes = {
  crises: PropTypes.array,
  fetchTypes: PropTypes.func.isRequired,
  getCrises: PropTypes.func.isRequired
};

const mapStateToProps = state => {
  const { system, common } = state;
  return {
    crisisType: system && system.crisisType,
    assistanceType: system && system.assistanceType,
    crises: common && common.crises
  };
};

const mapDispatchToProps = dispatch => ({
  fetchTypes: () => dispatch(fetchTypes()),
  getCrises: () => dispatch(getCrises())
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(PageHome);
