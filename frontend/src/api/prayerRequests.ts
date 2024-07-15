
import { BibleResults } from './bible';
import {Contact, ContactID, Group} from './contacts';

export type PrayerRequestID = number;

class PrayerRequest {
    public account_id: number;
    public contact: Contact;
    public request: string;
    public archived_at: string;
    public link_id: number;
    public id: PrayerRequestID;
    public created_at: string;
    public updated_at: string;
    public emotion: string;
    public sentiment: string;
    public prayer_type: string;
    public links: PrayerRequest[];
    public topics: string[];

    constructor() {
        this.account_id = 0;
        this.contact = new Contact();
        this.request = '';
        this.archived_at = '';
        this.link_id = 0;
        this.id = 0;
        this.created_at = '';
        this.updated_at = '';
        this.emotion = '';
        this.sentiment = '';
        this.prayer_type = '';
        this.links = [];
        this.topics = [];
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
        p.created_at = json.created_at;
        p.updated_at = json.updated_at;
        p.emotion = json.emotion;
        p.sentiment = json.sentiment;
        p.prayer_type = json.prayer_type;
        p.topics = json.topics || [];
        return p;
    }

    async save(): Promise<PrayerRequest> {
        let method = 'POST';
        if (this.id) method = 'PUT';
        const response = await fetch('/api/prayer_requests/', {
            method: method,
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
        if (!response.ok) {
            const message = await response.text();
            throw new Error(`Failed to save: ${message}`);
        }
        const json = await response.json();
        this.id = json.id;
        return PrayerRequest.fromJson(json);
    }

    async delete (): Promise<void> {
        const response = await fetch(`/api/prayer_requests/${this.id}`, {
            method: 'DELETE',
        });
        if (!response.ok) {
            throw new Error(`Failed to delete: ${response.statusText}`);
        }
    }

    async load(id: PrayerRequestID): Promise<PrayerRequest> {
        const response = await fetch(`/api/prayer_requests/${id}`);
        if (!response.ok) {
            throw new Error(`Failed to fetch: ${response.statusText}`);
        }
        const json = await response.json();
        return PrayerRequest.fromJson(json);
    }

    async link(idTo: PrayerRequestID, idFrom:PrayerRequestID = 0): Promise<void> {
        const response = await fetch(`/api/prayer_requests/link`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                id_from: idFrom || this.id,
                id_to: idTo,
            }),
        });
        if (!response.ok) {
            throw new Error(`Failed to link: ${response.statusText}`);
        }
    }

    async getLinks(): Promise<PrayerRequest[]> {
        // GetLinks should call the endpoint with the link_id and request_id as query parameters
        const response = await fetch(`/api/prayer_requests/links?link_id=${this.link_id}&request_id=${this.id}`);
        if (!response.ok) {
            throw new Error(`Failed to fetch: ${response.statusText}`);
        }
        const json = await response.json();
        this.links = json.map((p: any) => PrayerRequest.fromJson(p));
        return this.links;
    }

}

class PrayerRequests {
    public requests: PrayerRequest[];

    constructor() {
        this.requests = [];
    }

    async getRequestsForContact(contactId: ContactID): Promise<PrayerRequest[]> {
        const response = await fetch(`/api/prayer_requests/contact/${contactId}`);
        if (!response.ok) {
            throw new Error(`Failed to fetch: ${response.statusText}`);
        }
        const json = await response.json();
        this.requests = json.map((p: any) => PrayerRequest.fromJson(p));
        return this.requests;
    }

    async getTopRequests(id: PrayerRequestID): Promise<PrayerRequests> {
        const response = await fetch(`/api/prayer_requests/similar/${id}`);
        if (!response.ok) {
            throw new Error(`Failed to fetch: ${response.statusText}`);
        }
        const json = await response.json();
        this.requests = json.map((p: any) => PrayerRequest.fromJson(p));
        return this;
    }
}

export {PrayerRequest, PrayerRequests};