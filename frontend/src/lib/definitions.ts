export type Rule = {
    label: string;
    criteria_1: string;
    criteria_2?: string;
    criteria_3?: string;
}

export type Result = {
    id: string;
    label: string;
    value: string;
    status: -1 | 0 | 1
}

export type ResultGroup = {
    id: string;
    label: string;
    good: number;
    questionable: number;
    bad: number;
    score: number;
}