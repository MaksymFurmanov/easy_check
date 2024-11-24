import {createContext, Dispatch, ReactNode, SetStateAction, useContext, useState} from "react";

const FilesContext = createContext<File[] | null>(null);
const SetFilesContext = createContext<Dispatch<SetStateAction<File[]>> | null>(null);

export default function FilesProvider({children}: { children: ReactNode }) {
    const [files, setFiles] = useState<File[]>([]);

    return (
        <SetFilesContext.Provider value={setFiles}>
            <FilesContext.Provider value={files}>
                {children}
            </FilesContext.Provider>
        </SetFilesContext.Provider>
    );
}

export const useFiles = () => useContext(FilesContext);
export const useSetFiles = () => useContext(SetFilesContext);