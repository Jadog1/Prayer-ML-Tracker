import React, { useState } from 'react';

interface TruncateTextProps {
  text: string;
  limit: number;
}

const TruncateText: React.FC<TruncateTextProps> = ({ text, limit }) => {
  const [isTruncated, setIsTruncated] = useState(true);

  const truncatedText = isTruncated ? text.slice(0, limit) : text;

  const toggleTruncate = () => {
    setIsTruncated(!isTruncated);
  };

  return (
    <div className="max-h-32 overflow-auto">
      <p>{truncatedText}</p>
      {text.length > limit && (
        <button onClick={toggleTruncate} className="text-blue-500 underline">
          {isTruncated ? 'Read more' : 'Read less'}
        </button>
      )}
    </div>
  );
};

export default TruncateText;
