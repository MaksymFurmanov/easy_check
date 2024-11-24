import RulesList from "../components/template-editor/RulesList";
import DocumentVisualizer from "../components/template-editor/DocumentVisualizer";
import {useFiles} from "../providers/FilesProvider";
import {initAnalysis} from "../lib/actions";
import {useNavigate} from "react-router";

export default function TemplateEditor() {
    const navigate = useNavigate();
    const files = useFiles();

    const analyzeHandler = async () => {
        if(!files) return;
        await initAnalysis(files);
        navigate("/results");
    }

    return (
        <main className={"h-screen w-screen flex gap-8 justify-between px-10 py-6"}>
            <DocumentVisualizer/>
            <div className={"h-full w-full"}>
                <RulesList/>
                <button className={"absolute bottom-4 right-4 bg-white text-black px-8 py-2 rounded-full border-2 border-black"}
                    onClick={analyzeHandler}>
                    Next
                </button>
            </div>
        </main>
    );
}