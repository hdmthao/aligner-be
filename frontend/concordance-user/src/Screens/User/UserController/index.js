import React, { Component } from "react";

import { Input, message } from "antd";
import { connect } from "react-redux";
import { createAction } from "../../../Redux/Action";

import {
  ADD_SINGLE_USER_CORPUS,
  RESET_LOADING,
  SET_ALERT,
} from "../../../Redux/Action/type";
import { dataService } from "../../../Services";
class UserController extends Component {
  state = {
    search: {
      en_sent: "",
      vi_sent: "",
    },
    selectedFile: null,
    errors: false,
  };

  handleChangeFile = (event) => {
    console.log(event.target.files);
    if (event.target.files.length !== 0) {
      let fileName = event.target.files[0].name;
      let isTxtFile = fileName.includes(".txt");
      this.setState({
        selectedFile: event.target.files[0],
        errors: !isTxtFile,
      });
    }
  };

  handleChange = (e) => {
    const { name, value } = e.target;
    this.setState({
      ...this.state,
      search: {
        ...this.state.search,
        [name]: value,
      },
    });
  };
  handleSubmit = (e) => {
    e.preventDefault();
    let { selectedFile, search } = this.state;
    let isError =
      (search.en_sent === "" || search.vi_sent === "") && selectedFile === null;

    if (isError) {
      const msg =
        "Please fill the source and target sentence or select file before importing data";
      this.props.dispatch(createAction(SET_ALERT, msg));
      setTimeout(() => {
        this.props.dispatch({ type: SET_ALERT, payload: null });
      }, 3000);
    } else {
      this.props.dispatch(
        createAction(RESET_LOADING, {
          loaded: true,
          msg: "Corpus is importing...",
        })
      );

      // Import pair-sentence
      if (!selectedFile) {
        dataService.addSingleUserCorpus([search]).then((res) => {
          this.props.dispatch(createAction(ADD_SINGLE_USER_CORPUS, res.data));
          this.props.dispatch(
            createAction(RESET_LOADING, {
              loaded: false,
              msg: null,
            })
          );

          this.setState({
            ...this.state,
            search: {
              en_sent: "",
              vi_sent: "",
            },
          });
        });
      } else {
        //Import file: bulk pair sentences
        if (this.state.errors) {
          this.props.dispatch(
            createAction(
              SET_ALERT,
              "The type of file is not valid, please change to txt file before importing"
            )
          );
          this.props.dispatch(
            createAction(RESET_LOADING, {
              loaded: false,
              msg: null,
            })
          );
          setTimeout(() => {
            this.props.dispatch({ type: SET_ALERT, payload: null });
          }, 4000);
        } else {
          dataService.addFileUserCorpus(this.state.selectedFile).then((res) => {
            this.props.dispatch(createAction(ADD_SINGLE_USER_CORPUS, res.data));
            this.props.dispatch(
              createAction(RESET_LOADING, {
                loaded: false,
                msg: null,
              })
            );
            this.setState({
              ...this.state,
              selectedFile: null,
            });
          });
        }
      }
    }
  };

  render() {
    let { search, selectedFile } = this.state;
    return (
      <div className="pt-3">
        <form onSubmit={this.handleSubmit}>
          <div className="row">
            <div className="col-5">
              <p className="content__title">Import a pair of sentences</p>
              <div style={{ marginBottom: "8px" }}>
                <Input
                  placeholder="Enter English sentence..."
                  onChange={this.handleChange}
                  value={search.en_sent}
                  disabled={selectedFile !== null ? true : false}
                  name="en_sent"
                  size="large"
                />
              </div>
              <div>
                <Input
                  placeholder="Enter Vietnamese sentence..."
                  onChange={this.handleChange}
                  value={search.vi_sent}
                  disabled={selectedFile !== null ? true : false}
                  name="vi_sent"
                  size="large"
                />
              </div>
            </div>

            <div className="col-5 d-flex flex-column justify-content-between">
              <div>
                <p className="content__title">
                  Import file
                  <a
                    href="/assets/corpus_example.txt"
                    download
                    className="text-secondary"
                  >
                    <i
                      className="fa fa-question-circle ml-2"
                      data-toggle="tooltip"
                      data-placement="right"
                      title="Click here to download the file corpus format"
                      data-animation="true"
                      data-delay="100"
                    ></i>
                  </a>
                </p>
                <div className="custom-file mb-2">
                  <input
                    type="file"
                    className="custom-file-input"
                    onChange={this.handleChangeFile}
                    name="selectedFile"
                    disabled={
                      this.state.search.en_sent.length > 0 ||
                      this.state.search.vi_sent.length > 0
                        ? true
                        : false
                    }
                  />
                  <label className="custom-file-label">
                    {this.state.selectedFile == null
                      ? "Choosen file"
                      : this.state.selectedFile.name}
                  </label>
                  {this.state.errors && (
                    <span className="text-danger">File is not valid!</span>
                  )}
                </div>
              </div>
              <div className="d-flex" style={{ marginBottom: "16px" }}>
                <button
                  type="submit"
                  className="btn-search mr-2"
                  disabled={this.props.loaded}
                >
                  {this.props.loaded ? "IMPORTING..." : "IMPORT"}
                </button>
              </div>
            </div>
          </div>
        </form>
      </div>
    );
  }
}

const mapStateToProps = (state) => {
  return {
    loaded: state.Controller.loaded,
  };
};
export default connect(mapStateToProps)(UserController);
