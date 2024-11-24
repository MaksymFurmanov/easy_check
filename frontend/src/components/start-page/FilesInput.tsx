import {ChangeEvent, Dispatch, MouseEvent, SetStateAction, useRef} from "react";
import FileItem from "./FileItem";
import { LuPlus } from "react-icons/lu";

export default function FilesInput({files, setFiles}:
                                       { files: File[] | null, setFiles: Dispatch<SetStateAction<File[] | null>> }) {
    const inputRef = useRef<HTMLInputElement>(null);

    const exampleHandler = (e: ChangeEvent<HTMLInputElement>) => {
        const filesInput = e.target.files;
        if (!filesInput) return;

        const filesArray = Array.from(filesInput);

        setFiles((prevState) => {
            if (!prevState) return [...filesArray];
            return [...prevState, ...filesArray]
        });
    }

    const initUploading = (e: MouseEvent<HTMLButtonElement, globalThis.MouseEvent>) => {
        e.preventDefault();
        if (!inputRef || !inputRef.current) return;

        inputRef.current.click();
    }

    return (
        <div className={"flex flex-col gap-2 items-center w-full mt-4"}>
            {files && files.map((file, index) =>
                <FileItem key={index}
                          file={file}
                          fileIndex={index}
                          setFiles={setFiles}
                />
            )}
            <button
                className={"bg-white mx-auto mt-4 p-2 text-black border-2 border-black rounded-full hover:bg-slate-200"}
                onClick={(e) => initUploading(e)}
            >
                <LuPlus className={"stroke-2"}/>
            </button>
            <input ref={inputRef}
                   type={"file"}
                   multiple={true}
                   hidden={true}
                   name={"files"}
                   onChange={(e) => exampleHandler(e)}
            />
        </div>
    );
}