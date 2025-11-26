import React from "react";
import PropTypes from "prop-types";
import { connect } from "react-redux";
import { startRealTimeConditionTracking } from "@redux/actions";

class RealTimeCrisisTracker extends React.Component {
  componentDidMount = () => this.props.startRealTimeConditionTracking(600000); // 10 min
  render() {
    return this.props.children;
  }
}

RealTimeCrisisTracker.propTypes = {
  startRealTimeConditionTracking: PropTypes.func.isRequired,
  children: PropTypes.object.isRequired
};

const mapDispatchToProps = dispatch => ({
  startRealTimeConditionTracking: time =>
    dispatch(startRealTimeConditionTracking(time))
});

export default connect(
  null,
  mapDispatchToProps
)(RealTimeCrisisTracker);
