import React from "react";
import { connect } from "react-redux";
import { dispatchCrisis } from "@redux/actions";
import PropTypes from "prop-types";
import Modal from "antd/lib/modal";
import CrisisDispatchForm from "./CrisisDispatchForm";
import * as styles from "./style.scss";

const DispatchCrisis = props => {
  const {
    your_name,
    mobile_number,
    crisis_id,
    crisis_location1,
    crisis_location2,
    crisis_time,
    crisis_type,
    crisis_description,
    crisis_assistance,
    crisis_assistance_description
  } = props.crisis;
  return (
    <Modal
      centered
      title="DISPATCH CRISIS"
      visible
      onCancel={props.hideModal}
      footer={null}
    >
      <div className={styles.summary}>
        <div className={styles.summaryHeader}>SUMMARY</div>
        <div className={styles.summaryHint}>
          The following information will be submitted to emergency agencies.
        </div>
        <div className={styles.summaryContainer}>
          <div className={styles.label}>Reported Time:</div>
          <div className={styles.value}>
            {(() => {
              const date = new Date(crisis_time);
              return date.toLocaleString("en", {
                year: "numeric",
                month: "short",
                day: "numeric",
                hour: "numeric",
                minute: "numeric"
              });
            })()}
          </div>
          <div className={styles.label}>Reporter Name:</div>
          <div className={styles.value}>{your_name}</div>
          <div className={styles.label}>Mobile Number:</div>
          <div className={styles.value}>+65 {mobile_number}</div>
          <div className={styles.label}>Location:</div>
          <div className={styles.value}>
            {crisis_location1.replace(/"/g, "")}
          </div>
          <div className={styles.label}>Location 2:</div>
          <div className={styles.value}>{crisis_location2}</div>
          <div className={styles.label}>Crisis Type:</div>
          <div className={styles.value}>
            {crisis_type.map(val => props.crisisType[val]).join(", ")}
          </div>
          <div className={styles.label}>Crisis Description:</div>
          <div className={styles.value}>{crisis_description}</div>
          <div className={styles.label}>Assistance Type:</div>
          <div className={styles.value}>
            {crisis_assistance.map(val => props.assistanceType[val]).join(", ")}
          </div>
          <div className={styles.label}>Assistance Description:</div>
          <div className={styles.value}>{crisis_assistance_description}</div>
        </div>
      </div>
      <div className={styles.crisisDispatchForm}>
        <CrisisDispatchForm
          crisisId={crisis_id}
          emergencyAgencies={props.emergencyAgencies}
          dispatchCrisis={props.dispatchCrisis}
          hideModal={props.hideModal}
        />
      </div>
    </Modal>
  );
};

DispatchCrisis.propTypes = {
  hideModal: PropTypes.func.isRequired,
  dispatchCrisis: PropTypes.func.isRequired,
  crisis: PropTypes.object,
  crisisType: PropTypes.object,
  assistanceType: PropTypes.object,
  emergencyAgencies: PropTypes.array
};

const mapStateToProps = state => {
  const { system } = state;
  return {
    crisisType: system && system.crisisType,
    assistanceType: system && system.assistanceType,
    emergencyAgencies: system && system.emergencyAgencies
  };
};

const mapDispatchToProps = dispatch => ({
  dispatchCrisis: (id, phoneNumberToNotify) =>
    dispatch(dispatchCrisis(id, phoneNumberToNotify))
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(DispatchCrisis);
