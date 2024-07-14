import { PrayerRequestID } from "./prayerRequests";

class BibleVerse {
    public book: string;
    public chapter: number;
    public verse: number;
    public text: string;

    constructor() {
        this.book = '';
        this.chapter = 0;
        this.verse = 0;
        this.text = '';
    }

    public static fromJson(json: any): BibleVerse {
        const b = new BibleVerse();
        b.book = json.book;
        b.chapter = json.chapter;
        b.verse = json.verse;
        b.text = json.text;
        return b;
    }

    public Context(): string {
        return `${this.book} ${this.chapter}:${this.verse}`;
    }

    public Text(): string {
        return this.text;
    }
}

class BibleSection {
    public book: string;
    public chapter: number;
    public verse_start: number;
    public verse_end: number;
    public text: string;
    public section_name: string;

    constructor() {
        this.book = '';
        this.chapter = 0;
        this.verse_start = 0;
        this.verse_end = 0;
        this.text = '';
        this.section_name = '';
    }

    public static fromJson(json: any): BibleSection {
        const b = new BibleSection();
        b.book = json.book;
        b.chapter = json.chapter;
        b.verse_start = json.verse_start;
        b.verse_end = json.verse_end;
        b.text = json.text;
        b.section_name = json.section_name;
        return b;
    }

    public Context(): string {
        if (this.verse_end) 
            return `${this.book} ${this.chapter}:${this.verse_start}-${this.verse_end}`;
        else
            return `${this.book} ${this.chapter}:${this.verse_start}`;
    }

    public Text(): string {
        return this.text;
    }
}

export interface bibleResults {
    Context: () => string;
    Text: () => string;
}

class BibleResults {
    public results: bibleResults[];

    constructor() {
        this.results = [];
    }

    public static fromJson(json: any): BibleResults {
        const b = new BibleResults();
        let topics = json.topics ? json.topics : json;
        for (let obj of topics) {
            switch (obj.type) {
                case 'verse':
                    b.results.push(BibleVerse.fromJson(obj));
                    break;
                case 'section':
                    b.results.push(BibleSection.fromJson(obj));
                    break;
                case 'verses':

                default:
                    console.error('Unknown type: ' + obj.type);
                    break;
            }
        }
        return b;
    }
 
    async getTopBibleVerses(id: PrayerRequestID): Promise<BibleResults> {
        const response = await fetch(`/api/prayer_requests/similar/bible/${id}`);
        if (!response.ok) {
            throw new Error(`Failed to fetch: ${response.statusText}`);
        }
        const json = await response.json();
        return BibleResults.fromJson(json);
    }
}

export { BibleVerse, BibleSection, BibleResults };