import {ChangeEvent, Dispatch, MouseEvent, RefObject, SetStateAction, useRef} from "react";

export default function TemplateFileInput({template, setTemplate}:
                                             { template: File | null, setTemplate: Dispatch<SetStateAction<File | null>> }) {
    const inputRef = useRef<HTMLInputElement>(null);

    const exampleHandler = (e: ChangeEvent<HTMLInputElement>) => {
        const files = e.target.files;
        if (!files) return;

        const file = files[0];

        setTemplate(file);
    }

    return (
        <div className={"flex mt-12 gap-4 justify-center items-center"}>
            <label className={"text-xl"}>
                Form example:
            </label>
            <UploadingButton example={template} inputRef={inputRef}/>
            <input ref={inputRef}
                   type={"file"}
                   name={"template"}
                   hidden={true}
                   onChange={(e) => exampleHandler(e)}
            />
        </div>
    );
}

function UploadingButton({example, inputRef}: {
    example: File | null,
    inputRef: RefObject<HTMLInputElement>
}) {
    const initUploading = (e: MouseEvent<HTMLButtonElement, globalThis.MouseEvent>) => {
        e.preventDefault();
        if (!inputRef || !inputRef.current) return;

        inputRef.current.click();
    }

    return (
        <button
            className={"bg-white w-fit px-6 py-1 text-black border-2 border-black rounded-full hover:bg-slate-200"}
            onClick={(e) => initUploading(e)}
        >
            {example ? example.name : "Upload example file"}
        </button>
    );
}