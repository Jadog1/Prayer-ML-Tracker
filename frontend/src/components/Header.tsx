// src/components/Header.tsx

import React from 'react';
import { PrayerRequest, PrayerRequestID } from '../api/prayerRequests';
import { Contact } from '../api/contacts';


type HeaderProps = {
  save: () => void;
  id: PrayerRequestID;
  contact: Contact
};
function Header(props: HeaderProps) {


  return (
    <div className="flex justify-between items-center mb-4">
      <h1 className="text-2xl font-bold">Prayer Requests</h1>
      {props.contact.name && 
        <p className="text-gray-500">{props.contact.name}</p>}
      <button onClick={() => props.save()} className="bg-blue-500 text-white px-4 py-2 rounded">
        {props.id ? 'Update' : 'Save'}
      </button>
    </div>
  );
};

export default Header;
