import React from "react";
import { connect } from "react-redux";
import { addUser } from "@redux/actions";
import PropTypes from "prop-types";
import Modal from "antd/lib/modal";
import { Form, Input, Icon, Checkbox, Button, message } from "antd";
import * as styles from "./style.scss";

const FormItem = Form.Item;

class _AddUserForm extends React.Component {
  handleSubmit = e => {
    e.preventDefault();
    this.props.form.validateFields((err, values) => {
      if (!err) {
        const { username, password, isAdmin } = values;
        const form = new FormData();
        form.append("username", username);
        form.append("password", password);
        form.append("is_staff", isAdmin);
        this.props.addUser(form).then(() => {
          message.success("A new user has been created!");
          location.reload();
        });
      }
    });
  };

  render() {
    const { getFieldDecorator } = this.props.form;
    return (
      <Form onSubmit={this.handleSubmit}>
        <FormItem>
          {getFieldDecorator("username", {
            rules: [{ required: true, message: "Please input username!" }]
          })(
            <Input
              prefix={<Icon type="user" style={{ color: "rgba(0,0,0,.25)" }} />}
              placeholder="Username"
            />
          )}
        </FormItem>
        <FormItem>
          {getFieldDecorator("password", {
            rules: [{ required: true, message: "Please input password!" }]
          })(
            <Input
              prefix={<Icon type="lock" style={{ color: "rgba(0,0,0,.25)" }} />}
              type="password"
              placeholder="Password"
            />
          )}
        </FormItem>
        <FormItem>
          {getFieldDecorator("isAdmin", {
            valuePropName: "checked",
            initialValue: false
          })(
            <Checkbox className={styles.check}>
              This user is an admin user
            </Checkbox>
          )}
          <Button
            type="primary"
            htmlType="submit"
            className={styles.createButton}
          >
            Create
          </Button>
        </FormItem>
      </Form>
    );
  }
}

_AddUserForm.propTypes = {
  form: PropTypes.object.isRequired,
  addUser: PropTypes.func.isRequired
};

const AddUser = props => {
  const AddUserForm = Form.create()(_AddUserForm);
  const { addUser } = props;
  return (
    <Modal
      centered
      title="ADD USER"
      visible
      onCancel={props.hideModal}
      footer={null}
    >
      <AddUserForm addUser={addUser} />
    </Modal>
  );
};

AddUser.propTypes = {
  hideModal: PropTypes.func.isRequired,
  addUser: PropTypes.func.isRequired
};

const mapDispatchToProps = dispatch => ({
  addUser: form => dispatch(addUser(form))
});

export default connect(
  null,
  mapDispatchToProps
)(AddUser);
