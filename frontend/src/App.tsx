import './App.css'
import {Route, Routes} from "react-router";
import StartPage from "./pages/StartPage";

function App() {

    return (
        <main>
            <Routes>
                <Route path="/" element={<StartPage/>} />
            </Routes>
        </main>
    )
}

export default App
