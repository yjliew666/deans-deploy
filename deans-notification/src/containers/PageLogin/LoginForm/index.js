import React from "react";
import PropTypes from "prop-types";
import { Form, Input, Icon, Checkbox, Button, message } from "antd";
import * as styles from "./style.scss";

const FormItem = Form.Item;

class LoginForm extends React.Component {
  handleSubmit = e => {
    e.preventDefault();
    this.props.form.validateFields((err, values) => {
      if (!err) {
        const { username, password } = values;
        const form = new FormData();
        form.append("username", username);
        form.append("password", password);
        this.props
          .userLogin(form)
          .then(() => {
            if (this.props.flag) {
              message.success("Login successful!", 2);
              this.props.setRedirect();
            } else {
              message.error("Login failed, please try again.", 2);
            }
          })
          .catch(() => {
            /* do nothing */
          });
      }
    });
  };

  render() {
    const { getFieldDecorator } = this.props.form;
    return (
      <Form onSubmit={this.handleSubmit} className={styles.loginForm}>
        <FormItem>
          {getFieldDecorator("username", {
            rules: [{ required: true, message: "Please input your username!" }]
          })(
            <Input
              prefix={<Icon type="user" style={{ color: "rgba(0,0,0,.25)" }} />}
              placeholder="Username"
            />
          )}
        </FormItem>
        <FormItem>
          {getFieldDecorator("password", {
            rules: [{ required: true, message: "Please input your Password!" }]
          })(
            <Input
              prefix={<Icon type="lock" style={{ color: "rgba(0,0,0,.25)" }} />}
              type="password"
              placeholder="Password"
            />
          )}
        </FormItem>
        <FormItem>
          {getFieldDecorator("remember", {
            valuePropName: "checked",
            initialValue: true
          })(<Checkbox>Remember me</Checkbox>)}
          <Button
            type="primary"
            htmlType="submit"
            className={styles.loginButton}
          >
            Log in
          </Button>
        </FormItem>
      </Form>
    );
  }
}

LoginForm.propTypes = {
  flag: PropTypes.bool.isRequired,
  userLogin: PropTypes.func.isRequired,
  setRedirect: PropTypes.func.isRequired,
  form: PropTypes.object.isRequired
};

export default Form.create()(LoginForm);
