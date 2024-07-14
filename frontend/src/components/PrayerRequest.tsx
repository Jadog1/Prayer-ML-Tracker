import { PrayerRequest } from "../api/prayerRequests";

type PrayerRequestProps = {
    prayerRequest: PrayerRequest;
    showEmotion?: boolean;
    showSentiment?: boolean;
    showClassification?: boolean;
    showGroup?: boolean;
    showName?: boolean;
    showTopics?: boolean;
}
