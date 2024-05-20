import React from 'react';
import './index.css'; // Import your CSS styles

// import react logo
import logo from '../../assets/react.svg';

const Header = () => {
  return (
    <header>
      <div className="logo">
        <img className = "headerImg" src={logo} alt="Centering a div" />
        <h2>Trade with LLM</h2>
      </div>
      <nav>
        <ul>
          <li><a href="https://github.com/william-siegmund/exchange_server">Github</a></li>
          <li><a href="https://www.linkedin.com/in/kristian-l-b9a38028/">Linkdin</a></li>
          <li><a href="mailto:tchen175@ucsc.edu">Contact</a></li>
        </ul>
      </nav>
    </header>
  );
};

export default Header;