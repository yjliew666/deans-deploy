import React from "react";
import PropTypes from "prop-types";
import { connect } from "react-redux";
import { startRealTimeCrisisTracking } from "@redux/actions";

class RealTimeCrisisTracker extends React.Component {
  componentDidMount = () => this.props.startRealTimeCrisisTracking(); // 10 min
  render() {
    return this.props.children;
  }
}

RealTimeCrisisTracker.propTypes = {
  startRealTimeCrisisTracking: PropTypes.func.isRequired,
  children: PropTypes.object.isRequired
};

const mapDispatchToProps = dispatch => ({
  startRealTimeCrisisTracking: () => dispatch(startRealTimeCrisisTracking())
});

export default connect(
  null,
  mapDispatchToProps
)(RealTimeCrisisTracker);
