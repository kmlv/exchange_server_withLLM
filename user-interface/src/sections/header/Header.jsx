import React from "react";
import "./index.css"; // Import your CSS styles

// import a logo
import logo from "../../assets/react.svg";

// The Header section displays the header of the website.
const Header = () => {
  return (
    <header>
      <div className="logo">
        <img className="header-image" src={logo} alt="insert img" />
        <h2>Trade with LLM</h2>
      </div>

      <nav>
        <ul>
          <li>
            <a href="https://github.com/william-siegmund/exchange_server">
              Github
            </a>
          </li>
          <li>
            <a href="https://www.linkedin.com/in/kristian-l-b9a38028/">
              Linkedin
            </a>
          </li>
          <li>
            <a href="mailto:tchen175@ucsc.edu">Contact</a>
          </li>
        </ul>
      </nav>
    </header>
  );
};

export default Header;
