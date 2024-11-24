import {RxCross2} from "react-icons/rx";
import {useSetFiles} from "../../providers/FilesProvider";

export default function FileItem({file, fileIndex}: {
    file: File,
    fileIndex: number
}) {
    const setFiles = useSetFiles();

    const deleteHandler = () => {
        if(!setFiles) return;
        setFiles(prevState => {
            if (!prevState) return prevState;
            return [...prevState.filter((_, index) => index !== fileIndex)];
        });
    }

    return (
        <div
            className={"bg-white flex justify-between px-4 py-1 w-full text-black text-lg border border-black rounded-lg"}>
            <p>{file.name}</p>
            <button onClick={deleteHandler}>
                <RxCross2/>
            </button>
        </div>
    );
}