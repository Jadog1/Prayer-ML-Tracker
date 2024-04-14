// src/components/Header.tsx

import React from 'react';
import { PrayerRequest, PrayerRequestID } from '../api/prayerRequests';
import { Contact } from '../api/contacts';
import { PrayerRequestCRUDType, PrayerRequestPropsType } from '../util/prayerRequestProperties';


type HeaderProps = {
  deletePr: () => void;
  createNewPrayerRequest: () => void;
  disabled: boolean;
  listView: boolean;
  toggleListView: () => void;
  prayerRequestCRUDProps: PrayerRequestPropsType;
};
function Header(props: HeaderProps) {
  const { contact, id } = props.prayerRequestCRUDProps;

  const deleteContact = () => {
    alert("Not implemented");
  }


  return (
    <div className="flex justify-between items-center mb-4">

      {contact.name &&
        <>
          <p className="text-2xl font-bolder text-black">
            {contact.name} <i className="fa-solid fa-trash" onClick={() => deleteContact()}></i>
          </p>

          {!props.listView && <button onClick={() => props.toggleListView()} className="bg-blue-500 text-white px-4 py-2 rounded">
            Go back
          </button>}

          {(id > 0 || props.listView) && <button onClick={() => props.createNewPrayerRequest()} className="bg-green-500 text-white px-4 py-2 rounded">
            New
          </button>}

          {!props.listView && id > 0 && <button onClick={() => props.deletePr()} className="bg-blue-500 text-white px-4 py-2 rounded" disabled={props.disabled}>
            Delete
          </button>
          }
        </>
      }
    </div>
  );
};

export default Header;
