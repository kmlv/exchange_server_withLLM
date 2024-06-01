# React + Vite 

**NOTE:** 

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.
Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react/README.md) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

# Deployment

## Run Method \# 1: Run with Docker
See exchange_serve/README.md

## Run Method \# 2: Run locally
```bash
npm run dev
```


# Development Information

**Folder: /user-interface/src**

- Contains `App.jsx, App.css` contains overall configuration of design components.

**Folder: /user-interface/src/Components**

- Contains `/OrderBox` stores style (`index.css`) and functional (`OrderBox.jsx`) elements of the scrollable boxes to hold live order cards.
- Contains `/Orders` stores style (`index.css`) and functional (`OrderCard.jsx`) elements of the live order cards.

**Folder: /user-interface/src/sections**

- Contains `/ClientOrders` stores style (`index.css`) and functional (`ClientOrders.jsx`) elements of the user's data presentation. This is where the market's order book is fetched for the frontend.
- Contains `/header` stores style (`index.css`) and functional (`Header.jsx`) elements of the UI's header bar.
- Contains `/PromptInput` stores style (`index.css`) and functional (`PromptInput.jsx`) elements of the user's chatbox interaction with the LLM.

# Recommended Improvements

- Instead of http protocol for making API calls, the UI could benefit from using web sockets. Currently,  keeping the UI up to date in live time with the market's features is done by refreshing on a fixed 3 second loop.
