// src/components/MainContent.tsx

import React, { useContext, useState } from 'react';
import { PrayerRequest, PrayerRequestID, PrayerRequests } from '../api/prayerRequests';
import { BibleResults } from '../api/bible';
import TruncateText from './TruncateText';
import _debounce from 'lodash/debounce';
import { ErrorHandlerContext } from '../prayerRequests';
import { PrayerRequestCRUDType } from '../util/prayerRequestProperties';



function findSimimlar(setErrorText: (error: string) => void) {

  const findSimilarRequestsHandler = async (id: PrayerRequestID): Promise<PrayerRequests | null> => {
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

  const findSimilarBibleVersesHandler = async (id: PrayerRequestID): Promise<BibleResults | null> => {
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

  return { findSimilarRequestsHandler, findSimilarBibleVersesHandler };
}

let timeoutId: NodeJS.Timeout | undefined;
interface MainContentProps {
  prayerRequestCRUD: PrayerRequestCRUDType
  disabled: boolean;
}
const colors = ["black", "blue", "red", "pink", "purple", "gray", "cyan"]

function MainContent(props: MainContentProps) {
  const [prayerRequests, setPrayerRequests] = useState<PrayerRequests>(new PrayerRequests());
  const [bibleVerses, setBibleVerses] = useState<BibleResults>(new BibleResults());
  const [updatedTimestamp, setUpdatedTimestamp] = useState<string>('');
  const [sectionOpen, setSectionOpen] = useState<'requests' | 'verses'>('requests');
  const setErrorText = useContext(ErrorHandlerContext);
  const { findSimilarRequestsHandler, findSimilarBibleVersesHandler } = findSimimlar(setErrorText);
  const prayerCRUD = props.prayerRequestCRUD;
  const prayerCRUDProps = prayerCRUD.properties;

  const findSimilarRequests = async () => {
    let newPrayerRequests = await findSimilarRequestsHandler(prayerCRUDProps.id);
    if (newPrayerRequests)
      setPrayerRequests(newPrayerRequests);
    setSectionOpen('requests');
  }

  const findSimilarBibleVerses = async () => {
    let newBibleVerses = await findSimilarBibleVersesHandler(prayerCRUDProps.id);
    if (newBibleVerses)
      setBibleVerses(newBibleVerses);
    setSectionOpen('verses');
  }

  const handleSave = async (newRequest: string) => {
    let pr = await prayerCRUD.save(prayerCRUDProps.id, newRequest);
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


  const setPrayerRequest = (newRequest: string) => {
    clearTimeout(timeoutId)
    timeoutId = setTimeout(() => handleSave(newRequest), 500);
  };

  return (
    <div className="w-full">
      <textarea
        value={prayerCRUDProps.prayerRequest}
        onChange={(e) => prayerCRUDProps.setPrayerRequest(e.target.value)}
        onKeyUp={(e) => {
          const target = e.target as HTMLTextAreaElement;
          setPrayerRequest(target.value);
        }}

        className="w-full h-64 p-2 border rounded"
        placeholder="Type your prayer request here..."
        disabled={props.disabled}
      ></textarea>

      <div className="flex justify-between">
        {prayerCRUDProps.cachedLastSaved != null &&
          <p className="text-sm text-left text-gray-500">
            {prayerCRUDProps.cachedLastSaved.prayer_type} | {prayerCRUDProps.cachedLastSaved.emotion} | {prayerCRUDProps.cachedLastSaved.sentiment} | {prayerCRUDProps.cachedLastSaved.topics.join(', ')}
          </p>}

        {updatedTimestamp != '' &&
          <p className="text-sm text-right">Updated {updatedTimestamp}</p>}
      </div>


      <div className="mt-4">
        <button onClick={findSimilarRequests} className="bg-yellow-500 text-white px-4 py-2 mr-2 rounded">
          Similar Prayer Requests
        </button>

        <button onClick={findSimilarBibleVerses} className="bg-green-500 text-white px-4 py-2 rounded">
          Similar Bible Verses
        </button>
      </div>

      {sectionOpen == "requests" && <SimilarRequests existingID={prayerCRUDProps.id} prayerRequests={prayerRequests} {...props} />}
      {sectionOpen == "verses" && <SimilarBibleVerses verses={bibleVerses} />}
    </div>
  );
};


function SimilarRequests(props: { prayerRequests: PrayerRequests, existingID: PrayerRequestID } & MainContentProps) {
  const [selectedRequestId, setSelectedRequestId] = useState<number | null>(null);
  const setErrorText = useContext(ErrorHandlerContext);

  const linkPrayerRequest = async (pr: PrayerRequest): Promise<boolean> => {
    try {
      await pr.link(pr.id, props.existingID);
      return true;
    } catch (error: any) {
      console.error(error);
      setErrorText(error.message);
    }
    return false;
  }

  const link = async (request: PrayerRequest) => {
    let isSuccess = await linkPrayerRequest(request);
    if (isSuccess) setSelectedRequestId(request.id);
  }

  let uniqueLinkIdColors: { [id: number]: string } = {};
  let colorsIndexAt = 0;
  props.prayerRequests.requests.forEach((prayerRequest: PrayerRequest) => {
    if (!prayerRequest.link_id) return;
    if (!(prayerRequest.link_id in uniqueLinkIdColors)) {
      uniqueLinkIdColors[prayerRequest.link_id] = colors[colorsIndexAt];
      colorsIndexAt = (colorsIndexAt + 1); // We should never go out of bounds
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
            className={`pb-2 pt-2 cursor-pointer border-b hover:bg-blue-300 transition duration-300 ease-in-out ${selectedRequestId === prayerRequest.id ? 'bg-green-200' : ''
              }`}
          >
            <div className="flex items-stretch gap-x-1">
              <div className="flex-1">{prayerRequest.request}</div>
            </div>
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
