import {ChangeEvent, Dispatch, SetStateAction, MouseEvent, useRef, useState} from "react";

export default function StartPage() {
    const [showFilesInput, setShowFilesInput] = useState<boolean>(false);

    return (
        <main>
            <ExampleFileInput setShowFilesInput={setShowFilesInput}/>
            {showFilesInput ? <FilesInput/> : null}
            <button>
                Next
            </button>
        </main>
    );
}

function ExampleFileInput({setShowFilesInput}:
                              { setShowFilesInput: Dispatch<SetStateAction<boolean>> }) {
    const inputRef = useRef<HTMLInputElement>(null);
    const [example, setExample] = useState<File | null>(null);

    const exampleHandler = (e: ChangeEvent<HTMLInputElement>) => {
        const files = e.target.files;
        if (!files) return;

        const file = files[0];

        setExample(file);

        setShowFilesInput(true);
    }

    const initUploading = (e: MouseEvent<HTMLButtonElement, globalThis.MouseEvent>) => {
        e.preventDefault();
        if (!inputRef || !inputRef.current) return;

        inputRef.current.click();
    }

    return (
        <div className={""}>
            <label>Form example</label>
            <button className={""}
                    onClick={(e) => initUploading(e)}
            >
                {example ? example.name : "Upload example file"}
            </button>
            <input ref={inputRef}
                   type={"file"}
                   hidden={true}
                   onChange={(e) => exampleHandler(e)}
            />
        </div>
    );
}

function FilesInput() {
    return (
        <div>

        </div>
    );
}