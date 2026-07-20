import { createContext, useContext, useState } from "react";

const DomainContext = createContext();

export function DomainProvider({ children }) {
  const [selectedDomain, setSelectedDomain] = useState("Healthcare");
  const selectIntegratedDomain = (domain) => {
    if (domain === "Healthcare") setSelectedDomain("Healthcare");
  };

  return (
    <DomainContext.Provider
      value={{
        selectedDomain,
        setSelectedDomain: selectIntegratedDomain,
      }}
    >
      {children}
    </DomainContext.Provider>
  );
}

// eslint-disable-next-line react-refresh/only-export-components
export function useDomain() {
  return useContext(DomainContext);
}
