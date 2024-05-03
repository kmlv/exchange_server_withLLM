import React from "react";
import PropTypes from "prop-types";
import "./index.css";

export default function Order_Cards(props) {
  return (
    <div className="order-card">
      <h3>
        price: {props.price}
        quantity: {props.quantity}
        direction: {props.direction}
      </h3>
    </div>
  );
}

Order_Cards.propTypes = {
  price: PropTypes.number,
  quantity: PropTypes.number,
  direction: PropTypes.string,
};
