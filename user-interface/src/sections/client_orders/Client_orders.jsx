// OrdersTracker.js
import React, { useState, useEffect } from "react";
import OrderBox from "../../Components/OrderBox/OrderBox";
import "./index.css";

const Client_orders = () => {
  const [orders, setOrders] = useState([]);
  const [balance, setBalance] = useState(0);
  const [shares, setShares] = useState(0);

  const [order_book_sell, setSellOrders] = useState([]);
  const [order_book_buy, setBuyOrders] = useState([]);


  var client_addr = import.meta.env.VITE_API_URL 
  if (import.meta.env.VITE_API_URL === undefined) 
  {
    client_addr = "http://127.0.0.1:5001";
  }
  



  // Fetch orders from the API endpoint
  const fetchOrders = async () => {
    try {
      const response = await fetch(client_addr + "/client_orders");
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


  const fetch_order_book = async () => {

    try {
      const response = await fetch(client_addr + "/order_book");

      const data = await response.json();

      setSellOrders(data.asks);
      setBuyOrders(data.bids);
      
    } catch(error) {
      console.error("Error fetching orders:", error);
    }
  }

  // jsonify({"balance": balance, "shares": shares, "orders": orders_list})
  useEffect(() => {
    const interval = setInterval(() => {
      fetchOrders().then((newOrders) => {
        setOrders(newOrders.orders);
        setBalance(newOrders.balance);
        setShares(newOrders.shares);
      });
    }, 3000); // Update every second (adjust as needed)

    return () => clearInterval(interval);
  }, []); // Empty dependency array means run once on mount

  

  return (
    <>
      
      <div className="order-tracker-container">
        <div className="user-data-container">
          <div className="user-data-title">Your Info:</div>
          <div>Balance: {balance}</div>
          <div>Shares: {shares}</div>
        </div>
        <div>
          <OrderBox Orders={orders} Title = "Your Orders"/>
        </div>

        <div>
          <OrderBox Orders={order_book_buy} Title = "Market Buy orders"/>
        </div>

        <div>
         <OrderBox Orders={order_book_sell} Title = "Market Sell orders"/>
        </div>
      </div>
      
      <div className="button-container">
        <button onClick={fetch_order_book}>
          <div className="button-text">Fetch Order Book</div>
        </button>
      </div>
    </>
  );
};

export default Client_orders;
