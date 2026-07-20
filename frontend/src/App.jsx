import { HashRouter, Navigate, Route, Routes } from "react-router-dom";

import AuthFlow from "./pages/AuthFlow";
import Dashboard from "./pages/Dashboard";
import LandingPage from "./pages/LandingPage";

function App() {
  return (
    <HashRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<AuthFlow mode="login" />} />
        <Route path="/register" element={<AuthFlow mode="register" />} />
        <Route path="/role" element={<AuthFlow mode="role" />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </HashRouter>
  );
}

export default App;
