import React from "react";
import Order_Cards from "../Orders/Order_Cards";
import "./index.css";

{
  /* <h2>Orders Tracker</h2>
        {orders.map((order) => (
          <Order_Cards
            price={order.price}
            quantity={order.quantity}
            direction={order.direction}
          /> */
}

const OrderBox = ({ Orders, Title }) => {
  return (
    <div className="box">
        <h2>{Title}</h2>
      <div className="scrollable-box">
        {Orders.map((Order, index) => (
          <Order_Cards
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
