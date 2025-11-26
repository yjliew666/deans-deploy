import React from "react";
import { connect } from "react-redux";
import PropTypes from "prop-types";

import {
  addCrisisType,
  addAssistanceType,
  fetchTypes,
  getEmergencyAgencies,
  addEmergencyAgencies,
  editSiteSettings,
  editEmergencyAgencies,
  showModal
} from "@redux/actions";
import { Button, Tag, message } from "antd";
import EmergencyAgenciesTable from "./EmergencyAgenciesTable";
import * as styles from "./style.scss";

class PageSetting extends React.Component {
  state = {
    reportingEmail: {
      edited: false,
      content: null
    }
  };

  componentDidMount() {
    this.props.fetchTypes();
    this.props.getEmergencyAgencies();
  }

  componentDidUpdate = prevProps => {
    if (prevProps.crisisType !== this.props.crisisType) this.createCrisisTags();
  };

  createCrisisTags = () => {
    const { crisisType } = this.props;
    if (!crisisType) return [];
    return Object.keys(crisisType).map((val, index) => (
      <Tag color="purple" key={index}>
        {crisisType[val]}
      </Tag>
    ));
  };

  createAssistanceTags = () => {
    const { assistanceType } = this.props;
    if (!assistanceType) return [];
    return Object.keys(assistanceType).map((val, index) => (
      <Tag color="geekblue" key={index}>
        {assistanceType[val]}
      </Tag>
    ));
  };

  handleEmailChange = e => {
    this.setState({
      ...this.state,
      reportingEmail: {
        edited: true,
        content: e.target.value
      }
    });
  };

  editSiteSettings = () => {
    const email = this.state.reportingEmail.content;
    if (!email.match(/.+@.+\..+/g)) {
      console.log(email);
      message.error("Email is invalid");
    } else {
      const form = new FormData();
      form.append("summary_reporting_email", email);
      this.props.editSiteSettings(form).then(() => {
        message.success("Success!");
        this.setState({ edited: false });
      });
    }
  };

  addCrisisType = name => {
    // const name = prompt("Enter the name of new crisis");
    const form = new FormData();
    form.append("name", name);
    this.props
      .addCrisisType(form)
      .then(() => {
        message.success("Success!");
        this.props.fetchTypes();
      })
      .catch(() => message.error("Error!"));
  };

  addAssistanceType = name => {
    // const name = prompt("Enter the name of new crisis");
    const form = new FormData();
    form.append("name", name);
    this.props
      .addAssistanceType(form)
      .then(() => {
        message.success("Success!");
        this.props.fetchTypes();
      })
      .catch(() => message.error("Error!"));
  };

  addEmergencyAgencies = (agency, phoneNumber) => {
    const form = new FormData();
    form.append("agency", agency);
    form.append("phone_number", phoneNumber);
    this.props
      .addEmergencyAgencies(form)
      .then(() => {
        message.success("Success!");
        this.props.getEmergencyAgencies();
      })
      .catch(() => message.error("Error!"));
  };

  editEmergencyAgencies = (id, phoneNumber) => {
    const form = new FormData();
    form.append("agency_id", id);
    form.append("phone_number", phoneNumber);
    this.props
      .editEmergencyAgencies(id, form)
      .then(() => {
        message.success("Success!");
        this.props.getEmergencyAgencies();
      })
      .catch(() => message.error("Error!"));
  };

  render() {
    return (
      <div>
        <h1>Setting</h1>
        <div className={styles.subHeader}>
          <div>Crisis Type</div>
          <Button
            onClick={() =>
              this.props.showModal("SINGLE_INPUT", {
                title: "ADD CRISIS TYPE",
                handler: this.addCrisisType
              })
            }
          >
            Add
          </Button>
        </div>
        <div className={styles.tagContainer}>{this.createCrisisTags()}</div>
        <div className={styles.subHeader}>
          <div>Assistance Type</div>
          <Button
            onClick={() =>
              this.props.showModal("SINGLE_INPUT", {
                title: "ADD ASSISTANCE TYPE",
                handler: this.addAssistanceType
              })
            }
          >
            Add
          </Button>
        </div>
        <div className={styles.tagContainer}>{this.createAssistanceTags()}</div>
        <div className={styles.subHeader}>
          <div>Emergency Agencies</div>
          <Button
            onClick={() =>
              this.props.showModal("DOUBLE_INPUT", {
                title: "ADD EMERGENCY AGENCIES",
                handler: this.addEmergencyAgencies,
                labelA: "Agency Name",
                labelB: "Phone Number"
              })
            }
          >
            Add
          </Button>
        </div>
        <div className={styles.emergencyAgenciesContainer}>
          <EmergencyAgenciesTable
            showModal={this.props.showModal}
            emergencyAgencies={this.props.emergencyAgencies || []}
            editPhoneNumber={this.editEmergencyAgencies}
          />
        </div>
        {/* <div className={styles.subHeader}>
          <div>Summary Reporting Email</div>
          <Button
            type="primary"
            disabled={!this.state.reportingEmail.edited}
            onClick={this.editSiteSettings}
          >
            Save
          </Button>
        </div>
        <div className={styles.summaryReportingEmailContainer}>
          <Input
            defaultValue="prime-minister@gmail.com"
            onChange={this.handleEmailChange}
          />
        </div> */}
      </div>
    );
  }
}

const mapStateToProps = state => {
  const { system } = state;
  return {
    crisisType: system && system.crisisType,
    assistanceType: system && system.assistanceType,
    emergencyAgencies: system && system.emergencyAgencies
  };
};

PageSetting.propTypes = {
  addCrisisType: PropTypes.func.isRequired,
  addAssistanceType: PropTypes.func.isRequired,
  fetchTypes: PropTypes.func.isRequired,
  crisisType: PropTypes.object,
  assistanceType: PropTypes.object,
  getEmergencyAgencies: PropTypes.func.isRequired,
  addEmergencyAgencies: PropTypes.func.isRequired,
  editEmergencyAgencies: PropTypes.func.isRequired,
  emergencyAgencies: PropTypes.array,
  editSiteSettings: PropTypes.func.isRequired,
  showModal: PropTypes.func.isRequired
};

const mapDispatchToProps = dispatch => ({
  addCrisisType: form => dispatch(addCrisisType(form)),
  addAssistanceType: form => dispatch(addAssistanceType(form)),
  fetchTypes: () => dispatch(fetchTypes()),
  getEmergencyAgencies: () => dispatch(getEmergencyAgencies()),
  addEmergencyAgencies: form => dispatch(addEmergencyAgencies(form)),
  editEmergencyAgencies: (id, form) =>
    dispatch(editEmergencyAgencies(id, form)),
  editSiteSettings: form => dispatch(editSiteSettings(form)),
  showModal: (modalType, modalProps) =>
    dispatch(showModal(modalType, modalProps))
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(PageSetting);
