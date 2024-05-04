// OrdersTracker.js
import React, { useState, useEffect } from "react";
import Order_Cards from "../../Components/Orders/Order_Cards";

const Client_orders = () => {
  const [orders, setOrders] = useState([]);
  const [balance, setBalance] = useState(0);
  const [shares, setShares] = useState(0);

  // Fetch orders from the API endpoint
  const fetchOrders = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5001/client_orders");
      if (!response.ok) {
        throw new Error("Failed to fetch orders");
      }
      const data = await response.json();

      console.log(data.balance);
      console.log(data.shares);
      return data; // Assuming the API response has an "orders" field containing the list of orders
    } catch (error) {
      console.error("Error fetching orders:", error);
      return [];
    }
  };
  // jsonify({"balance": balance, "shares": shares, "orders": orders_list})
  useEffect(() => {
    const interval = setInterval(() => {
      fetchOrders().then((newOrders) => {
        setOrders(newOrders.orders);
        setBalance(newOrders.balance);
        setShares(newOrders.shares);
      });
    }, 10000); // Update every second (adjust as needed)

    return () => clearInterval(interval);
  }, []); // Empty dependency array means run once on mount

  return (
    <>
      <div>Balance: {balance}</div>
      <div>Shares: {shares}</div>
      <div className="orders-tracker">
        <h2>Orders Tracker</h2>
        {orders.map((order) => (
          <Order_Cards
            price={order.price}
            quantity={order.quantity}
            direction={order.direction}
          />
        ))}
      </div>
    </>
  );
};

export default Client_orders;
