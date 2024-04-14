// src/components/Sidebar.tsx

import React, { useContext, useEffect, useState } from 'react';
import { Contact, Contacts, Group, Groups } from '../api/contacts';
import { ErrorHandlerContext } from '../prayerRequests';


type SidebarProps = {
  setContact: (contact: Contact) => void;
}
function Sidebar(props: SidebarProps) {
  const [groups, setGroups] = useState<Group[]>([]);
  const [contacts, setContacts] = useState<Contact[]>([]);

  const fetchData = async () => {
    try {
      const newGroups = await new Groups().all();
      const newContacts = await new Contacts().all();
      setGroups(newGroups.groups);
      setContacts(newContacts.contacts);
    } catch (error: any) {
      console.error(error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div className="w-1/4 mr-4">
      <p className="text-lg font-semibold mb-2">Groups</p>
      <SidebarGroups groups={groups} contacts={contacts} setContact={props.setContact}
        refresh={fetchData} />
    </div>
  );
}

type SidebarGroupsProps = {
  groups: Group[];
  contacts: Contact[];
  refresh: () => void;
} & SidebarProps;
function SidebarGroups(props: SidebarGroupsProps) {
  const [expandedGroups, setExpandedGroups] = useState<number[]>([]);
  const setErrorText = useContext(ErrorHandlerContext);

  const toggleGroup = (groupId: number) => {
    setExpandedGroups((prevExpanded) =>
      prevExpanded.includes(groupId)
        ? prevExpanded.filter((id) => id !== groupId)
        : [...prevExpanded, groupId]
    );
  };

  const addUser = async (e: React.MouseEvent, groupId: number) => {
    // Prevent bubbling
    e.stopPropagation();
    e.preventDefault();

    let name = prompt('Enter contact name');
    if (!name) return;
    try {
      let contact = new Contact();
      contact.name = name;
      let group = props.groups.find((group) => group.id === groupId);
      if (!group) throw new Error('Group not found');
      contact.group = group;
      contact.save();
      props.refresh();
    } catch (error: any) {
      setErrorText(error.message);
      console.error(error);
    }
  }

  return (
    <ul>
      {props.groups.map((group) => (
        <li key={group.id} className="mb-2 border-b pb-2">
          <div className="cursor-pointer flex justify-between items-center"
            onClick={() => toggleGroup(group.id)}>
            <span className="flex items-center">
              {expandedGroups.includes(group.id) ? '🔽' : '▶️'}
              <span className="ml-2">{group.name}</span>
            </span>
            <button className="bg-blue-500 text-white px-2 rounded m-1 float-right" onClick={(e) => addUser(e, group.id)}>
              Add
            </button>
          </div>
          {expandedGroups.includes(group.id) && (
            <div className="flex flex-col max-h-80 overflow-y-auto">
              <ul className="ml-4">
                {props.contacts
                  .filter((contact) => contact.group.id === group.id)
                  .map((contact) => (
                    <li key={contact.id} className="pb-2 pt-2 cursor-pointer border-b hover:bg-blue-300 transition duration-300 ease-in-out" onClick={() => props.setContact(contact)}>
                      {contact.name}
                    </li>
                  ))}
              </ul>
            </div>
          )}
        </li>
      ))}
    </ul>
  );
}

export default Sidebar;
