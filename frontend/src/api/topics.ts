

type topicJson = {
    id: number;
    name: string;
}


class Topic {
    public id: number;
    public name: string;

    constructor() {
        this.id = 0;
        this.name = '';
    }

    public static fromJson(json: topicJson): Topic {
        const t = new Topic();
        t.id = json.id;
        t.name = json.name;
        return t;
    }
}

class Topics {
    public topics: Topic[];

    constructor() {
        this.topics = [];
    }

    public fromJson(json: topicJson[]): Topics {
        const t = new Topics();
        t.topics = json.map((item: topicJson) => Topic.fromJson(item));
        return t;
    }
}

type GroupedTopic = {
    name: string;
    count: number;
}

class GroupedTopics extends Topics {
    public groupedTopics: GroupedTopic[];

    constructor() {
        super();
        this.groupedTopics = [];
    }

    public fromJson(json: topicJson[]): GroupedTopics {
        const t = new GroupedTopics();
        t.topics = json.map((item: topicJson) => Topic.fromJson(item));
        return t;
    }

    TopK(k: number): GroupedTopic[] {
        // Aggregate the topics
        const topicCounts = new Map<string, number>();
        for (const topic of this.topics) {
            let count = topicCounts.get(topic.name);
            if (count === undefined) {
                count = 0;
            }
            topicCounts.set(topic.name, count + 1);
        }

        // Sort the topics by count
        const sortedTopics = Array.from(topicCounts.entries()).sort((a, b) => b[1] - a[1]);

        // Return the top k
        return sortedTopics.slice(0, k).map(([name, count]) => ({ name, count }));
    }
}

export { Topic, Topics, GroupedTopics };