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
import { PrayerRequestCRUD, PrayerRequestCRUDType } from './util/prayerRequestProperties';

export type errorHandler = (error: string) => void;
export const ErrorHandlerContext = React.createContext<errorHandler>((error: string) => { });

function PrayerRequestView() {
  const [errorText, setErrorText] = useState('');
  const prayerRequestCRUD = PrayerRequestCRUD(setErrorText);

  return (
    <ErrorHandlerContext.Provider value={setErrorText}>
      <div className="container mx-auto p-4">
        {errorText && <ErrorMessage message={errorText} onClose={() => setErrorText("")} />}
        <div className="flex">
          <Sidebar setContact={prayerRequestCRUD.properties.setContact} />
          <PrayerRequestsBody prayerRequestCRUD={prayerRequestCRUD} />
        </div>
      </div>
    </ErrorHandlerContext.Provider>
  );
};


type PrayerRequestBodyProps = {
  prayerRequestCRUD: PrayerRequestCRUDType;
}
function PrayerRequestsBody(props: PrayerRequestBodyProps) {
  const [listView, setListView] = useState(true);
  const [prayerRequests, setPrayerRequests] = useState<PrayerRequests>(new PrayerRequests());
  const setErrorText = React.useContext(ErrorHandlerContext);
  const crudProps = props.prayerRequestCRUD.properties;
  const [disabled, setDisabled] = useState(false);

  useEffect(() => {
   setDisabled(crudProps.contact.id === 0);
  }, [crudProps.contact]);

  useEffect(() => {
    loadPrayerRequests()
    setListView(true);
  }, [crudProps.contact]);

  const editRecord = async (id: number) => {
    try {
      let pr = await new PrayerRequest().load(id);
      crudProps.setId(id);
      crudProps.setPrayerRequest(pr.request);
      setListView(false);
    } catch (error: any) {
      console.error(error);
      setErrorText(error.message);
    }
  }

  const loadPrayerRequests = async () => {
    try {
      if (crudProps.contact.id) {
        let pr = new PrayerRequests()
        let prayerRequests = await pr.getRequestsForContact(crudProps.contact.id);
        if (prayerRequests) setPrayerRequests(pr);
      }
    } catch (error: any) {
      console.error(error);
      setErrorText(error.message);
    }
  }

  const deletePrayerRequest = async (pr: PrayerRequest) => {
    try {
      await pr.delete();
      loadPrayerRequests();
    } catch (error: any) {
      console.error(error);
      setErrorText(error.message);
    }
  }

  const createNewPrayerRequest = () => {
    crudProps.setPrayerRequest('');
    crudProps.setId(0);
    let result = props.prayerRequestCRUD.save(0, "");
    if (result != null) setListView(false);
  }

  const toggleListView = () => {
    if (!listView) {
      crudProps.setId(0);
      loadPrayerRequests();
    }
    setListView(!listView);
  }

  const deletePr = async () => {
    await props.prayerRequestCRUD.deletePr();
    toggleListView();
  }


  return (
    <div className="w-3/4">
      <Header deletePr={deletePr} disabled={disabled} listView={listView}
        toggleListView={toggleListView} createNewPrayerRequest={createNewPrayerRequest} 
        prayerRequestCRUDProps={crudProps}/>
      {listView ?
        <PrayerList requests={prayerRequests.requests} id={crudProps.id} editRecord={editRecord}
          delete={deletePrayerRequest} />
        :
        <MainContent prayerRequestCRUD={props.prayerRequestCRUD}
          disabled={crudProps.id == 0} />
      }
    </div>
  );
}

export default PrayerRequestView;
