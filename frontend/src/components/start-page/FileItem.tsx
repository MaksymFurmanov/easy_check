import {RxCross2} from "react-icons/rx";
import {Dispatch, SetStateAction} from "react";

export default function FileItem({file, fileIndex, setFiles}: {
    file: File,
    fileIndex: number,
    setFiles: Dispatch<SetStateAction<File[] | null>>
}) {
    const deleteHandler = () => {
        setFiles(prevState => {
            if (!prevState) return prevState;
            return [...prevState.filter((_, index) => index !== fileIndex)];
        });
    }

    return (
        <div className={"bg-white flex justify-between px-4 py-1 w-full text-black text-lg border border-black rounded-lg"}>
            <p>{file.name}</p>
            <button onClick={deleteHandler}>
                <RxCross2/>
            </button>
        </div>
    );
}