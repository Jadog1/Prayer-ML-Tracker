// src/components/Sidebar.tsx

import React, { useEffect, useState } from 'react';
import { Groups } from '../api/contacts';

function Sidebar() {
  const [groups, setGroups] = useState<Groups>(new Groups());
  
  useEffect(() => {
    (async () => {
      try {
        let newGroups = await groups.all();
        setGroups(newGroups);
      } catch (error: any) {
        console.error(error);
      }
    })();
  }, []);

  return (
    <div className="w-1/4 mr-4">
      <p className="text-lg font-semibold mb-2">Groups</p>
      <ul>
        {groups.groups.map((group) => (
          <li key={group.id} className="mb-2">
            {group.name}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Sidebar;
