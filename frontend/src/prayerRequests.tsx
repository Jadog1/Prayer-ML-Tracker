// src/PrayerRequests.tsx

import React, { useEffect, useState } from 'react';
import Header from './components/Header';
import Sidebar from './pages/PrayerRequestPage/Sidebar';
import MainContent from './components/MainContent';
import { PrayerRequest, PrayerRequestID, PrayerRequests } from './api/prayerRequests';
import ErrorMessage from './components/errorBubble';
import PrayerList from './components/PrayerList';
import { PrayerRequestCRUD, PrayerRequestCRUDType } from './util/prayerRequestProperties';
import PrayerRequestContent from './pages/PrayerRequestPage/prayerRequests';
import PrayerSummaryContent from './pages/PrayerSummaryPage/prayerSummary';

export type errorHandler = (error: string) => void;
export const ErrorHandlerContext = React.createContext<errorHandler>((error: string) => { });
type Pages = 'Prayer Requests' | 'Prayer Summary';

// Page header will have two options, "Prayer Requests" and "Prayer Summary"
// The user can switch between the two options by clicking on the respective button
function PageHeader(props: {setPage: (page: Pages) => void}) {
  const [selected, setSelected] = useState<Pages>('Prayer Requests');

  useEffect(() => {
    props.setPage(selected);
  }, [selected]);

  return (
    <div className="flex justify-between border-b p-2">
      <div className="flex">
        <button className={`mr-5 ${selected === 'Prayer Requests' ? 'text-black' : 'text-blue-500'}`}
          onClick={() => setSelected('Prayer Requests')}>Prayer Requests</button>
        <button className={`mr-5 ${selected === 'Prayer Summary' ? 'text-black' : 'text-blue-500'}`}
          onClick={() => setSelected('Prayer Summary')}>Prayer Summary</button>
      </div>
      <div className="flex">
        <button className="bg-blue-500 text-white p-2 rounded">Logout</button>
      </div>
    </div>
  );
}

function PrayerRequestView() {
  const [errorText, setErrorText] = useState('');
  const [page, setPage] = useState<Pages>('Prayer Requests');
  const prayerRequestCRUD = PrayerRequestCRUD(setErrorText);

  return (
    <ErrorHandlerContext.Provider value={setErrorText}>
      <PageHeader setPage={setPage}/>
      <div className="container mx-auto p-4">
        {errorText && <ErrorMessage message={errorText} onClose={() => setErrorText("")} />}
        <PageHandler page={page} prayerRequestCRUD={prayerRequestCRUD} />
      </div>
    </ErrorHandlerContext.Provider>
  );
};

function PageHandler(props: {page: Pages, prayerRequestCRUD: PrayerRequestCRUDType}) {
  switch (props.page) {
    case 'Prayer Requests':
      return <PrayerRequestContent prayerRequestCRUD={props.prayerRequestCRUD} />;
    case 'Prayer Summary':
      return <PrayerSummaryContent />;
  }
}



export default PrayerRequestView;
