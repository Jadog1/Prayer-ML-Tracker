// src/PrayerRequests.tsx

import React, { useEffect, useState } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import MainContent from './components/MainContent';
import { PrayerRequest, PrayerRequests } from './api/prayerRequests';
import { Contact } from './api/contacts';
import ErrorMessage from './components/errorBubble';
import PrayerList from './components/PrayerList';

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
      console.error(error);
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
      console.error(error);
      setErrorText(error.message);
    }
    return null;
  }

  return (
    <div className="container mx-auto p-4">
      {errorText && <ErrorMessage message={errorText} onClose={() => setErrorText("")} />}
      <div className="flex">
        <Sidebar setContact={setContact} />
        <PrayerRequestsBody save={save} id={id} contact={contact} disabled={disabled} 
          prayerRequest={prayerRequest} setPrayerRequest={setPrayerRequest} 
          findSimilarRequests={findSimilarRequests} setId={setId} setErrorText={setErrorText}/>
      </div>
    </div>
  );
};

type PrayerRequestBodyProps = {
  save: () => Promise<PrayerRequest | null>;
  id: number;
  setId: (id: number) => void;
  contact: Contact;
  disabled: boolean;
  prayerRequest: string;
  setPrayerRequest: (prayerRequest: string) => void;
  findSimilarRequests: () => Promise<PrayerRequests | null>;
  setErrorText: (errorText: string) => void;
}
function PrayerRequestsBody(props: PrayerRequestBodyProps) {
  const [listView, setListView] = useState(true);
  const [prayerRequests, setPrayerRequests] = useState<PrayerRequests>(new PrayerRequests());

  useEffect(() => {
    loadPrayerRequests()
    setListView(true);
  }, [props.contact]);

  const editRecord = async (id: number) => {
    try {
      let pr = await new PrayerRequest().load(id);
      props.setId(id);
      props.setPrayerRequest(pr.request);
      setListView(false);
    } catch (error: any) {
      console.error(error);
      props.setErrorText(error.message);
    }
  }

  const loadPrayerRequests = async () => {
    try {
      if (props.contact.id) {
        let pr = new PrayerRequests()
        let prayerRequests = await pr.getRequestsForContact(props.contact.id);
        if (prayerRequests) setPrayerRequests(pr);
      }
    } catch (error: any) {
      console.error(error);
      props.setErrorText(error.message);
    }
  }

  const deletePrayerRequest = async (pr: PrayerRequest) => {
    try {
      await pr.delete();
      setPrayerRequests(prayerRequests);
    } catch (error: any) {
      console.error(error);
      props.setErrorText(error.message);
    }
  }

  const toggleListView = () => {
    if (!listView) props.setId(0);
    setListView(!listView);
  }


  return (
    <div className="w-3/4">
      <Header save={props.save} id={props.id} contact={props.contact} disabled={props.disabled} 
        toggleListView={toggleListView}/>
      {listView ? 
        <PrayerList requests={prayerRequests.requests} id={props.id} editRecord ={editRecord} 
          delete={deletePrayerRequest} /> 
        :
          <MainContent prayerRequest={props.prayerRequest} setPrayerRequest={props.setPrayerRequest} 
           findSimilarRequests={props.findSimilarRequests} disabled={props.disabled} />
      }
    </div>
  );
}

export default PrayerRequestView;
