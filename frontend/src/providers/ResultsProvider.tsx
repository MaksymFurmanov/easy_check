import {createContext, Dispatch, ReactNode, SetStateAction, useCallback, useContext, useState} from "react";
import {Result} from "../lib/definitions";
import groupResults from "../utils/groupResults";

const ResultsContext = createContext<Result[] | null>(null);
const SetResultsContext = createContext<Dispatch<SetStateAction<Result[]>> | null>(null);
const ResultsGroupedContext = createContext([]);

export default function ResultsProvider({children}: { children: ReactNode }) {
    const [results, setResults] = useState<Result[]>([]);

    const resultsGrouped = useCallback(() => {
        if(results) return [];
        return groupResults(results);
    }, [results]);

    return (
        // @ts-ignore
        <ResultsGroupedContext.Provider value={resultsGrouped}>
            <SetResultsContext.Provider value={setResults}>
                <ResultsContext.Provider value={results}>
                    {children}
                </ResultsContext.Provider>
            </SetResultsContext.Provider>
        </ResultsGroupedContext.Provider>
    );
}

export const useResults = () => useContext(ResultsContext);
export const useSetResults = () => useContext(SetResultsContext);
export const useGroupedResults = () => useContext(ResultsGroupedContext);