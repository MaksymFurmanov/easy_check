import {createContext, Dispatch, ReactNode, SetStateAction, useContext, useState} from "react";

const TemplateContext = createContext<File | null>(null);
const SetTemplateContext = createContext<Dispatch<SetStateAction<File | null>> | null>(null);

export default function TemplateProvider({children}: { children: ReactNode }) {
    const [template, setTemplate] = useState<File | null>(null);

    return (
        <SetTemplateContext.Provider value={setTemplate}>
            <TemplateContext.Provider value={template}>
                {children}
            </TemplateContext.Provider>
        </SetTemplateContext.Provider>
    );
}

export const useTemplate = () => useContext(TemplateContext);
export const useSetTemplate = () => useContext(SetTemplateContext);