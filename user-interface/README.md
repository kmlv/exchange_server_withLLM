# React + Vite 

# Deployment

## Run Method \# 1: Run with Docker
See exchange_serve/README.md

## Run Method \# 2: Run locally
```bash
npm run dev
```


# Development Information

**Folder: /user-interface/src**

- Contains `App.jsx, App.css` manages overall configuration of design components.

**Folder: /user-interface/src/Components**

- Contains `/OrderBox` stores style (index.css) and functional (OrderBox.jsx) elements of the scrollable boxes to hold live order cards.
- Contains `/Orders` stores style (index.css) and functional (OrderCard.jsx) elements of the live order cards.

**Folder: /user-interface/src/sections**

- Contains `/ClientOrders` 
- Contains `/header` 
- Contains `/PromptInput` 


# API Endpoints


# Recommended Improvements

- we should’ve used web sockets over the http protocol for APIs, When we are trying to update the stock market live, its one a 3 second loop of get_market




This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react/README.md) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh
