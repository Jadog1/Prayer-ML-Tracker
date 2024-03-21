// src/components/Header.tsx

import React from 'react';
import { PrayerRequest, PrayerRequestID } from '../api/prayerRequests';
import { Contact } from '../api/contacts';


type HeaderProps = {
  deletePr: () => void;
  id: PrayerRequestID;
  createNewPrayerRequest: () => void;
  contact: Contact;
  disabled: boolean;
  listView: boolean;
  toggleListView: () => void;
};
function Header(props: HeaderProps) {


  return (
    <div className="flex justify-between items-center mb-4">

      {props.contact.name &&
        <>
          <p className="text-2xl font-bolder text-black">{props.contact.name}</p>
          {!props.listView && <button onClick={() => props.toggleListView()} className="bg-blue-500 text-white px-4 py-2 rounded">
            Go back
          </button>}

          {(props.id > 0 || props.listView) && <button onClick={() => props.createNewPrayerRequest()} className="bg-green-500 text-white px-4 py-2 rounded">
            New
          </button>}

          {!props.listView && <button onClick={() => props.deletePr()} className="bg-blue-500 text-white px-4 py-2 rounded" disabled={props.disabled}>
            Delete
          </button>
          }
        </>
      }
    </div>
  );
};

export default Header;
