// src/components/MainContent.tsx

import React, { useState } from 'react';
import { PrayerRequests } from '../api/prayerRequests';

interface MainContentProps {
  prayerRequest: string;
  setPrayerRequest: (prayerRequest: string) => void;
  findSimilarRequests: () => Promise<PrayerRequests | null>;
}

function MainContent(props: MainContentProps) {
  const [prayerRequests, setPrayerRequests] = useState<PrayerRequests>(new PrayerRequests());

  const findSimilarRequests = async () => {
    try {
      let newPrayerRequests = await props.findSimilarRequests();
      if (newPrayerRequests) 
        setPrayerRequests(newPrayerRequests);
    } catch (error: any) {
      console.error(error);
    }
  }

  return (
    <div className="w-3/4">
      <textarea
        value={props.prayerRequest}
        onChange={(e) => props.setPrayerRequest(e.target.value)}
        className="w-full h-64 p-2 border rounded"
        placeholder="Type your prayer request here..."
      ></textarea>

      <div className="mt-4">
        <button onClick={findSimilarRequests} className="bg-yellow-500 text-white px-4 py-2 mr-2 rounded">
          Top Requests
        </button>
      </div>

      {prayerRequests.requests.length > 0 && <SimilarRequests prayerRequests={prayerRequests} />}
    </div>
  );
};

function SimilarRequests(props: {prayerRequests: PrayerRequests}) {
  return (
    <div className="mt-4">
      <p className="text-lg font-semibold mb-2">Similar Requests</p>
      <ul>
        {props.prayerRequests.requests.map((prayerRequest) => (
          <li key={prayerRequest.id} className="mb-2">
            {prayerRequest.request}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default MainContent;
