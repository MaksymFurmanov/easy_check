import {Result, ResultGroup} from "../lib/definitions";

export default function groupResults(results: Result[]): ResultGroup[] {
    const groupsMap = new Map<
        string,
        { label: string; good: number; questionable: number; bad: number; total: number }
    >();

    results.forEach((result) => {
        if (!groupsMap.has(result.id)) {
            groupsMap.set(result.id, {
                label: result.label,
                good: 0,
                questionable: 0,
                bad: 0,
                total: 0,
            });
        }

        const group = groupsMap.get(result.id)!;

        if (result.status === 1) {
            group.good++;
        } else if (result.status === 0) {
            group.questionable++;
        } else if (result.status === -1) {
            group.bad++;
        }

        group.total++;
    });

    return Array.from(groupsMap.entries()).map(([id, group]) => ({
        id,
        label: group.label,
        good: group.good,
        questionable: group.questionable,
        bad: group.bad,
        score:  Math.round((group.good / group.total) * 100),
    }));
}