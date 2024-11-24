import {Rule} from "../../lib/definitions";
import {IoIosArrowDown} from "react-icons/io";
import {useState} from "react";
import clsx from "clsx";

export default function RuleBox({rule, index, changeRules}: {
    rule: Rule,
    index: number,
    changeRules: (value: string, index: number, criterion: 1 | 2 | 3) => void
}) {
    const [showCriteria, setShowCriteria] = useState<boolean>(false);

    return (
        <div
            className={clsx("w-full bg-white px-6 py-4 text-black text-lg ", showCriteria ? "rounded-3xl" : "rounded-full")}>
            <div className={"flex justify-between"}>
                <p>{rule.label}</p>
                <button onClick={() => setShowCriteria(!showCriteria)}>
                    <IoIosArrowDown/>
                </button>
            </div>
            {showCriteria &&
                <ul className="mt-2 ml-6 list-disc pl-5">
                    {rule.criteria_1 &&
                        <li>
                            <input onChange={(e) => changeRules(e.target.value, index, 1)}
                                   value={rule.criteria_1}
                            />
                        </li>
                    }
                    {rule.criteria_2 &&
                        <li>
                            <input onChange={(e) => changeRules(e.target.value, index, 2)}
                                   value={rule.criteria_2}
                            />
                        </li>
                    }
                    {rule.criteria_3 &&
                        <li>
                            <input onChange={(e) => changeRules(e.target.value, index, 3)}
                                   value={rule.criteria_3}
                            />
                        </li>
                    }
                </ul>
            }
        </div>
    );
}