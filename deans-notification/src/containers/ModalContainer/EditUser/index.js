import React from "react";
import PropTypes from "prop-types";
import Modal from "antd/lib/modal";
import { Form, Input, Icon, Button, message } from "antd";
import * as styles from "./style.scss";

const FormItem = Form.Item;

class _EditUserForm extends React.Component {
  handleSubmit = e => {
    e.preventDefault();
    this.props.form.validateFields((err, values) => {
      if (!err) {
        const { password } = values;
        const { userId } = this.props;
        const form = new FormData();
        form.append("password", password);
        this.props
          .editUser(userId, form)
          .then(() => {
            message.success("Success!");
            this.props.hideModal();
          })
          .catch(() => null);
      }
    });
  };

  render() {
    const { getFieldDecorator } = this.props.form;
    return (
      <Form onSubmit={this.handleSubmit}>
        <FormItem>
          {getFieldDecorator("password", {
            rules: [{ required: true, message: "Please input password!" }]
          })(
            <Input
              prefix={<Icon type="lock" style={{ color: "rgba(0,0,0,.25)" }} />}
              type="password"
              placeholder="New Password"
            />
          )}
        </FormItem>
        <FormItem>
          <Button
            type="primary"
            htmlType="submit"
            className={styles.createButton}
          >
            Confirm
          </Button>
        </FormItem>
      </Form>
    );
  }
}

_EditUserForm.propTypes = {
  form: PropTypes.object.isRequired,
  editUser: PropTypes.func.isRequired,
  userId: PropTypes.number.isRequired,
  hideModal: PropTypes.func.isRequired
};

const EditUser = props => {
  const EditUserForm = Form.create()(_EditUserForm);
  const { editUser, userId, hideModal } = props;
  return (
    <Modal
      centered
      title="CHANGE PASSWORD"
      visible
      onCancel={props.hideModal}
      footer={null}
    >
      <EditUserForm editUser={editUser} userId={userId} hideModal={hideModal} />
    </Modal>
  );
};

EditUser.propTypes = {
  hideModal: PropTypes.func.isRequired,
  editUser: PropTypes.func.isRequired,
  userId: PropTypes.number.isRequired
};

export default EditUser;
