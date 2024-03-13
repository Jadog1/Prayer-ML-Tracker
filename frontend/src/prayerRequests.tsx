// src/PrayerRequests.tsx

import React, { useEffect, useState } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import MainContent from './components/MainContent';
import { PrayerRequest, PrayerRequests } from './api/prayerRequests';
import { Contact } from './api/contacts';

function PrayerRequestView() {
  const [errorText, setErrorText] = useState('');
  const [id, setId] = useState(0);
  const [prayerRequest, setPrayerRequest] = useState('');
  const [contact, setContact] = useState<Contact>(new Contact());
  const [disabled, setDisabled] = useState(false);

  useEffect(() => {
    setDisabled(contact.id === 0);
    setId(0);
  }, [contact]);

  const save = async (): Promise<PrayerRequest | null> => {
    const pr = new PrayerRequest();
    pr.id = id;
    pr.contact = contact;
    pr.request = prayerRequest;
    try {
      let newId = await pr.save();
      setId(newId);
      return pr;
    } catch (error: any) {
      setErrorText(error.message);
    }
    return null
  }

  const findSimilarRequests = async (): Promise<PrayerRequests | null> => {
    const pr = new PrayerRequests();
    try {
      if (id == 0) {
        throw new Error('Prayer request must be saved before finding similar requests');
      }
      return await pr.getTopRequests(id);
    } catch (error: any) {
      setErrorText(error);
    }
    return null;
  }
  
  return (
    <div className="container mx-auto p-4">
      <Header save={save} id={id} contact={contact} disabled={disabled} />
      {errorText && <p className="text-red-500">{errorText}</p>}
      <div className="flex">
        <Sidebar setContact={setContact}/>
        <MainContent prayerRequest={prayerRequest} setPrayerRequest={setPrayerRequest}
          findSimilarRequests={findSimilarRequests} disabled={disabled} />
      </div>
    </div>
  );
};

export default PrayerRequestView;
