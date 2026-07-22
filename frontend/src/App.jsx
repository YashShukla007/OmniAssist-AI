import { HashRouter, Navigate, Route, Routes } from "react-router-dom";

import AuthFlow from "./pages/AuthFlow";
import Dashboard from "./pages/Dashboard";
import LandingPage from "./pages/LandingPage";

function PublicRoute({ children }) {
  return localStorage.getItem("omniassist_token") ? <Navigate to="/dashboard" replace /> : children;
}

function App() {
  return (
    <HashRouter>
      <Routes>
        <Route path="/" element={<PublicRoute><LandingPage /></PublicRoute>} />
        <Route path="/login" element={<PublicRoute><AuthFlow mode="login" /></PublicRoute>} />
        <Route path="/register" element={<PublicRoute><AuthFlow mode="register" /></PublicRoute>} />
        <Route path="/role" element={<PublicRoute><AuthFlow mode="role" /></PublicRoute>} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </HashRouter>
  );
}

export default App;
