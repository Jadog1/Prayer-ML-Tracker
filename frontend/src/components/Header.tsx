// src/components/Header.tsx

import React from 'react';
import { PrayerRequest, PrayerRequestID } from '../api/prayerRequests';
import { Contact } from '../api/contacts';


type HeaderProps = {
  save: () => void;
  id: PrayerRequestID;
  contact: Contact;
  disabled: boolean;
  toggleListView: () => void;
};
function Header(props: HeaderProps) {


  return (
    <div className="flex justify-between items-center mb-4">

      {props.contact.name &&
        <>
          <p className="text-2xl font-bolder text-black">{props.contact.name}</p>
          <button onClick={() => props.toggleListView()} className="bg-blue-500 text-white px-4 py-2 rounded">
            Toggle List View
          </button>
        </>}
      <button onClick={() => props.save()} className="bg-blue-500 text-white px-4 py-2 rounded" disabled={props.disabled}>
        {props.id ? 'Update' : 'Save'}
      </button>
    </div>
  );
};

export default Header;
