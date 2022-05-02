import React, { Component } from "react";
import "./Home.css";
import { Link } from "react-router-dom";
class Home extends Component {
  render() {
    return (
      <div className="feat bg-gray pt-5 pb-5">
        <div className="container">
          <div className="row">
            <div className="section-head col-sm-12">
              <h1>
                <span>Parallel Corpus Tool</span>
              </h1>
              <p>
                Parallel Corpus Tool is the most powerful tool with a variety of
                search options.It is a tool used to mine bilingual corpus for
                many applications different purposes (teaching, research, ...),
                comparing vocabulary in English to Vietnamese and vice versa, as
                well as supporting vocabulary statistics in the corpus based on
                the most criteria identification and accompanying label
                information.
              </p>
            </div>
            <div className="col-lg-4 col-sm-6 module-item">
              <Link to="/user">
                <div className="item">
                  <span className="icon feature_box_col_two">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      xmlnsXlink="http://www.w3.org/1999/xlink"
                      width="1.5em"
                      height="1.5m"
                      viewBox="0 0 60 60"
                      style={{ enableBackground: "new 0 0 60 60" }}
                      xmlSpace="preserve"
                    >
                      <g>
                        <path
                          d="M36,34.5v24h24v-24H36z M58,56.5H38v-20h9v11.586l-4.293-4.293l-1.414,1.414L48,51.914l6.707-6.707l-1.414-1.414L49,48.086
		V36.5h9V56.5z"
                        />
                        <path
                          d="M30.768,32.859c-0.002-0.003-0.064-0.078-0.165-0.21c-0.006-0.008-0.012-0.016-0.019-0.024
		c-0.053-0.069-0.115-0.153-0.186-0.251c-0.001-0.002-0.002-0.003-0.003-0.005c-0.149-0.207-0.336-0.476-0.544-0.8
		c-0.005-0.007-0.009-0.015-0.014-0.022c-0.098-0.154-0.202-0.32-0.308-0.497c-0.008-0.013-0.016-0.026-0.024-0.04
		c-0.226-0.379-0.466-0.808-0.705-1.283l-0.001-0.002c-0.127-0.254-0.254-0.523-0.378-0.802l0,0
		c-0.017-0.039-0.035-0.077-0.052-0.116h0c-0.055-0.125-0.11-0.256-0.166-0.391c-0.02-0.049-0.04-0.1-0.06-0.15
		c-0.052-0.131-0.105-0.263-0.161-0.414c-0.102-0.272-0.198-0.556-0.29-0.849l-0.055-0.178c-0.006-0.02-0.013-0.04-0.019-0.061
		c-0.094-0.316-0.184-0.639-0.26-0.971l-0.091-0.396l-0.341-0.22C26.346,24.803,26,24.176,26,23.5v-4
		c0-0.561,0.238-1.084,0.67-1.475L27,17.728V11.5v-0.354l-0.027-0.021c-0.034-0.722,0.009-2.935,1.623-4.776
		C30.253,4.458,33.081,3.5,37,3.5c3.905,0,6.727,0.951,8.386,2.828c1.947,2.201,1.625,5.017,1.623,5.041L47,17.728l0.33,0.298
		C47.762,18.415,48,18.939,48,19.5v4c0,0.873-0.571,1.637-1.422,1.899c-0.528,0.162-0.823,0.722-0.661,1.25
		c0.162,0.527,0.725,0.82,1.25,0.661C48.861,26.787,50,25.256,50,23.5v-4c0-0.963-0.359-1.897-1-2.625v-5.319
		c0.057-0.55,0.276-3.824-2.092-6.525C44.854,2.688,41.521,1.5,37,1.5s-7.854,1.188-9.908,3.53
		c-1.435,1.637-1.918,3.481-2.064,4.805C23.314,8.949,21.294,8.5,19,8.5c-10.389,0-10.994,8.855-11,9v4.579
		c-0.648,0.706-1,1.521-1,2.33v3.454c0,1.079,0.483,2.085,1.311,2.765c0.825,3.11,2.854,5.46,3.644,6.285v2.743
		c0,0.787-0.428,1.509-1.171,1.915l-6.653,4.173C1.583,47.134,0,49.801,0,52.703V56.5h14h2h11c0.552,0,1-0.447,1-1s-0.448-1-1-1H16
		v-2.238c0-2.571,1.402-4.934,3.659-6.164l8.921-4.866C30.073,40.417,31,38.854,31,37.155v-4.018v-0.001l-0.194-0.232L30.768,32.859
		z M29,37.155c0,0.968-0.528,1.856-1.377,2.32l-2.646,1.443l-0.649,0.354l-5.626,3.069c-2.9,1.582-4.701,4.616-4.701,7.92V54.5H2
		v-1.797c0-2.17,1.184-4.164,3.141-5.233l6.652-4.173c1.333-0.727,2.161-2.121,2.161-3.641v-3.591l-0.318-0.297
		c-0.026-0.024-2.683-2.534-3.468-5.955l-0.091-0.396l-0.342-0.22C9.275,28.899,9,28.4,9,27.863v-3.454
		c0-0.36,0.245-0.788,0.671-1.174L10,22.938l-0.002-5.38C10.016,17.271,10.537,10.5,19,10.5c2.393,0,4.408,0.553,6,1.644v4.731
		c-0.64,0.729-1,1.662-1,2.625v4c0,0.304,0.035,0.603,0.101,0.893c0.027,0.116,0.081,0.222,0.118,0.334
		c0.055,0.168,0.099,0.341,0.176,0.5c0.001,0.002,0.002,0.003,0.003,0.005c0.256,0.528,0.629,1,1.099,1.377
		c0.005,0.019,0.011,0.036,0.016,0.054c0.06,0.229,0.123,0.457,0.191,0.68l0.081,0.261c0.014,0.046,0.031,0.093,0.046,0.139
		c0.035,0.108,0.069,0.216,0.105,0.322c0.06,0.175,0.123,0.355,0.196,0.553c0.031,0.083,0.065,0.156,0.097,0.237
		c0.082,0.209,0.164,0.411,0.25,0.611c0.021,0.048,0.039,0.1,0.06,0.147l0.056,0.126c0.026,0.058,0.053,0.11,0.079,0.167
		c0.098,0.214,0.194,0.421,0.294,0.622c0.016,0.032,0.031,0.067,0.047,0.099c0.063,0.125,0.126,0.243,0.189,0.363
		c0.108,0.206,0.214,0.4,0.32,0.588c0.052,0.092,0.103,0.182,0.154,0.269c0.144,0.246,0.281,0.472,0.414,0.682
		c0.029,0.045,0.057,0.092,0.085,0.135c0.242,0.375,0.452,0.679,0.626,0.916c0.046,0.063,0.086,0.117,0.125,0.17
		c0.022,0.029,0.052,0.071,0.071,0.097V37.155z"
                        />
                      </g>
                      <g></g>
                      <g></g>
                      <g></g>
                      <g></g>
                      <g></g>
                      <g></g>
                      <g></g>
                      <g></g>
                      <g></g>
                      <g></g>
                      <g></g>
                      <g></g>
                      <g></g>
                      <g></g>
                      <g></g>
                    </svg>
                  </span>
                  <h4>User Corpus</h4>
                  <p>
                    Import your corpus and the result is the parallel corpus.
                    You can import the single sentence or the couple of
                    alignment file.
                  </p>
                </div>
              </Link>
            </div>
            <div className="col-lg-4 col-sm-6 module-item">
              <Link to="/corpus">
                <div className="item">
                  <span className="icon feature_box_col_one ">
                    <svg
                      version="1.1"
                      id="Capa_1"
                      xmlns="http://www.w3.org/2000/svg"
                      xmlnsXlink="http://www.w3.org/1999/xlink"
                      width="1.5em"
                      height="1.5m"
                      viewBox="0 0 58.371 58.371"
                      style={{ enableBackground: "new 0 0 58.371 58.371" }}
                      xmlSpace="preserve"
                    >
                      <g>
                        <path
                          d="M55.833,56.679l-5.969-6.243c1.745-1.918,2.82-4.458,2.82-7.25c0-5.953-4.843-10.796-10.796-10.796
		s-10.796,4.843-10.796,10.796s4.843,10.796,10.796,10.796c2.442,0,4.689-0.824,6.5-2.196l6,6.276
		c0.196,0.205,0.459,0.309,0.723,0.309c0.249,0,0.497-0.092,0.691-0.277C56.2,57.711,56.215,57.079,55.833,56.679z M33.092,43.186
		c0-4.85,3.946-8.796,8.796-8.796s8.796,3.946,8.796,8.796s-3.946,8.796-8.796,8.796S33.092,48.036,33.092,43.186z"
                        />
                        <path
                          d="M28.096,43.1c0.025-4.029,1.793-7.644,4.578-10.153c-0.911,0.054-1.844,0.097-2.807,0.123
		c-0.87,0.027-1.74,0.041-2.606,0.041c-0.869,0-1.742-0.014-2.614-0.042c-7.341-0.201-13.191-1.238-17.403-2.717
		C5.264,29.685,3.569,28.899,2.261,28v7.111v0.5v0.5V37.4c2.846,2.971,12.394,5.711,25,5.711
		C27.544,43.111,27.816,43.103,28.096,43.1z"
                        />
                        <path
                          d="M24.896,29.965c0.326,0.009,0.651,0.018,0.982,0.023C26.334,29.996,26.795,30,27.261,30s0.926-0.004,1.383-0.011
		c0.33-0.005,0.656-0.015,0.982-0.023c0.116-0.003,0.234-0.005,0.349-0.008c11.253-0.359,19.648-2.915,22.286-5.668V23v-0.5V22
		v-7.111C47.393,18.232,37.105,20,27.261,20s-20.133-1.768-25-5.111V22v0.5V23v1.289c2.638,2.754,11.033,5.31,22.286,5.668
		C24.662,29.96,24.78,29.962,24.896,29.965z"
                        />
                        <path
                          d="M52.261,11.306V9.5V9c0-0.168-0.056-0.319-0.135-0.458C51.003,4.241,42.376,0,27.261,0C12.183,0,3.564,4.22,2.407,8.51
		C2.322,8.657,2.261,8.818,2.261,9v0.5v1.806C5.097,14.267,14.577,17,27.261,17S49.424,14.267,52.261,11.306z"
                        />
                        <path
                          d="M28.43,46.187c-0.39,0.005-0.772,0.014-1.17,0.014c-12.346,0-20.866-2.29-25-5.201v8.201c0,0.162,0.043,0.315,0.117,0.451
		c1.181,4.895,11.747,8.549,24.883,8.549c4.764,0,9.182-0.486,12.945-1.332C34.389,56.157,29.686,51.819,28.43,46.187z"
                        />
                      </g>
                      <g />
                      <g />
                      <g />
                      <g />
                      <g />
                      <g />
                      <g />
                      <g />
                      <g />
                      <g />
                      <g />
                      <g />
                      <g />
                      <g />
                      <g />
                    </svg>
                  </span>
                  <h4>Paracor Corpus</h4>
                  <p>
                    Our corpus with 54000 pairs of bilingual sentences from the
                    Computational Linguistics Center
                  </p>
                </div>
              </Link>
            </div>
            <div className="col-lg-4 col-sm-6 module-item">
              <Link to="/faq">
                <div className="item">
                  <span className="icon feature_box_col_three">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      xmlnsXlink="http://www.w3.org/1999/xlink"
                      width="1.5em"
                      height="1.5em"
                      viewBox="0 0 285.939 285.939"
                      style={{ enableBackground: "new 0 0 285.939 285.939" }}
                      xmlSpace="preserve"
                    >
                      <g>
                        <g>
                          <path
                            style={{ fill: "#F9BA48" }}
                            d="M142.967,285.939L142.967,285.939c-10.355,0-18.75-8.395-18.75-18.75l0,0
			c0-10.355,8.395-18.75,18.75-18.75l0,0c10.355,0,18.75,8.395,18.75,18.75l0,0C161.717,277.544,153.322,285.939,142.967,285.939z"
                          />
                          <path
                            style={{ fill: "#F9BA48" }}
                            d="M72.655,117.189v4.688h37.5l0,0c0-10.355,8.395-18.75,18.75-18.75h28.125
			c10.355,0,18.75,8.395,18.75,18.75v14.063c0,10.355-8.395,18.75-18.75,18.75h-14.063c-10.355,0-18.75,8.395-18.75,18.75v37.5
			c0,10.355,8.395,18.75,18.75,18.75l0,0c10.355,0,18.75-8.395,18.75-18.75v-18.75l0,0c28.477,0,51.563-23.086,51.563-51.563
			v-23.438c0-28.477-23.086-51.563-51.563-51.563h-37.5C95.741,65.627,72.655,88.713,72.655,117.189z"
                          />
                          <path
                            style={{ fill: "#333333" }}
                            d="M167.267,260.224l-1.72-9.22c2.939-0.548,5.902-1.219,8.798-1.987l2.419,9.061
			C173.633,258.902,170.436,259.629,167.267,260.224z"
                          />
                          <path
                            style={{ fill: "#333333" }}
                            d="M195.055,251.721l-3.717-8.606c5.47-2.367,10.833-5.175,15.923-8.339l4.955,7.955
			C206.731,246.147,200.956,249.171,195.055,251.721z M90.51,251.561c-5.892-2.573-11.653-5.611-17.133-9.047l4.983-7.945
			c5.086,3.192,10.439,6.014,15.9,8.395L90.51,251.561z M227.867,231.321l-6.07-7.148c4.57-3.872,8.883-8.119,12.825-12.614
			l7.05,6.178C237.425,222.574,232.78,227.149,227.867,231.321z M57.767,231.063c-4.898-4.181-9.53-8.766-13.772-13.622l7.069-6.159
			c3.938,4.514,8.241,8.77,12.792,12.652L57.767,231.063z M253.339,202.282l-7.875-5.081c3.248-5.039,6.145-10.35,8.606-15.792
			l8.541,3.863C259.963,191.135,256.841,196.858,253.339,202.282z M32.38,201.949c-3.483-5.433-6.581-11.17-9.22-17.044l8.55-3.834
			c2.447,5.452,5.33,10.777,8.559,15.816L32.38,201.949z M269.263,167.093l-9.019-2.555c1.627-5.752,2.836-11.672,3.6-17.611
			l9.3,1.191C272.328,154.511,271.016,160.896,269.263,167.093z M16.56,166.689c-1.734-6.202-3.019-12.591-3.816-18.984l9.3-1.162
			c0.741,5.939,1.936,11.864,3.544,17.63L16.56,166.689z M264.819,128.955c-0.112-6-0.67-12.023-1.65-17.911l9.248-1.537
			c1.059,6.333,1.655,12.816,1.777,19.275L264.819,128.955z M21.121,128.575l-9.375-0.202c0.141-6.464,0.759-12.947,1.833-19.275
			l9.248,1.575C21.819,116.547,21.247,122.571,21.121,128.575z M258.913,93.583c-1.847-5.681-4.134-11.278-6.806-16.645l8.386-4.186
			c2.883,5.775,5.353,11.813,7.336,17.934L258.913,93.583z M27.144,93.227l-8.906-2.93c2.016-6.131,4.5-12.15,7.388-17.897
			l8.377,4.2C31.325,81.939,29.014,87.532,27.144,93.227z M242.905,61.474c-3.427-4.898-7.256-9.591-11.367-13.95l6.811-6.436
			c4.425,4.688,8.541,9.736,12.234,15.009L242.905,61.474z M43.241,61.183l-7.673-5.391c3.698-5.259,7.833-10.294,12.277-14.972
			l6.792,6.464C50.506,51.621,46.672,56.299,43.241,61.183z M218.263,35.407c-4.692-3.689-9.708-7.073-14.916-10.059l4.659-8.128
			c5.597,3.206,11.002,6.848,16.05,10.819L218.263,35.407z M67.949,35.191l-5.766-7.388c5.091-3.98,10.505-7.603,16.097-10.777
			l4.622,8.156C77.713,28.122,72.683,31.493,67.949,35.191z M187.133,17.622c-5.573-2.166-11.358-3.933-17.194-5.25l2.067-9.145
			c6.286,1.425,12.516,3.328,18.52,5.662L187.133,17.622z M99.158,17.482l-3.37-8.742c6.009-2.32,12.253-4.205,18.553-5.606
			l2.044,9.145C110.535,13.582,104.741,15.335,99.158,17.482z M152.164,9.714c-5.944-0.441-12.038-0.45-17.991-0.028l-0.67-9.347
			c6.398-0.464,12.947-0.45,19.355,0.028L152.164,9.714z"
                          />
                          <path
                            style={{ fill: "#333333" }}
                            d="M118.667,260.224c-3.173-0.595-6.366-1.317-9.492-2.147l2.419-9.061
			c2.897,0.769,5.859,1.439,8.798,1.987L118.667,260.224z"
                          />
                        </g>
                      </g>
                      <g></g>
                      <g></g>
                      <g></g>
                      <g></g>
                      <g></g>
                      <g></g>
                      <g></g>
                      <g></g>
                      <g></g>
                      <g></g>
                      <g></g>
                      <g></g>
                      <g></g>
                      <g></g>
                      <g></g>
                    </svg>
                  </span>
                  <h4>FAQ</h4>
                  <p>
                    Information about our system's POS and NER labels. Along with
                    that is the user manual
                  </p>
                </div>
              </Link>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default Home;
