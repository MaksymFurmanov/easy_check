import {Result, ResultGroup, Rule} from "./definitions";
import groupResults from "../utils/groupResults";

export const rulesData: Rule[] = [
    {
        label: "Name",
        criteria_1: "should be name",
        criteria_2: "should be name",
        criteria_3: "should be name",
    },
    {
        label: "Surname",
        criteria_1: "should be surname",
        criteria_2: "should be surname",
        criteria_3: "should be surname",
    },
    {
        label: "Date_of_birth",
        criteria_1: "should be date of birth",
        criteria_2: "should be date of birth",
        criteria_3: "should be date of birth",
    }
];

export const resultsData: Result[] = [
    {
        id: "1",
        label: "name",
        value: "ddd",
        status: -1
    },
    {
        id: "1",
        label: "surname",
        value: "ddd",
        status: 0
    },
    {
        id: "1",
        label: "Date_of_birth",
        value: "ddd",
        status: 1
    },
    {
        id: "2",
        label: "Name",
        value: "ddd",
        status: -1
    },
    {
        id: "2",
        label: "surname",
        value: "ddd",
        status: 0
    },
    {
        id: "2",
        label: "Date_of_birth",
        value: "ddd",
        status: 1
    },
];

export const resultGroupsData = groupResults(resultsData);