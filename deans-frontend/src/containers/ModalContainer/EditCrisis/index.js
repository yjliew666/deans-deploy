import React from "react";
import PropTypes from "prop-types";
import Modal from "antd/lib/modal";
import CrisisEditForm from "./CrisisEditForm";

const EditCrisis = props => {
  return (
    <Modal
      centered
      title="EDIT CRISIS"
      visible
      onCancel={props.hideModal}
      footer={null}
    >
      <CrisisEditForm />
    </Modal>
  );
};

EditCrisis.propTypes = {
  hideModal: PropTypes.func.isRequired
};

export default EditCrisis;
