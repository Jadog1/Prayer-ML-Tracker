
import React, { useContext, useEffect, useState } from 'react';
import { Contact, Contacts, Group, Groups } from '../../api/contacts';
import { ErrorHandlerContext } from '../../prayerRequests';
import { PrayerSummary } from '../../api/prayerSummary';
import { set } from 'lodash';


type SidebarProps = {
  setSummary: (summary: PrayerSummary) => void;
}
function Sidebar(props: SidebarProps) {
  const [groups, setGroups] = useState<Group[]>([]);

  const fetchData = async () => {
    try {
      const newGroups = await new Groups().all();
      setGroups(newGroups.groups);
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
      <SidebarGroups groups={groups} setSummary={props.setSummary} />
    </div>
  );
}

type SidebarGroupsProps = {
  groups: Group[];
} & SidebarProps;
function SidebarGroups(props: SidebarGroupsProps) {
    const [selectedGroup, setSelectedGroup] = useState<number>(0);
    const setErrorText = useContext(ErrorHandlerContext);
    const [fromDate, setFromDate] = useState<string>(aWeekAgo());
    const [toDate, setToDate] = useState<string>(today());

    const get_summary = async () => {
        try {
            let summary = await PrayerSummary.load(fromDate, toDate, selectedGroup);
            props.setSummary(summary);
        } catch (error: any) {
            setErrorText(error.message);
            console.error(error);
        }
    }

    const dateInputClasses = "border border-gray-300 rounded p-2 mb-4";

    return (
        <div className="flex flex-col">
            <div className="flex flex-col mb-4">
                <label className="text-sm">Group</label>
                <select value={selectedGroup} onChange={(e) => setSelectedGroup(parseInt(e.target.value))} className="border border-gray-300 rounded p-2 mb-4">
                    <option value={0}>All</option>
                    {props.groups.map((group) => (
                        <option key={group.id} value={group.id}>{group.name}</option>
                    ))}
                </select>
            </div>
            <div className="flex flex-col mb-4">
                <label className="text-sm">From Date</label>
                <input type="date" value={fromDate} onChange={(e) => setFromDate(e.target.value)} className={dateInputClasses} />
            </div>
            <div className="flex flex-col mb-4">
                <label className="text-sm">To Date</label>
                <input type="date" value={toDate} onChange={(e) => setToDate(e.target.value)} className={dateInputClasses} />
            </div>
            <button className="bg-blue-500 text-white p-2 rounded" onClick={get_summary}>Get Summary</button>
        </div>
    );
}

function aWeekAgo() {
    const date = new Date();
    date.setDate(date.getDate() - 7);
    return convertDateToInputDate(date);
}

function today() {
    return convertDateToInputDate(new Date());
}

function convertDateToInputDate(date: Date) {
    const offset = date.getTimezoneOffset()
    date = new Date(date.getTime() - (offset*60*1000))
    return date.toISOString().split('T')[0]
}

export default Sidebar;