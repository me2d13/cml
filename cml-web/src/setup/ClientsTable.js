import React from "react";
import { Table, Tag, Checkbox, Button, Tooltip, Popconfirm } from "antd";
import { DeleteOutlined, EditOutlined } from "@ant-design/icons";

function ClientsTable({ clients, deleteHandler, editHandler }) {
  const columns = [
    {
      title: "Action",
      key: "action",
      render: value => (
        <div className="actionCell">
          <Tooltip title="Delete" mouseEnterDelay="1">
            <Popconfirm
              title="Are you sure you want to delete the client?"
              placement="right"
              onConfirm={() => deleteHandler(value)}
            >
              <Button danger shape="circle" icon={<DeleteOutlined />} />
            </Popconfirm>
          </Tooltip>
          <Tooltip title="Edit" mouseEnterDelay="1">
            <Button shape="circle" icon={<EditOutlined />} onClick={() => editHandler(value)} />
          </Tooltip>
        </div>
      )
    },
    {
      title: "Approved",
      dataIndex: "approved",
      render: value => <Checkbox checked={value} />
    },
    {
      title: "Id",
      dataIndex: "id"
    },
    {
      title: "Name/message",
      dataIndex: "message"
    },
    {
      title: "Registered",
      dataIndex: "registered_at",
      render: value => new Date(value).toLocaleString(),
      sorter: (a, b) =>
        new Date(a.registered_at).getTime() -
        new Date(b.registered_at).getTime(),
      defaultSortOrder: "descend"
    },
    {
      title: "All commands",
      dataIndex: "all_commands",
      render: value => <Checkbox checked={value} />
    },
    {
      title: "Commands",
      dataIndex: "commands",
      render: tags => (
        <span>
          {tags.map(tag => {
            const color = "geekblue";
            return (
              <Tag color={color} key={tag}>
                {tag}
              </Tag>
            );
          })}
        </span>
      )
    }
  ];

  return <Table dataSource={clients} columns={columns} />;
}

export default ClientsTable;
