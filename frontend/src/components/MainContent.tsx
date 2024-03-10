// src/components/MainContent.tsx

import React, { useState } from 'react';

interface MainContentProps {
  onSave: (note: string) => void;
  onLoadNotes: () => void;
  onTopRequests: () => void;
  onFindVerses: () => void;
}

const MainContent: React.FC<MainContentProps> = ({ onSave, onLoadNotes, onTopRequests, onFindVerses }) => {
  const [note, setNote] = useState('');

  return (
    <div className="w-3/4">
      <textarea
        value={note}
        onChange={(e) => setNote(e.target.value)}
        className="w-full h-64 p-2 border rounded"
        placeholder="Type your note here..."
      ></textarea>

      <div className="mt-4">
        <button onClick={() => onSave(note)} className="bg-green-500 text-white px-4 py-2 mr-2 rounded">
          Load Notes
        </button>
        <button onClick={onLoadNotes} className="bg-yellow-500 text-white px-4 py-2 mr-2 rounded">
          Top Requests
        </button>
        <button onClick={onTopRequests} className="bg-purple-500 text-white px-4 py-2 rounded">
          Find Bible Verses
        </button>
      </div>
    </div>
  );
};

export default MainContent;
