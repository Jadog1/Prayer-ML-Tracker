// src/PrayerRequests.tsx

import React, { useState } from 'react';
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

  const save = async (): Promise<PrayerRequest | null> => {
    const pr = new PrayerRequest();
    pr.id = id;
    pr.contact = contact;
    pr.request = prayerRequest;
    try {
      await pr.save();
      return pr;
    } catch (error: any) {
      setErrorText(error);
    }
    return null
  }

  const findSimilarRequests = async (): Promise<PrayerRequests | null> => {
    const pr = new PrayerRequests();
    let idToUse = id;
    try {
      if (contact.id == 0) {
        let saveResult = await save();
        if (saveResult) idToUse = saveResult.id;
        else return null;
      }
      return await pr.getTopRequests(id);
    } catch (error: any) {
      setErrorText(error);
    }
    return null;
  }
  
  return (
    <div className="container mx-auto p-4">
      <Header save={save} id={id} contact={contact} />
      {errorText && <p className="text-red-500">{errorText}</p>}
      <div className="flex">
        <Sidebar />
        <MainContent prayerRequest={prayerRequest} setPrayerRequest={setPrayerRequest}
          findSimilarRequests={findSimilarRequests} />
      </div>
    </div>
  );
};

export default PrayerRequestView;
