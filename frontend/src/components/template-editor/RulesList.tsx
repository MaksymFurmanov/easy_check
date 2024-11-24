import {useState} from "react";
import RuleBox from "./RuleBox";
import {Rule} from "../../lib/definitions";
import {rulesData} from "../../lib/placeholders";

export default function RulesList() {
    const [rules, setRules] = useState<Rule[]>(rulesData);

    const changeRules = (value: string, index: number, criterion: 1 | 2 | 3) => {
        setRules(prevState => prevState.map((rule, i) => {
            if(i === index) {
                switch (criterion) {
                    case 1:
                        return {...rule, criteria_1: value}
                    case 2:
                        return {...rule, criteria_2: value}
                    case 3:
                        return {...rule, criteria_3: value}
                    default:
                        return rule
                }
            }
            return rule;
        }));
    }

    return (
        <div className={"flex flex-col gap-6"}>
            {rules &&
                rules.map((rule, index) =>
                    <RuleBox key={index}
                             rule={rule}
                             index={index}
                             changeRules={changeRules}
                    />
                )
            }
        </div>
    );
}