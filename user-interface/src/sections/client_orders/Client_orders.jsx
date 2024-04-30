// OrdersTracker.js
import React, { useState, useEffect } from "react";
import Order_Cards from "../../Components/Orders/Order_Cards";

const Client_orders = () => {
  const [orders, setOrders] = useState([]);

  // Fetch orders from the API endpoint
  const fetchOrders = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/client_orders");
      if (!response.ok) {
        throw new Error("Failed to fetch orders");
      }
      const data = await response.json();
      return data.orders; // Assuming the API response has an "orders" field containing the list of orders
    } catch (error) {
      console.error("Error fetching orders:", error);
      return [];
    }
  };
  // jsonify({"balance": balance, "shares": shares, "orders": orders_list})
  useEffect(() => {
    const interval = setInterval(() => {
      fetchOrders().then((newOrders) => {
        setOrders(newOrders);
      });
    }, 10000); // Update every second (adjust as needed)

    return () => clearInterval(interval);
  }, []); // Empty dependency array means run once on mount

  return (
    <div className="orders-tracker">
      <h2>Orders Tracker</h2>
      {orders.map((order) => (
        <Order_Cards
          key={order.order_num} // Use a unique key for each order card
          order_num={order.order_num}
          price={order.price}
          quantity={order.quantity}
          direction={order.direction}
        />
      ))}
    </div>
  );
};

export default Client_orders;
