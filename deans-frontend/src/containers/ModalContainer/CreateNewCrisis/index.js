import React from "react";
import PropTypes from "prop-types";
import Modal from "antd/lib/modal";
import CrisisReportForm from "./CrisisReportForm";

const CreateNewCrisis = props => {
  return (
    <Modal
      centered
      title="CREATE NEW CRISIS"
      visible
      onCancel={props.hideModal}
      footer={null}
    >
      <CrisisReportForm {...props} />
    </Modal>
  );
};

CreateNewCrisis.propTypes = {
  hideModal: PropTypes.func.isRequired,
  crisisType: PropTypes.object.isRequired,
  assistanceType: PropTypes.object.isRequired,
  reportCrises: PropTypes.func.isRequired,
  getCrises: PropTypes.func.isRequired
};

export default CreateNewCrisis;
