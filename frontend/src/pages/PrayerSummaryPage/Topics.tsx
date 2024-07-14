import { PrayerSummary } from "../../api/prayerSummary";
import Badge from "../../components/Badge"


type topicProps = {
    summary: PrayerSummary;
}
// Using Badges, display the topics in the summary
function Topics(props: topicProps) {
    return (
        <div className="flex flex-col">
            <p className="text-lg font-semibold mb-2">Topics</p>
            <div>
                {props.summary.topics.TopK(5).map((topic, index) => (
                    <>
                    <Badge key={index} text={topic.name} color={getColor(index)} 
                        className='mb-2' />
                    <br />
                    </>
                ))}
            </div>
        </div>
    );
}

function getColor(index: number) {
    const colors = ["green", "blue", "red", "yellow", "purple"];
    return colors[index % colors.length];
}

export { Topics }