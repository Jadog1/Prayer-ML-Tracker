// src/components/Header.tsx

import React from 'react';

interface HeaderProps {
  onButtonClick: () => void;
}

const Header: React.FC<HeaderProps> = ({ onButtonClick }) => {
  return (
    <div className="flex justify-between items-center mb-4">
      <h1 className="text-2xl font-bold">Prayer Requests</h1>
      <button onClick={onButtonClick} className="bg-blue-500 text-white px-4 py-2 rounded">
        Save
      </button>
    </div>
  );
};

export default Header;
