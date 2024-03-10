// src/PrayerRequests.tsx

import React from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import MainContent from './components/MainContent';

const PrayerRequests: React.FC = () => {
  const handleSave = (note: string) => {
    // Replace this with your actual save functionality
    fetch('/prayerRequests/save', {
      method: 'POST',
      body: JSON.stringify({ note }),
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then(response => response.json())
      .then(data => console.log(data))
      .catch(error => console.error(error));
  };

  const handleLoadNotes = () => {
    // Replace this with your actual load notes functionality
    console.log('Load Notes clicked');
  };

  const handleTopRequests = () => {
    // Replace this with your actual top requests functionality
    fetch('/prayerRequests/topRequests')
      .then(response => response.json())
      .then(data => console.log(data))
      .catch(error => console.error(error));
  };

  const handleFindVerses = () => {
    // Replace this with your actual find Bible verses functionality
    fetch('/prayerRequests/findBibleVerses')
      .then(response => response.json())
      .then(data => console.log(data))
      .catch(error => console.error(error));
  };

  return (
    <div className="container mx-auto p-4">
      <Header onButtonClick={() => handleSave('')} />
      <div className="flex">
        <Sidebar />
        <MainContent onSave={handleSave} onLoadNotes={handleLoadNotes} onTopRequests={handleTopRequests} onFindVerses={handleFindVerses} />
      </div>
    </div>
  );
};

export default PrayerRequests;
