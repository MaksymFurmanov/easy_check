import {Rule} from "../../lib/definitions";
import {IoIosArrowDown} from "react-icons/io";
import {useState} from "react";
import clsx from "clsx";

export default function RuleBox({rule}: { rule: Rule }) {
    const [showCriteria, setShowCriteria] = useState<boolean>(false);

    return (
        <div className={clsx("w-full bg-white px-6 py-4 text-black text-lg", showCriteria ? "rounded-lg" : "rounded-full")}>
            <div className={"flex justify-between"}>
                <p>{rule.label}</p>
                <button onClick={() => setShowCriteria(!showCriteria)}>
                    <IoIosArrowDown/>
                </button>
            </div>
            {showCriteria &&
                <ul>
                    {rule.criteria_1 && <li>{rule.criteria_1}</li>}
                    {rule.criteria_2 && <li>{rule.criteria_2}</li>}
                    {rule.criteria_3 && <li>{rule.criteria_3}</li>}
                </ul>
            }
        </div>
    );
}