import React from "react";
import PropTypes from "prop-types";
import Modal from "antd/lib/modal";
import { Form, Input, Icon, Button } from "antd";
import * as styles from "./style.scss";

const FormItem = Form.Item;

class _Form extends React.Component {
  handleSubmit = e => {
    e.preventDefault();
    this.props.form.validateFields((err, values) => {
      if (!err) {
        const { valueA, valueB } = values;
        this.props.handler(valueA, valueB);
        this.props.hideModal();
      }
    });
  };

  render() {
    const { getFieldDecorator } = this.props.form;
    const { labelA, labelB } = this.props;
    return (
      <Form onSubmit={this.handleSubmit}>
        <FormItem>
          {getFieldDecorator("valueA", {
            rules: [{ required: true, message: `Please input ${labelA}!` }]
          })(
            <Input
              prefix={<Icon type="lock" style={{ color: "rgba(0,0,0,.25)" }} />}
              type="text"
              placeholder={`Enter ${labelA}...`}
            />
          )}
        </FormItem>
        <FormItem>
          {getFieldDecorator("valueB", {
            rules: [{ required: true, message: `Please input ${labelB}!` }]
          })(
            <Input
              prefix={<Icon type="lock" style={{ color: "rgba(0,0,0,.25)" }} />}
              type="text"
              placeholder={`Enter ${labelB}...`}
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

_Form.propTypes = {
  form: PropTypes.object.isRequired,
  labelA: PropTypes.string.isRequired,
  labelB: PropTypes.string.isRequired,
  handler: PropTypes.func.isRequired,
  hideModal: PropTypes.func.isRequired
};

const DoubleInput = props => {
  const EmbedForm = Form.create()(_Form);
  const { handler, hideModal, labelA, labelB } = props;
  return (
    <Modal
      centered
      title={props.title}
      visible
      onCancel={props.hideModal}
      footer={null}
    >
      <EmbedForm
        handler={handler}
        hideModal={hideModal}
        labelA={labelA}
        labelB={labelB}
      />
    </Modal>
  );
};

DoubleInput.propTypes = {
  hideModal: PropTypes.func.isRequired,
  title: PropTypes.string.isRequired,
  labelA: PropTypes.string.isRequired,
  labelB: PropTypes.string.isRequired,
  handler: PropTypes.func.isRequired
};

export default DoubleInput;
