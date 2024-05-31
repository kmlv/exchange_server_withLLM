import React from "react";
import PropTypes from "prop-types";
import "./index.css";

/**
   * An order card compenent that displays the price and quantity of an order
   * @param {number} price - the price of the order
   * @param {number} quantity - the quantity of the order
   * @param {string} direction - the direction of the order (either "B" or "S")
   * @param {boolean} best_price - a boolean value that determines if the order is the best buy or sell order
   * @returns {JSX.Element} - The card component
  */

export default function OrderCard(props) {

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

      {/* Displays what kind of order it is */}
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

OrderCard.propTypes = {
  price: PropTypes.number,
  quantity: PropTypes.number,
  direction: PropTypes.string,
  best_price: PropTypes.bool,
};
