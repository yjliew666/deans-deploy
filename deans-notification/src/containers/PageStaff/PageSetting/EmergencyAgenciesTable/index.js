import React from "react";
import PropTypes from "prop-types";
import { Table, Button } from "antd";
import * as styles from "./style.scss";

const EmergencyAgenciesTable = props => {
  const COLUMNS = [
    {
      title: "Agency",
      dataIndex: "agency",
      key: "agency"
    },
    {
      title: "Phone Number",
      dataIndex: "phoneNumber",
      key: "phoneNumber"
    },
    {
      title: "Actions",
      key: "actions",
      dataIndex: "actions"
    }
  ];

  const createDataSource = () => {
    const { emergencyAgencies, editPhoneNumber } = props;
    return emergencyAgencies.map(agency => {
      const id = agency.agency_id;
      const name = agency.agency;
      const phoneNumber = agency.phone_number;
      return {
        agency: name,
        phoneNumber: phoneNumber,
        actions: (
          <div className={styles.actions}>
            <Button
              type="dashed"
              onClick={() =>
                props.showModal("SINGLE_INPUT", {
                  title: "EDIT PHONE NUMBER",
                  defaultValue: phoneNumber,
                  handler: phoneNumber => editPhoneNumber(id, phoneNumber)
                })
              }
            >
              Edit
            </Button>
            <Button type="danger">Delete</Button>
          </div>
        )
      };
    });
  };

  return (
    <Table
      dataSource={createDataSource()}
      columns={COLUMNS}
      pagination={false}
    />
  );
};

EmergencyAgenciesTable.propTypes = {
  emergencyAgencies: PropTypes.array,
  showModal: PropTypes.func.isRequired,
  editPhoneNumber: PropTypes.func.isRequired
};

export default EmergencyAgenciesTable;
