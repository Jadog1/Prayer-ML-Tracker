// src/PrayerRequests.tsx

import React, { useEffect, useState } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import MainContent from './components/MainContent';
import { PrayerRequest, PrayerRequestID, PrayerRequests } from './api/prayerRequests';
import { Contact } from './api/contacts';
import ErrorMessage from './components/errorBubble';
import PrayerList from './components/PrayerList';
import { BibleResults } from './api/bible';
import { over } from 'lodash';

function PrayerRequestView() {
  const [errorText, setErrorText] = useState('');
  const [id, setId] = useState(0);
  const [prayerRequest, setPrayerRequest] = useState('');
  const [contact, setContact] = useState<Contact>(new Contact());
  const [disabled, setDisabled] = useState(false);

  useEffect(() => {
    setDisabled(contact.id === 0);
    setId(0);
    setPrayerRequest('');
  }, [contact]);

  const save = async (overridePrayerRequest : string = "", overridePrayerID : number = 0): Promise<PrayerRequest | null> => {
    const pr = new PrayerRequest();
    pr.id = overridePrayerID || id;
    pr.contact = contact;
    pr.request = overridePrayerRequest || prayerRequest;
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

  const deletePr = async () => {
    if (id > 0) {
      try {
        let pr = new PrayerRequest();
        pr.id = id;
        await pr.delete();
        setId(0);
        setPrayerRequest('');
      } catch (error: any) {
        console.error(error);
        setErrorText(error.message);
      }
    }
  }

  const findSimilarRequests = async (): Promise<PrayerRequests | null> => {
    try {
      if (id == 0) {
        throw new Error('Prayer request must be saved before finding similar requests');
      }
      return await new PrayerRequests().getTopRequests(id);
    } catch (error: any) {
      console.error(error);
      setErrorText(error.message);
    }
    return null;
  }

  const findSimilarBibleVerses = async (): Promise<BibleResults | null> => {
    try {
      if (id == 0) {
        throw new Error('Prayer request must be saved before finding similar bible verses');
      }
      return await new BibleResults().getTopBibleVerses(id);
    } catch (error: any) {
      console.error(error);
      setErrorText(error.message);
    }
    return null;
  }

  const linkPrayerRequest = async (pr: PrayerRequest): Promise<boolean> => {
    try {
      await pr.link(id);
      return true;
    } catch (error: any) {
      console.error(error);
      setErrorText(error.message);
    }
    return false;
  }

  return (
    <div className="container mx-auto p-4">
      {errorText && <ErrorMessage message={errorText} onClose={() => setErrorText("")} />}
      <div className="flex">
        <Sidebar setContact={setContact} />
        <PrayerRequestsBody save={save} id={id} contact={contact} disabled={disabled} 
          prayerRequest={prayerRequest} setPrayerRequest={setPrayerRequest} 
          findSimilarRequests={findSimilarRequests} setId={setId} setErrorText={setErrorText}
          findSimilarBibleVerses={findSimilarBibleVerses} deletePr={deletePr}
          linkPrayerRequest={linkPrayerRequest}/>
      </div>
    </div>
  );
};

type PrayerRequestBodyProps = {
  save: (overridePrayerRequest?: string, overridePrayerID?: number) => Promise<PrayerRequest | null>;
  id: number;
  setId: (id: number) => void;
  contact: Contact;
  disabled: boolean;
  prayerRequest: string;
  setPrayerRequest: (prayerRequest: string) => void;
  findSimilarRequests: () => Promise<PrayerRequests | null>;
  findSimilarBibleVerses: () => Promise<BibleResults | null>;
  setErrorText: (errorText: string) => void;
  linkPrayerRequest: (pr: PrayerRequest) => Promise<boolean>;
  deletePr : () => Promise<void>;
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
      loadPrayerRequests();
    } catch (error: any) {
      console.error(error);
      props.setErrorText(error.message);
    }
  }

  const createNewPrayerRequest = () => {
    props.setPrayerRequest('');
    props.setId(0);
    let result = props.save("", 0);
    if (result != null) setListView(false);
  }

  const toggleListView = () => {
    if (!listView) {
      props.setId(0);
      loadPrayerRequests();
    }
    setListView(!listView);
  }

  const deletePr = async () => {
    await props.deletePr();
    toggleListView();
  }


  return (
    <div className="w-3/4">
      <Header deletePr={deletePr} id={props.id} contact={props.contact} disabled={props.disabled} 
        listView={listView}
        toggleListView={toggleListView} createNewPrayerRequest={createNewPrayerRequest} />
      {listView ? 
        <PrayerList requests={prayerRequests.requests} id={props.id} editRecord ={editRecord} 
          delete={deletePrayerRequest} /> 
        :
          <MainContent prayerRequest={props.prayerRequest} setPrayerRequest={props.setPrayerRequest} 
           findSimilarRequests={props.findSimilarRequests} disabled={props.id == 0} 
           findSimilarBibleVerses={props.findSimilarBibleVerses} save={props.save}
           linkPrayerRequest={props.linkPrayerRequest}/>
      }
    </div>
  );
}

export default PrayerRequestView;
