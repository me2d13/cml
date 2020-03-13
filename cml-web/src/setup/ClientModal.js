import React from "react";
import { Form, Modal } from "antd";
import ClientForm from "./ClientForm";

function ClientModal({ client, onCancel, saveHandler, availableCommands }) {
  const [form] = Form.useForm();
  return (
    <Modal
      title="Client"
      visible={!!client}
      onCancel={onCancel}
      onOk={() => {
        form
          .validateFields()
          .then(values => {
            saveHandler(values);
          })
          .catch(info => {
            console.log("Validate Failed:", info);
          });
      }}
    >
      <ClientForm
        form={form}
        client={client}
        availableCommands={availableCommands}
      />
    </Modal>
  );
}

export default ClientModal;
