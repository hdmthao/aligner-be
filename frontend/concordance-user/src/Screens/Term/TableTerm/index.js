import React, { Component } from "react";
import "./TableHelp.css";
import { connect } from "react-redux";
import { Table } from "antd";

class TableTerm extends Component {
  render() {
    // Render <tr> </tr> tags of tbody in table
    const data = this.props.tags[`${this.props.typeTag}`];
    const columns = [
      {
        title: "Tag",
        dataIndex: "tag",
        key: "tag",
      },
      {
        title: "Description",
        dataIndex: "description",
        key: "description",
      },
    ];

    return (
      <div>
        <Table
          bordered
          dataSource={data}
          columns={columns}
          pagination={{ pageSize: 20 }}
        ></Table>
      </div>
    );
  }
}
const mapStateToProps = (state) => {
  return {
    tags: state.Tag.tags,
  };
};
export default connect(mapStateToProps)(TableTerm);
