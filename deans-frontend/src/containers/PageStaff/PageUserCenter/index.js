import React from "react";
import PropTypes from "prop-types";
import { connect } from "react-redux";
import { getUserList, showModal, editUser } from "@redux/actions";
import { Button } from "antd";
import UserTable from "./UserTable";
import * as styles from "./style.scss";

class PageUserCenter extends React.Component {
  componentDidMount() {
    this.props.getUserList();
  }

  render() {
    const {
      userList,
      addUser,
      showEditUserModal,
      editUser,
      currentUser
    } = this.props;
    return (
      <div>
        <h1>User Center</h1>
        <div className={styles.subHeader}>
          <div className={styles.item}>User List</div>
          <div className={styles.item}>
            <Button onClick={addUser}>Add</Button>
          </div>
        </div>
        <div className={styles.userTable}>
          <UserTable
            userList={userList || []}
            showEditUserModal={showEditUserModal}
            editUser={editUser}
            currentUser={currentUser}
          />
        </div>
      </div>
    );
  }
}

PageUserCenter.propTypes = {
  addUser: PropTypes.func.isRequired,
  editUser: PropTypes.func.isRequired,
  showEditUserModal: PropTypes.func.isRequired,
  userList: PropTypes.array,
  currentUser: PropTypes.string,
  getUserList: PropTypes.func.isRequired
};

const mapStateToProps = state => {
  const { staff } = state;
  return {
    currentUser: staff && staff.currentUser,
    userList: staff && staff.userList
  };
};

const mapDispatchToProps = dispatch => ({
  getUserList: () => dispatch(getUserList()),
  addUser: modalProps => dispatch(showModal("ADD_USER", modalProps)),
  showEditUserModal: modalProps => dispatch(showModal("EDIT_USER", modalProps)),
  editUser: (id, form) => dispatch(editUser(id, form))
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(PageUserCenter);
