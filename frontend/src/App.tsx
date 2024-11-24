import './App.css'
import {Route, Routes} from "react-router";
import StartPage from "./pages/StartForm";
import TemplateEditor from "./pages/TemplateEditor";

function App() {
    return (
        <main className={"flex justify-center items-center bg-magenta text-white min-h-screen min-w-screen"}>
            <Routes>
                <Route path="/" element={<StartPage/>} />
                <Route path="/template-editor" element={<TemplateEditor/>} />
            </Routes>
        </main>
    )
}

export default App
