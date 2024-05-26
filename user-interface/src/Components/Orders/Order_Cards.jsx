import React from "react";
import PropTypes from "prop-types";
import "./index.css";

export default function Order_Cards(props) {

  // Different styles depending on sell and buy order
  const cardClassName =
    props.direction === "B"
      ? "buy-card"
      : props.direction === "S"
      ? "sell-card"
      : props.best_price
      ? "best-price-card"
      : "";
  
  
  
    
  return (
    <div className={cardClassName}>

      <h3>{props.direction === "B" ? "Buy Order" : props.direction === "S"
      ? "Sell Order": ""}</h3>
      <div className = "container">
        <h4>
          price: {props.price}
        </h4>
        <h4>
          quantity: {props.quantity}
        </h4>
      </div>
    </div>
  );
}

Order_Cards.propTypes = {
  price: PropTypes.number,
  quantity: PropTypes.number,
  direction: PropTypes.string,
  best_price: PropTypes.bool,
};
