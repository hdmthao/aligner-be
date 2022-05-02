import React from "react";
import PropTypes from "prop-types";
import "./modal.css";
const Modal = (props) => {
  return (
    <div
      className="Modal"
      style={{
        transform: props.show ? "translateY(0)" : "translateY(-100vh)",
        opacity: props.show ? 1 : 0,
        height: `${props.height}px`,
      }}
    >
      {props.children}
    </div>
  );
};

Modal.defaultProps = {
  height: "480",
};

export default Modal;
