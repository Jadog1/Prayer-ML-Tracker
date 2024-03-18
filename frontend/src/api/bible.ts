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
    public start_verse: number;
    public end_verse: number;
    public text: string;
    public section_name: string;

    constructor() {
        this.book = '';
        this.chapter = 0;
        this.start_verse = 0;
        this.end_verse = 0;
        this.text = '';
        this.section_name = '';
    }

    public static fromJson(json: any): BibleSection {
        const b = new BibleSection();
        b.book = json.book;
        b.chapter = json.chapter;
        b.start_verse = json.start_verse;
        b.end_verse = json.end_verse;
        b.text = json.text;
        b.section_name = json.section_name;
        return b;
    }

    public Context(): string {
        return `${this.book} ${this.chapter}:${this.start_verse}-${this.end_verse}`;
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
        for (let obj of json) {
            switch (obj.type) {
                case 'verse':
                    b.results.push(BibleVerse.fromJson(obj));
                    break;
                case 'section':
                    b.results.push(BibleSection.fromJson(obj));
                    break;
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