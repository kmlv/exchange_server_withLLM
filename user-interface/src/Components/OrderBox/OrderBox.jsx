import React from "react";
import OrderCard from "../Orders/OrderCard";
import "./index.css";

/**
 * A box component that displays a list of order cards
 * 
 * @param {Object[]} Orders - A list of orders cards to display
 * @param {string} Title - The title of the box
 * @returns {JSX.Element} - The box component
 */

const OrderBox = ({ Orders, Title }) => {
  return (
    <div className="box">
        <h2>{Title}</h2>
      <div className="scrollable-box">
        {Orders.map((Order, index) => (
          <OrderCard
            key={index}
            price={Order.price}
            quantity={Order.quantity}
            direction={Order.direction}
            best_price = {index === 0} 
          />
        ))}
      </div>
    </div>
  );
};

export default OrderBox;
