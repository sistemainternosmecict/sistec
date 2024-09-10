import { createContext, useState } from "react";

export const HostContext = createContext();

export const HostProvider = ({ children }) => {
    const [hostUrl, setHostUrl] = useState("http://127.0.0.1:5000")

    return (
        <HostContext.Provider value={{ hostUrl, setHostUrl }}>
            {children}
        </HostContext.Provider>
    )
}