import {useState} from "react";
import {ResultGroup} from "../lib/definitions";
import ResultItem from "../components/results/ResultItem";
import {resultGroupsData} from "../lib/placeholders";

export default function Results() {
    const [results, setResults] = useState<ResultGroup[]>(resultGroupsData);

    return (
        <main className={"w-full flex flex-col gap-6"}>
            {results.map((result, index) =>
                <ResultItem key={index} result={result}/>
            )}
        </main>
    );
}