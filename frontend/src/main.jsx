import { createRoot } from "react-dom/client";
import { ChatProvider } from "./context/ChatContext";

import "./index.css";

import App from "./App";

import { DomainProvider } from "./context/DomainContext";
import { ThemeProvider } from "./context/ThemeContext";

createRoot(document.getElementById("root")).render(
  <ThemeProvider>
    <DomainProvider>
      <ChatProvider>
        <App />
      </ChatProvider>
    </DomainProvider>
  </ThemeProvider>
);
