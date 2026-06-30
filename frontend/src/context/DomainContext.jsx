import { createContext, useContext, useState } from "react";

const DomainContext = createContext();

export function DomainProvider({ children }) {
  const [selectedDomain, setSelectedDomain] = useState("IT Helpdesk");

  return (
    <DomainContext.Provider
      value={{
        selectedDomain,
        setSelectedDomain,
      }}
    >
      {children}
    </DomainContext.Provider>
  );
}

export function useDomain() {
  return useContext(DomainContext);
}