import { Contact } from "./contacts";
import { PrayerRequest } from "./prayerRequests";

type prayerSummaryJson = {
    prayers: PrayerRequest[];
}

class PrayerSummary {
    public prayers: PrayerRequest[];

    constructor() {
        this.prayers = [];
    }

    public static fromJson(json: prayerSummaryJson): PrayerSummary {
        const ps = new PrayerSummary()
        ps.prayers = json.prayers.map((item: PrayerRequest) => PrayerRequest.fromJson(item));
        return ps;
    }

    public static async load(date_from: string, date_to: string, group_id?: number): Promise<PrayerSummary> {
        const response = await fetch('/api/prayer_requests/summary', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                date_from: date_from,
                date_to: date_to,
                group_id: group_id,
            }),
        });
        const json = await response.json();

        if (!response.ok) {
            const message = await response.text();
            throw new Error(`Failed to load: ${message}`);
        }

        return PrayerSummary.fromJson(json);
    }

}

export { PrayerSummary };