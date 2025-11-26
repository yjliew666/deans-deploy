import React from "react";
import PropTypes from "prop-types";
import { Button, Table, Switch } from "antd";
import * as styles from "./style.scss";

const COLUMNS = [
  {
    title: "Username",
    dataIndex: "username",
    key: "username"
  },
  {
    title: "Is Admin",
    dataIndex: "adminStatus",
    key: "adminStatus"
  },
  {
    title: "Action",
    dataIndex: "action",
    key: "action"
  }
];

const UserTable = props => {
  const { editUser, showEditUserModal, currentUser } = props;

  const toggleAdmin = (id, isAdmin) => {
    const form = new FormData();
    form.append("is_staff", isAdmin);
    editUser(id, form);
  };

  const createDataSource = arr => {
    return arr.map(val => ({
      key: val.id,
      username: val.username,
      adminStatus: (
        <Switch
          disabled={val.username === currentUser}
          defaultChecked={val.is_staff}
          onChange={checked => toggleAdmin(val.id, checked)}
        />
      ),
      action: (
        <div className={styles.actions}>
          <Button
            type="dashed"
            onClick={() =>
              showEditUserModal({ userId: val.id, editUser: editUser })
            }
          >
            Change Password
          </Button>
        </div>
      )
    }));
  };

  return (
    <Table dataSource={createDataSource(props.userList)} columns={COLUMNS} />
  );
};

UserTable.propTypes = {
  userList: PropTypes.array.isRequired,
  editUser: PropTypes.func.isRequired,
  showEditUserModal: PropTypes.func.isRequired,
  currentUser: PropTypes.string.isRequired
};

export default UserTable;
