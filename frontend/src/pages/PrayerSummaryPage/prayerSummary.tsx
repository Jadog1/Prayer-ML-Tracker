import React, { useEffect, useState } from 'react';
import Header from '../../components/Header';
import Sidebar from './Sidebar';
import { PrayerSummary } from '../../api/prayerSummary';
import { PrayerSummaryList } from '../../components/PrayerList';
import { Topics } from './Topics';

type PrayerSummaryContentProps = {
}
function PrayerSummaryContent(props: PrayerSummaryContentProps) {
  const [summary, setSummary] = useState<PrayerSummary>(new PrayerSummary());
    return (
        <div className="flex">
          <Sidebar setSummary={setSummary} />
          <PrayerSummaryBody summary={summary} />
          <Topics summary={summary} />
        </div>
      );
}

function PrayerSummaryBody(props: {summary: PrayerSummary}) {
  return (
    <>
      <PrayerSummaryList summary={props.summary} />
    </>
  );
}

export default PrayerSummaryContent;