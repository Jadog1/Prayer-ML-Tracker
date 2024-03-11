
export type ContactID = number;
export type GroupID = number;

class Contact {
    public account_id: number;
    public name: string;
    public group: Group;
    public id: ContactID;

    constructor() {
        this.account_id = 0;
        this.name = '';
        this.group = new Group();
        this.id = 0;
    }

    public static fromJson(json: any): Contact {
        const c = new Contact();
        c.account_id = json.account_id;
        c.name = json.name;
        let group = new Group();
        group.account_id = json.group.account_id;
        group.name = json.group.name;
        group.id = json.group.id;
        c.group = group;
        c.id = json.id;
        return c;
    }

    async save(): Promise<void> {
        const response = await fetch('/api/contacts', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                account_id: this.account_id,
                name: this.name,
                group: this.group,
                id: this.id,
            }),
        });
        const json = await response.json();
        this.id = json.id;
    }

    async delete(): Promise<void> {
        await fetch(`/api/contacts/${this.id}`, {
            method: 'DELETE',
        });
    }

}

class Contacts {
    public contacts: Contact[];

    constructor() {
        this.contacts = [];
    }

    async all(): Promise<Contacts> {
        const response = await fetch('/api/contacts/');
        const json = await response.json();
        this.contacts = json.map((c: any) => Contact.fromJson(c));
        return this;
    }
}

class Group {
    public account_id: number;
    public name: string;
    public id: GroupID;

    constructor() {
        this.account_id = 0;
        this.name = '';
        this.id = 0;
    }

    public static fromJson(json: any): Group {
        const g = new Group();
        g.account_id = json.account_id;
        g.name = json.name;
        g.id = json.id;
        return g;
    }

    async save(): Promise<void> {
        const response = await fetch('/api/contacts/group', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                account_id: this.account_id,
                name: this.name,
                id: this.id,
            }),
        });
        const json = await response.json();
        this.id = json.id;
    }

    async delete(): Promise<void> {
        await fetch(`/api/contacts/group/${this.id}`, {
            method: 'DELETE',
        });
    }
}

class Groups {
    public groups: Group[];

    constructor() {
        this.groups = [];
    }

    async all(): Promise<Groups> {
        const response = await fetch('/api/contacts/groups');
        const json = await response.json();
        this.groups = json.map((g: any) => Group.fromJson(g));
        return this;
    }
}

export { Contact, Contacts, Group, Groups};