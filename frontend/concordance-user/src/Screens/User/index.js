import React, { Component } from "react";
import UserController from "./UserController";
import Alert from "../../Layouts/Alert";
import Linebreak from "../../Components/Linebreak";
import TableUser from "./UserTable";
import $ from "jquery";
import Modal from "../../Components/Modal";
import Backdrop from "../../Components/Backdrop";
import { ArcherContainer, ArcherElement } from "react-archer";
import { connect } from "react-redux";
class User extends Component {
  state = {
    selectedId: null,
    modalToggle: false,
  };
  componentDidMount() {
    $(".sourceIDHome, .targetIDHome").on("scroll", function () {
      $(".sourceIDHome, .targetIDHome").scrollTop($(this).scrollTop());
    });
  }
  handleRowSelected = (id) => {
    this.setState({
      selectedId: id,
    });
  };
  openModalHandler = (id) => {
    this.setState({
      modalToggle: !this.state.modalToggle,
      selectedId: id,
    });
  };
  render() {
    let { selectedId } = this.state;
    let enData = [],
      viData = [];
    let renderSource = null,
      renderTarget = null;

    // Pipe Data
    this.props.data.map((item) => {
      enData.push({
        sentence_id: item.id,
        sentence: item.en_sent,
      });

      viData.push({
        sentence_id: item.id,
        sentence: item.vi_sent,
      });
    });

    // Word Alignment
    let fIndexAlignment = this.props.data.findIndex(
      (item) => item.id === selectedId
    );

    if (fIndexAlignment !== -1) {
      let alignmentArr = this.props.data[fIndexAlignment].envi_align;
      let sourceSent = this.props.data[fIndexAlignment].en_sent
        .trim()
        .split(" ");

      renderSource = sourceSent.map((item, index) => {
        let obj = {
          targetId: "target" + alignmentArr[index],
          targetAnchor: "top",
          sourceAnchor: "bottom",
          style: { strokeColor: "#275efe", strokeWidth: 1 },
        };
        return (
          <ArcherElement id={index} relations={[obj]} key={index}>
            <div className={"word-item"}>
              <p className="mb-2">{item}</p>
            </div>
          </ArcherElement>
        );
      });

      let targetSent = this.props.data[fIndexAlignment].vi_sent
        .trim()
        .split(" ");

      renderTarget = targetSent.map((item, index) => {
        return (
          <ArcherElement id={`target${index + 1}`} key={index}>
            <div className={"word-item"}>
              <p className="mb-2">{item}</p>
            </div>
          </ArcherElement>
        );
      });
    }

    return (
      <div className="myContainer">
        <UserController />
        <Linebreak />
        <Alert />

        <div className="mt-3">
          <TableUser
            data={enData}
            selectedId={selectedId}
            classID="sourceIDHome"
            handleRowSelected={this.handleRowSelected}
            openModalHandler={this.openModalHandler}
            tableName="English sentence"
          />
          <TableUser
            data={viData}
            selectedId={selectedId}
            classID="targetIDHome"
            handleRowSelected={this.handleRowSelected}
            openModalHandler={this.openModalHandler}
            tableName="Vietnamese sentence"
          />
        </div>

        {/* Modal WordAlignment */}
        <Modal
          show={this.state.modalToggle}
          modalClosed={this.openModalHandler}
          height="380"
        >
          <div className="myModal-top">
            <p className="modal-title">Show Alignment</p>
            <i className="fa fa-times" onClick={this.openModalHandler}></i>
          </div>
          <div className="myModal-content">
            <div className="modal-content__right">
              <ArcherContainer>
                <div className="modal-content__item-right d-flex source justify-content-around align-items-center fs-14">
                  {renderSource}
                </div>
                <div className="modal-content__item-right d-flex justify-content-around align-items-center fs-14">
                  {renderTarget}
                </div>
              </ArcherContainer>
            </div>
          </div>
        </Modal>
        <Backdrop
          show={this.state.modalToggle}
          clicked={this.openModalHandler}
        />
      </div>
    );
  }
}

const mapStateToProps = (state) => {
  return {
    data: state.User.data,
  };
};
export default connect(mapStateToProps)(User);
