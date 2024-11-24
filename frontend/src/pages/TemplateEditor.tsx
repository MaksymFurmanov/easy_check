import RulesList from "../components/template-editor/RulesList";
import DocumentVisualizer from "../components/template-editor/DocumentVisualizer";

export default function TemplateEditor() {

    return (
        <main className={"h-screen w-screen flex gap-8 justify-between px-10 py-6"}>
            <DocumentVisualizer/>
            <RulesList/>
        </main>
    );
}