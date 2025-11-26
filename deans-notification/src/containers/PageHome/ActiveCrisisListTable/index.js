import React from "react";
import { connect } from "react-redux";
import PropTypes from "prop-types";
import { Table, Tag } from "antd";
// import * as styles from "./style.scss";

const createDataSource = (crisisList, crisisType) =>
  crisisList.filter(crisis => crisis.crisis_status !== "RS").map(crisis => {
    const key = crisis.crisis_id;
    const type = crisis.crisis_type
      .map(val => crisisType && crisisType[val])
      // eslint-disable-next-line react/jsx-key
      .map((type, index) => (
        <Tag key={index} color="purple">
          {type}
        </Tag>
      ));
    const location = crisis.crisis_location1.replace(/"/g, "");
    const time = (() => {
      const date = new Date(crisis.crisis_time);
      return date.toLocaleString("en", {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "numeric",
        minute: "numeric"
      });
    })();
    const description = crisis.crisis_description;
    return {
      key: key,
      crisisType: type,
      location: location,
      description: description,
      reportTime: time
    };
  });

const ActiveCrisisListTable = props => {
  const { crises, crisisType } = props;
  const COLUMNS = [
    {
      title: "Crisis Type",
      dataIndex: "crisisType",
      key: "crisisType",
      width: 100
    },
    {
      title: "Location",
      dataIndex: "location",
      key: "location",
      width: 300
    },
    {
      title: "Description",
      key: "description",
      dataIndex: "description",
      width: 200
    },
    {
      title: "Report Time",
      key: "reportTime",
      dataIndex: "reportTime",
      width: 150
    }
  ];
  return (
    <Table
      dataSource={createDataSource(crises, crisisType)}
      columns={COLUMNS}
    />
  );
};

ActiveCrisisListTable.propTypes = {
  crisisType: PropTypes.object,
  assistanceType: PropTypes.object,
  crises: PropTypes.array
};

export default connect(state => {
  const { system } = state;
  return {
    crisisType: system && system.crisisType,
    assistanceType: system && system.assistanceType
  };
})(ActiveCrisisListTable);
