import React, { useState, useEffect } from "react";
import OrderBox from "../../Components/OrderBox/OrderBox";
import "./index.css";
/**
 * The Client Orders section displays the client's
 * orders, balance, shares, and the order book(market buy and sell orders)
 */

const ClientOrders = () => {
  const [orders, setOrders] = useState([]);
  const [balance, setBalance] = useState(1000);
  const [shares, setShares] = useState(100);

  const [order_book_sell, setSellOrders] = useState([]);
  const [order_book_buy, setBuyOrders] = useState([]);

  var client_addr = import.meta.env.VITE_API_URL;
  if (import.meta.env.VITE_API_URL === undefined) {
    client_addr = "http://127.0.0.1:5001";
  }

  // Fetch the client's orders from the client endpoint
  const fetchClientOrders = async () => {
    try {
      const response = await fetch(client_addr + "/client_orders");
      if (!response.ok) {
        throw new Error("Failed to fetch orders");
      }

      const data = await response.json();
      return data; // Example return value: {balance: 1000, shares: 100, orders: [{price: 100, quantity: 10, direction: "B"}]}
    } catch (error) {
      console.error("Error fetching orders:", error);
      throw error;
    }
  };

  // Fetches the market order from the client endpoint
  const fetchOrderBook = async () => {
    try {
      const response = await fetch(client_addr + "/order_book");
      const data = await response.json();

      return data;
    } catch (error) {
      console.error("Error fetching orders:", error);
    }
  };

  // Updates client orders and market orders every 3 seconds
  useEffect(() => {

    // Updates the client orders by fetching the client orders
    const updateClientOrders = async () => {
      try {
        const newClientOrders = await fetchClientOrders();
        setOrders(newClientOrders.orders);
        setBalance(newClientOrders.balance);
        setShares(newClientOrders.shares);
      } catch (error) {
        console.error("Error fetching client data:", error);
      }
    };

    // Updates the market orders by fetching the market orders
    const updateMarketOrders = async () => {
      try {
        const newMarketOrders = await fetchOrderBook();
        setSellOrders(newMarketOrders.asks);
        setBuyOrders(newMarketOrders.bids);
      } catch (error) {
        console.error("Error fetching market data:", error);
      }
    };

    // Update the client orders and market orders every 3 seconds
    const interval = setInterval(() => {
      updateClientOrders();
      updateMarketOrders();
    }, 3000); // 3 seconds

    // Clear the interval when the component is unmounted
    return () => clearInterval(interval);
  }, []);

  return (
    <>
      <div className="order-tracker-container">
        {/* Display the client's balance and shares */}
        <div className="user-data-container">
          <div className="user-data-title">Your Info:</div>
          <div>Balance: {balance}</div>
          <div>Shares: {shares}</div>
        </div>

        {/* Display the client's orders and the market orders */}
        <div>
          <OrderBox Orders={orders} Title="Your Orders" />
        </div>

        <div>
          <OrderBox Orders={order_book_buy} Title="Market Buy orders" />
        </div>

        <div>
          <OrderBox Orders={order_book_sell} Title="Market Sell orders" />
        </div>
      </div>
    </>
  );
};

export default ClientOrders;
