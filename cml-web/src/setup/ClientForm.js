import React from "react";
import { Form, Input, Select, Checkbox } from "antd";

function ClientForm({ client, availableCommands, form }) {
  const layout = {
    labelCol: {
      span: 8
    },
    wrapperCol: {
      span: 16
    }
  };
  const tailLayout = {
    wrapperCol: {
      offset: 8,
      span: 16
    }
  };
  return (
    <Form {...layout} name="client" form={form} initialValues={client}>
      <Form.Item
        label="Name/message"
        name="message"
        rules={[
          {
            required: true,
            message: "Please enter some name!"
          }
        ]}
      >
        <Input />
      </Form.Item>
      <Form.Item {...tailLayout} name="approved" valuePropName="checked">
        <Checkbox>Approved</Checkbox>
      </Form.Item>
      <Form.Item {...tailLayout} name="all_commands" valuePropName="checked">
        <Checkbox>All commands</Checkbox>
      </Form.Item>
      <Form.Item name="commands" label="Commands"
      rules={[{ type: 'array' }]}
      >
        <Select
          mode="multiple"
          placeholder="Please select commands">
          {availableCommands.map(it => <Select.Option key={it} value={it}>{it}</Select.Option>)}
        </Select>
      </Form.Item>
    </Form>
  );
}

export default ClientForm;
