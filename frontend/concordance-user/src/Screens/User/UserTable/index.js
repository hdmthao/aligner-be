import React, { Component } from "react";
import { connect } from "react-redux";
class TableUser extends Component {
  render() {
    let { data } = this.props;
    let tbodyContent = data.map((item) => {
      let activeClass =
        this.props.selectedId === item.sentence_id ? "text-info" : null;
      return (
        <tr
          key={item.sentence_id}
          onDoubleClick={() => this.props.openModalHandler(item.sentence_id)}
          onClick={() => this.props.handleRowSelected(item.sentence_id)}
          className={activeClass}
        >
          <td className="col-12">
            {item.sentence.length > 100
              ? item.sentence.slice(0, 100) + "..."
              : item.sentence}
          </td>
        </tr>
      );
    });
    return (
      <div className="table__home">
        <div className="table-content">
          <table className="table table-fixed">
            <thead>
              <tr>
                <th className="col-12">{this.props.tableName}</th>
              </tr>
            </thead>
            <tbody className={this.props.classID}>{tbodyContent}</tbody>
          </table>
        </div>
      </div>
    );
  }
}

export default connect()(TableUser);
