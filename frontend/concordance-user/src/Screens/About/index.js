import React from "react";
import "./About.css";
const AboutUs = () => {
  return (
    <div className="myContainer">
      <div className="about">
        <h5 className="about-title">Contact Us</h5>
        <ul>
          <li>
            Address:
            <span>
              <a
                href="https://goo.gl/maps/deAF4UdVxs6pTPwU9"
                style={{ color: "black" }}
              >
                Room C44, Building C, 227 Nguyen Van Cu Str., District 5, Ho Chi
                Minh City, Vietnam.
              </a>
            </span>
          </li>
          <li>
            Tel: <span>(028) 66 849 856</span>
          </li>
          <li>
            Email: <span>clc@hcmus.edu.vn</span>
          </li>
        </ul>
      </div>
      <h5 className="about-title mt-5">About Us</h5>
      <div className="row">
        <div className="col-12 col-sm-6 col-md-4 col-lg-3">
          <div className="our-team">
            <div className="picture">
              <img className="img-fluid" src="images/khue.jpg" />
            </div>
            <div className="team-content">
              <h3 className="name">Hoàng Khuê</h3>
              <h4 className="title">Paracor Manager</h4>
            </div>
            <ul className="social">
              <li></li>
            </ul>
          </div>
        </div>
        <div className="col-12 col-sm-6 col-md-4 col-lg-3">
          <div className="our-team">
            <div className="picture">
              <img className="img-fluid" src="images/hung_dev.jpg" />
            </div>
            <div className="team-content">
              <h3 className="name">Hùng Trịnh</h3>
              <h4 className="title">Paracor Developer</h4>
            </div>
            <ul className="social">
              <li>
                <a
                  href="https://www.facebook.com/minhhung.it.99/"
                  className="fa fa-facebook"
                  aria-hidden="true"
                />
              </li>
              <li>
                <a
                  href="https://www.linkedin.com/in/hungtrinhit99/"
                  className="fa fa-linkedin"
                  aria-hidden="true"
                />
              </li>
            </ul>
          </div>
        </div>
        <div className="col-12 col-sm-6 col-md-4 col-lg-3">
          <div className="our-team">
            <div className="picture">
              <img className="img-fluid" src="images/bao_dev.jpg" />
            </div>
            <div className="team-content">
              <h3 className="name">Bảo Lê</h3>
              <h4 className="title">Paracor Developer</h4>
            </div>
            <ul className="social">
              <li>
                <a
                  href="https://www.facebook.com/profile.php?id=100009318796476"
                  className="fa fa-facebook"
                  aria-hidden="true"
                />
              </li>
              <li>
                <a
                  href="https://www.linkedin.com/in/hoai-bao-le-94a610187/"
                  className="fa fa-linkedin"
                  aria-hidden="true"
                />
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};
export default AboutUs;
