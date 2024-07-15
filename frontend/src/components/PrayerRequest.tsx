import { PrayerRequest } from "../api/prayerRequests";
import React, { useEffect, useState } from 'react';
import Badge from './Badge'; // Import your custom Badge component
import TruncateText from "./TruncateText";
import { ErrorHandlerContext } from "../prayerRequests";

type PrayerOpts = {
    showEmotion?: boolean;
    showSentiment?: boolean;
    showClassification?: boolean;
    showGroup?: boolean;
    showName?: boolean;
    showTopics?: boolean;
    headerChildren?: React.ReactNode;
}

type PrayerRequestProps = {
    prayerRequest: PrayerRequest;
} & PrayerOpts;

const PrayerRequestCard: React.FC<PrayerRequestProps> = ({ prayerRequest, ...opts }) => {
    const [activeTab, setActiveTab] = useState<'prayer' | 'related'>('prayer');
    const setErrorText = React.useContext(ErrorHandlerContext);

    const handleTabClick = (tab: 'prayer' | 'related') => {
        setActiveTab(tab);
    };

    useEffect(() => {
        (async () => {
            if (activeTab === 'related' && prayerRequest.links.length === 0) {
                try {
                    await prayerRequest.getLinks();
                } catch (error: any) {
                    console.error(error);
                    setErrorText(error.message);
                }
            }
        })()
    }, [activeTab]);

    const renderFooter = () => (
        <div className="flex space-x-2 mt-2 border-t border-gray-200 bg-gray-50 p-2">
            {opts.showEmotion && <Badge text={prayerRequest.emotion} color="blue" small />}
            {opts.showSentiment && <Badge text={prayerRequest.sentiment} color="blue" small />}
            {opts.showClassification && <Badge text={prayerRequest.prayer_type} color="blue" small />}
            <br />
            {opts.showTopics && prayerRequest.topics.map(topic => <Badge key={topic} text={topic} color="green" small />)}
        </div>
    );

    const dateStr = new Date(prayerRequest.created_at).toLocaleDateString();
    const renderContent = () => (
        <div className="p-1 bg-white rounded-lg md:p-3 dark:bg-gray-800">
            <div className="text-sm text-gray-500 dark:text-gray-400 float-right">{dateStr}</div>
            {opts.showGroup && <span className="text-sm text-gray-500 dark:text-gray-400 mr-2 float-left">{prayerRequest.contact.group.name}</span>}
            {opts.showName && <span className="text-sm text-gray-900 dark:text-white mr-2 float-left">{prayerRequest.contact.name}</span>}
            <br />
            <TruncateText text={prayerRequest.request} limit={200} />
        </div>
    );

    return (
        <div className="w-full bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700">
            <div className="text-gray-500 border-b border-gray-200 rounded-t-lg bg-gray-100 dark:border-gray-700 dark:text-gray-400 dark:bg-gray-800 flex">
                <ul className="flex flex-wrap text-sm font-medium text-center">
                    <li className="me-2">
                        <button
                            onClick={() => handleTabClick('prayer')}
                            className={`inline-block p-4 rounded-ss-lg hover:bg-gray-100 dark:bg-gray-800 dark:hover:bg-gray-700 ${activeTab === 'prayer' ? 'text-blue-600 dark:text-blue-500' : ''}`}
                        >
                            Prayer
                        </button>
                    </li>
                    <li className="me-2">
                        <button
                            onClick={() => handleTabClick('related')}
                            className={`inline-block p-4 hover:bg-gray-100 dark:bg-gray-800 dark:hover:bg-gray-700 ${activeTab === 'related' ? 'text-blue-600 dark:text-blue-500' : ''}`}
                        >
                            Related
                        </button>
                    </li>
                </ul>
                <span className="ml-auto p-2 me-2">
                    {opts.headerChildren}
                </span>
            </div>
            <div>
                {activeTab === 'prayer' && renderContent()}
                {renderFooter()}
                {activeTab === 'related' && (
                    <div className="p-4 bg-white rounded-lg md:p-8 dark:bg-gray-800">
                        {prayerRequest.links.map(link => (
                            <div key={link.id}>
                                <PrayerRequestCard prayerRequest={link} {...opts} />
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};

export default PrayerRequestCard;
