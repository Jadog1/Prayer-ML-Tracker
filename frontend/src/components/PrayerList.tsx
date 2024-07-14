
// PrayerList is a function that gives a tabular view of all the existing prayer requests
// If a prayer request exceeds 100 characters, it is truncated and an ellipsis is added to the end
// With the ability to see the full prayer request by clicking on the truncated text
// The prayer requests are sorted by the date they were created
// The user can also archive a prayer request by clicking on the delete button
// It takes the loaded prayer requests as props
// As props, it also has id and setId which are used to set the id of the prayer request

import { PrayerRequest, PrayerRequestID } from "../api/prayerRequests";
import { PrayerSummary } from "../api/prayerSummary";
import PrayerRequestCard from "./PrayerRequest";
import TruncateText from "./TruncateText";

type PrayerListProps = {
    requests: PrayerRequest[];
    id: PrayerRequestID;
    editRecord: (id: PrayerRequestID) => void;
    delete: (prayerRequest: PrayerRequest) => void;
};
function PrayerList(props: PrayerListProps) {
    const deleteRequest = (prayerRequest: PrayerRequest) => {
        if (window.confirm('Are you sure you want to delete this prayer request?')) {
            props.delete(prayerRequest);
        }
    }

    return (
        <div className="text-center">
            <table className="w-full h-full overflow-auto">
                <thead>
                    <tr>
                        <th className="text-center">Date</th>
                        <th className="text-center">Sentiment</th>
                        <th className="text-center">Prayer Request</th>
                        <th className="text-center">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {props.requests.map((prayerRequest) => (
                        <tr key={prayerRequest.id} className="border-t" style={{ height: '75px' }}>
                            <td className="p-2">
                                {new Date(prayerRequest.created_at).toLocaleDateString()}
                            </td>
                            <td className="p-2">
                                {prayerRequest.prayer_type} <br />
                                {prayerRequest.emotion} <br />
                                {prayerRequest.sentiment}
                            </td>
                            <td className="p-2">
                                <TruncateText text={prayerRequest.request} limit={100} />
                            </td>
                            <td className="p-2 text-right">
                                <button onClick={() => props.editRecord(prayerRequest.id)} className="text-blue-500 mb-2">Edit</button>
                                <button onClick={() => deleteRequest(prayerRequest)} className="text-red-500 ml-2">Delete</button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

function PrayerSummaryList(props: { summary: PrayerSummary }) {
    return (
        <div className="p-2 mb-2 space-y-2">
            {
                props.summary.prayers.map((prayerRequest: PrayerRequest) => (
                    <PrayerRequestCard prayerRequest={prayerRequest} showClassification showEmotion
                        showGroup showName showSentiment showTopics/>
                ))
            }
        </div>
    )
}

export { PrayerSummaryList }

export default PrayerList;