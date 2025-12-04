import React from "react";
import PropTypes from "prop-types";
import { Form, Select, Button, message } from "antd";

const FormItem = Form.Item;
const Option = Select.Option;

class CrisisDispatchForm extends React.Component {
  state = {
    confirmDirty: false,
    autoCompleteResult: []
  };

  createEmergencyAgenciesList = arr =>
    arr.map((val, index) => (
      <Option value={val.phone_number} key={index}>
        {val.agency}
      </Option>
    ));

  handleSubmit = e => {
    e.preventDefault();
    this.props.form.validateFieldsAndScroll((err, values) => {
      if (!err) {
        console.log("Received values of form: ", values);
        const { agencies } = values;
        const phoneNumbers = "[" + agencies.join(", ") + "]";
        this.props
          .dispatchCrisis(this.props.crisisId, phoneNumbers)
          .then(() => {
            message.success("Dispatched!");
            this.props.hideModal();
          })
          .catch(() => null);
      }
    });
  };

  handleConfirmBlur = e => {
    const value = e.target.value;
    this.setState({ confirmDirty: this.state.confirmDirty || !!value });
  };

  render() {
    const { getFieldDecorator } = this.props.form;

    const formItemLayout = {
      labelCol: {
        sm: { span: 8 }
      },
      wrapperCol: {
        sm: { span: 15 }
      }
    };

    return (
      <Form onSubmit={this.handleSubmit}>
        <FormItem {...formItemLayout} label="Agencies">
          {getFieldDecorator("agencies", {
            rules: [
              {
                type: "array",
                required: true,
                message: "Please select emergency agencies!"
              }
            ]
          })(
            <Select
              mode="multiple"
              placeholder="Select emergency agencies to notify"
            >
              {this.createEmergencyAgenciesList(this.props.emergencyAgencies)}
            </Select>
          )}
        </FormItem>
        <FormItem style={{ marginBottom: 0 }}>
          <Button type="primary" htmlType="submit" style={{ width: "100%" }}>
            Dispatch
          </Button>
        </FormItem>
      </Form>
    );
  }
}

CrisisDispatchForm.propTypes = {
  hideModal: PropTypes.func.isRequired,
  crisisId: PropTypes.number.isRequired,
  emergencyAgencies: PropTypes.array,
  dispatchCrisis: PropTypes.func.isRequired
};

export default Form.create()(CrisisDispatchForm);
