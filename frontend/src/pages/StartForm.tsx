import {useState, FormEvent} from "react";
import TemplateInput from "../components/start-page/TemplateInput";
import FilesInput from "../components/start-page/FilesInput";
import {submitFiles} from "../lib/actions";
import {useNavigate} from "react-router";
import {useTemplate} from "../providers/TemplateProvider";
import {useFiles} from "../providers/FilesProvider";

export default function StartForm() {
    const files = useFiles();
    const template = useTemplate();
    const [isPending, setIsPending] = useState<boolean>(false);

    const navigate = useNavigate();

    const submitHandler = async (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setIsPending(true);
        if (!template) return;
        const res = await submitFiles(template);
        console.log(res)
        navigate("/template-editor");
    }

    return (
        <form onSubmit={(e) => submitHandler(e)}>
            <div className={"min-w-72 h-fit mx-auto px-40 py-10 border-2 border-black rounded-lg"}>
                <h1 className={"text-3xl text-center"}>
                    Easy check
                </h1>
                <h2 className={"mt-4 text-lg text-center"}>
                    Check documents data easier with AI
                </h2>
                <TemplateInput />
                {template ? <FilesInput /> : null}
                {files && <RedirectButton/>}
            </div>
        </form>
    );
}

function RedirectButton() {

    return (
        <button
            className={"bg-white w-full mt-6 px-3 py-1 text-black text-xl border-2 border-black rounded-full hover:bg-slate-200"}
            type={"submit"}
        >
            Next
        </button>
    );
}