import {useState} from "react";
import RuleBox from "./RuleBox";
import {Rule} from "../../lib/definitions";
import {criteriaData} from "../../lib/placeholders";

export default function RulesList() {
    const [rules, setRules] = useState<Rule[]>(criteriaData);

    return (
        <div className={"h-full w-full flex flex-col gap-6"}>
            {rules &&
                rules.map((rule, index) =>
                    <RuleBox key={index} rule={rule}/>)
            }
        </div>
    );
}