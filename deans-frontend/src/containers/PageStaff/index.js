import React from "react";
import { Route, Switch } from "react-router-dom";
import { connect } from "react-redux";
import PropTypes from "prop-types";
import * as ROUTES from "src/routes";
import NavBar from "@components/NavBar";
import Footer from "@components/Footer";
import RealTimePSI from "@components/RealTimePSI";
import RealTimeWeather from "@components/RealTimeWeather";
import Menu from "./Menu";
import RealTimeStatus from "./RealTimeStatus";
import PageCallCenter from "./PageCallCenter";
import PageUserCenter from "./PageUserCenter";
import PageSetting from "./PageSetting";
import { fetchTypes, getCrises } from "@redux/actions";

import * as styles from "./style.scss";

class PageStaff extends React.Component {
  componentDidMount() {
    this.props.fetchTypes();
    this.props.getCrises();
  }

  render() {
    const { crises } = this.props;
    const numOfPending =
      crises && crises.filter(crisis => crisis.crisis_status === "PD").length;
    const numOfDispatched =
      crises && crises.filter(crisis => crisis.crisis_status === "DP").length;
    return (
      <React.Fragment>
        <NavBar />
        <div className={styles.container}>
          <div className={styles.left}>
            <Menu isAdmin={this.props.isAdmin} />
            <RealTimePSI />
            <RealTimeWeather />
            <RealTimeStatus
              numOfPending={numOfPending || 0}
              numOfDispatched={numOfDispatched || 0}
            />
          </div>
          <div className={styles.right}>
            <Switch>
              <Route
                exact
                path={ROUTES.ROUTE_DASHBOARD}
                component={PageCallCenter}
              />
              <Route
                exact
                path={ROUTES.ROUTE_USER_CENTER}
                component={PageUserCenter}
              />
              <Route
                exact
                path={ROUTES.ROUTE_SETTING}
                component={PageSetting}
              />
              {/* fallback */}
              <Route path={ROUTES.ROUTE_STAFF} component={PageCallCenter} />
            </Switch>
          </div>
        </div>
        <Footer />
      </React.Fragment>
    );
  }
}

PageStaff.propTypes = {
  crises: PropTypes.array,
  fetchTypes: PropTypes.func.isRequired,
  getCrises: PropTypes.func.isRequired,
  crisisType: PropTypes.object,
  isAdmin: PropTypes.bool.isRequired,
  assistanceType: PropTypes.object
};

const mapStateToProps = state => {
  const { staff, system, common } = state;
  return {
    isAdmin: staff && staff.isAdmin,
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
)(PageStaff);
