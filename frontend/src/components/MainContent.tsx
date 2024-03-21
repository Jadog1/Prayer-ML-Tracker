// src/components/MainContent.tsx

import React, { useState } from 'react';
import { PrayerRequest, PrayerRequestID, PrayerRequests } from '../api/prayerRequests';
import { BibleResults } from '../api/bible';
import TruncateText from './TruncateText';
import _debounce from 'lodash/debounce';

let timeoutId: NodeJS.Timeout | undefined;
interface MainContentProps {
  prayerRequest: string;
  setPrayerRequest: (prayerRequest: string) => void;
  findSimilarRequests: () => Promise<PrayerRequests | null>;
  findSimilarBibleVerses: () => Promise<BibleResults | null>;
  linkPrayerRequest: (pr: PrayerRequest) => Promise<boolean>;
  disabled: boolean;
  save: (overridePrayerRequest?: string) => Promise<PrayerRequest | null>;
}

function MainContent(props: MainContentProps) {
  const [prayerRequests, setPrayerRequests] = useState<PrayerRequests>(new PrayerRequests());
  const [bibleVerses, setBibleVerses] = useState<BibleResults>(new BibleResults());
  const [updatedTimestamp, setUpdatedTimestamp] = useState<string>('');
  const [sectionOpen, setSectionOpen] = useState<'requests' | 'verses'>('requests');

  const findSimilarRequests = async () => {
    let newPrayerRequests = await props.findSimilarRequests();
    if (newPrayerRequests)
      setPrayerRequests(newPrayerRequests);
    setSectionOpen('requests');
  }

  const findSimilarBibleVerses = async () => {
    let newBibleVerses = await props.findSimilarBibleVerses();
    if (newBibleVerses)
      setBibleVerses(newBibleVerses);
    setSectionOpen('verses');
  }

  const handleSave = async (newRequest: string) => {
    let pr = await props.save(newRequest);
    if (pr == null) return;
    setUpdatedTimestamp(new Date().toLocaleTimeString());

    switch (sectionOpen) {
      case 'requests':
        await findSimilarRequests();
        break;
      case 'verses':
        await findSimilarBibleVerses();
        break;
    }
  }


  const setPrayerRequest = (newRequest : string) => {
    clearTimeout(timeoutId)
    timeoutId = setTimeout(() => handleSave(newRequest), 500);
  };

  return (
    <div className="w-full">
      <textarea
        value={props.prayerRequest}
        onChange = {(e) => props.setPrayerRequest(e.target.value)}
        onKeyUp={(e) => {
          const target = e.target as HTMLTextAreaElement;
          setPrayerRequest(target.value);
        }}
        
        className="w-full h-64 p-2 border rounded"
        placeholder="Type your prayer request here..."
        disabled={props.disabled}
      ></textarea>

      {updatedTimestamp != '' && 
        <p className="text-sm text-right">Updated {updatedTimestamp}</p>}

      <div className="mt-4">
        <button onClick={findSimilarRequests} className="bg-yellow-500 text-white px-4 py-2 mr-2 rounded">
          Similar Prayer Requests
        </button>

        <button onClick={findSimilarBibleVerses} className="bg-green-500 text-white px-4 py-2 rounded">
          Similar Bible Verses
        </button>
      </div>

      {sectionOpen == "requests" && <SimilarRequests prayerRequests={prayerRequests} {...props} />}
      {sectionOpen == "verses" && <SimilarBibleVerses verses={bibleVerses} />}
    </div>
  );
};


function SimilarRequests(props: { prayerRequests: PrayerRequests } & MainContentProps) {
  const [selectedRequestId, setSelectedRequestId] = useState<number | null>(null);

  const link = async (request: PrayerRequest) => {
    let isSuccess = await props.linkPrayerRequest(request);
    if (isSuccess) setSelectedRequestId(request.id);
  }

  let uniqueLinkIdColors: { [id: number]: string } = {};
  props.prayerRequests.requests.forEach((prayerRequest: PrayerRequest) => {
    if (!(prayerRequest.id in uniqueLinkIdColors)) {
      uniqueLinkIdColors[prayerRequest.id] = `#${Math.floor(Math.random()*16777215).toString(16)}`;
    }
  });

  return (
    <div className="mt-4">
      <p className="text-lg font-semibold mb-2">Similar Requests</p>
      <ul>
        {props.prayerRequests.requests.map((prayerRequest: PrayerRequest) => (
          <li
            key={prayerRequest.id}
            onClick={() => link(prayerRequest)}
            className={`pb-2 pt-2 cursor-pointer border-b hover:bg-blue-300 transition duration-300 ease-in-out ${
              selectedRequestId === prayerRequest.id ? 'bg-green-200' : ''
            }`}
          >
            {prayerRequest.link_id > 0 && <span className="mr-2" style={{ color: uniqueLinkIdColors[prayerRequest.link_id] }}>[]</span>}
            {prayerRequest.request}
          </li>
        ))}
      </ul>
    </div>
  );
}

function SimilarBibleVerses(props: { verses: BibleResults }) {
  return (
    <div className="mt-4">
      <p className="text-lg font-semibold mb-2">Similar Bible Verses</p>
      <ul>
        {props.verses.results.map((verse, index: number) => (
          <li key={index} className="pb-2 pt-2 border-b">
            <TruncateText text={`${verse.Context()} - ${verse.Text()}`} limit={200} />
          </li>
        ))}
      </ul>
    </div>
  );
}

export default MainContent;
