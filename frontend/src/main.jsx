import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { ChatProvider } from "./context/ChatContext";

import "./index.css";

import App from "./App";

import { DomainProvider } from "./context/DomainContext";

createRoot(document.getElementById("root")).render(
  <DomainProvider>
    <ChatProvider>
      <App />
    </ChatProvider>
  </DomainProvider>
);