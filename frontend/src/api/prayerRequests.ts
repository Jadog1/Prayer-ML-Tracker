
import {Contact, ContactID, Group} from './contacts';

export type PrayerRequestID = number;

class PrayerRequest {
    public account_id: number;
    public contact: Contact;
    public request: string;
    public archived_at: string;
    public link_id: number;
    public id: PrayerRequestID;

    constructor() {
        this.account_id = 0;
        this.contact = new Contact();
        this.request = '';
        this.archived_at = '';
        this.link_id = 0;
        this.id = 0;
    }

    public static fromJson(json: any): PrayerRequest {
        const p = new PrayerRequest();
        p.account_id = json.account_id;
        let contact = new Contact();
        let group = new Group();
        if (json.contact.group) {
            group.account_id = json.contact.group.account_id;
            group.name = json.contact.group.name;
            group.id = json.contact.group.id;
        }

        contact.account_id = json.account_id;
        contact.name = json.contact.name;
        contact.id = json.contact.id;
        contact.group = group;

        p.contact = contact;
        p.request = json.request;
        p.archived_at = json.archived_at;
        p.link_id = json.link_id;
        p.id = json.id;
        return p;
    }

    async save(): Promise<void> {
        const response = await fetch('/api/prayer_requests', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                account_id: this.account_id,
                request: this.request,
                archived_at: this.archived_at,
                link_id: this.link_id,
                id: this.id,
                contact: this.contact,
            }),
        });
        const json = await response.json();
        this.id = json.id;
    }

    async delete (): Promise<void> {
        await fetch(`/api/prayer_requests/${this.id}`, {
            method: 'DELETE',
        });
    }
}

class PrayerRequests {
    public requests: PrayerRequest[];

    constructor() {
        this.requests = [];
    }

    async getRequestsForContact(contactId: number): Promise<PrayerRequest[]> {
        const response = await fetch(`/api/prayer_requests/contact/${contactId}`);
        const json = await response.json();
        this.requests = json.map((p: any) => PrayerRequest.fromJson(p));
        return this.requests;
    }

    async getTopRequests(id: PrayerRequestID): Promise<PrayerRequests> {
        const response = await fetch(`/api/prayer_requests/similar/${id}`);
        const json = await response.json();
        this.requests = json.map((p: any) => PrayerRequest.fromJson(p));
        return this;
    }
}

export {PrayerRequest, PrayerRequests};