import {ResultGroup} from "../../lib/definitions";
import { IoIosWarning } from "react-icons/io";
import { FaCheck } from "react-icons/fa6";
import { BsQuestionLg } from "react-icons/bs";

export default function ResultItem({result}: {result: ResultGroup}) {
    return (
        <div className={"flex justify-between bg-white rounded-lg mx-8 px-16 py-12 text-black"}>
            <p>{result.label}</p>
            <div className={"flex gap-4"}>
                <div>
                    <FaCheck/>
                    <p>{result.good}</p>
                </div>
                <div>
                    <BsQuestionLg/>
                    <p>{result.questionable}</p>
                </div>
                <div>
                    <IoIosWarning/>
                    <p>{result.bad}</p>
                </div>
            </div>
            <p>{result.score} %</p>
        </div>
    );
}