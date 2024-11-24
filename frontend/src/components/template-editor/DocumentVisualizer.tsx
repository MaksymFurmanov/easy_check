import DocViewer from "react-doc-viewer";
import {useState} from "react";

type DocType = {
    uri: string;
    fileType?: string;
    fileName?: string;
};

const file = {
    uri: "https://www.vo.eu/wp-content/uploads/2021/04/S21.0161-VO-schema-Patent-Specificatie-1500px-EN-Pr2a.jpg",
    fileType: "image/jpg",
    fileName: "name"
};

export default function DocumentVisualizer() {
    const [docs, setDocs] = useState<DocType[]>([file]);

    return (
        <div className={"h-full w-1/2"}>
            <DocViewer className={"h-full rounded-lg"}
                       documents={docs}
            />
        </div>
    );
}