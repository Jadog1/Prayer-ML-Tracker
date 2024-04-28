import React, { useEffect } from "react";
import { useState } from "react";
import { PrayerRequest, PrayerRequestID } from "../api/prayerRequests";
import { ErrorHandlerContext } from "../prayerRequests";
import { Contact } from "../api/contacts";

export function PrayerRequestProps () {
    const [id, setId] = useState(0);
    const [prayerRequest, setPrayerRequest] = useState('');
    const [contact, setContact] = useState<Contact>(new Contact());
    const [cachedLastSaved, setCachedLastSaved] = useState<PrayerRequest | null>(null);

    return { id, setId, prayerRequest, setPrayerRequest, contact, setContact, cachedLastSaved, setCachedLastSaved };
}

export function PrayerRequestCRUD(setErrorText: (error: string) => void) {
    const properties = PrayerRequestProps();

    useEffect(() => {
        properties.setId(0);
        properties.setPrayerRequest('');
      }, [properties.contact]);

    const save = async (id: PrayerRequestID, prayerRequest: string): Promise<PrayerRequest | null> => {
        const pr = new PrayerRequest();
        pr.id = id
        pr.contact = properties.contact;
        pr.request = prayerRequest
        try {
            let newPr = await pr.save();
            properties.setId(newPr.id);
            properties.setCachedLastSaved(newPr);
            return pr;
        } catch (error: any) {
            console.error(error);
            setErrorText(error.message);
        }
        return null
    }

    const deletePr = async () => {
        if (properties.id > 0) {
            try {
                let pr = new PrayerRequest();
                pr.id = properties.id;
                await pr.delete();
                properties.setId(0);
                properties.setPrayerRequest('');
            } catch (error: any) {
                console.error(error);
                setErrorText(error.message);
            }
        }
    }

    return { properties, save, deletePr };
}

export type PrayerRequestPropsType = ReturnType<typeof PrayerRequestProps>;
export type PrayerRequestCRUDType = ReturnType<typeof PrayerRequestCRUD>;
