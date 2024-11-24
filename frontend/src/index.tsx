import React, {StrictMode} from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import {BrowserRouter} from "react-router";
import TemplateProvider from "./providers/TemplateProvider";
import FilesProvider from "./providers/FilesProvider";
import ResultsProvider from "./providers/ResultsProvider";

const root = ReactDOM.createRoot(
    document.getElementById('root') as HTMLElement
);
root.render(
    <StrictMode>
        <BrowserRouter>
            <ResultsProvider>
                <TemplateProvider>
                    <FilesProvider>
                        <App/>
                    </FilesProvider>
                </TemplateProvider>
            </ResultsProvider>
        </BrowserRouter>
    </StrictMode>,
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
