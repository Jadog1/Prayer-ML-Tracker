from abc import ABC, abstractmethod
from ..dto.prayerRequests import PrayerRequest, PrayerRequests
from ..dto.topic import Topic, Topics
from typing import List, Union
from sqlalchemy.orm import scoped_session, Session
from .orm import ContactORM, PrayerRequestORM, LinkORM, prayerColumnsExceptEmbeddings, TopicORM, PrayerTopicsORM
from ..models.models import ClassifierModels, EmbeddingResult, Embeddings
from sqlalchemy.sql import text
from sqlalchemy import func, and_, case
import numpy as np

class PrayerRequestRepo(ABC):
    @abstractmethod
    def get(self, account_id:int, request_id:int)->PrayerRequest:
        pass

    @abstractmethod
    def get_all(self, account_id:int)->PrayerRequests:
        pass

    @abstractmethod
    def get_contact(self, account_id:int, contact_id: int)->PrayerRequests:
        pass

    @abstractmethod
    def get_daterange(self, account_id:int, start:str, end:str)->PrayerRequests:
        pass

    @abstractmethod
    def save(self, account_id:int, request: PrayerRequest)->PrayerRequest:
        pass

    @abstractmethod
    def update(self, account_id:int, request: PrayerRequest)->PrayerRequest:
        pass

    @abstractmethod
    def delete(self, account_id:int, request_id: int):
        pass

    @abstractmethod
    def link_requests(self, account_id:int, id_from:int, id_to:int):
        pass

    @abstractmethod
    def get_similar_requests(self, account_id:int, request: PrayerRequest)->PrayerRequests:
        pass
        
class PrayerRequestRepoImpl(PrayerRequestRepo):
    def __init__(self, session: scoped_session[Session], model: Embeddings, classifierModels: ClassifierModels):
        self.pool = session
        self.model = model
        self.classifierModels = classifierModels

    def get(self, account_id:int, request_id:int, include_embeddings=False)->PrayerRequest:
        with self.pool() as session:
            request = session.query(PrayerRequestORM).filter(PrayerRequestORM.account_id == account_id, PrayerRequestORM.id == request_id).first()
            if not request:
                raise ValueError(f"Prayer request with id {request_id} does not exist")
            return PrayerRequest(request, includeEmbeddings=include_embeddings)

    def get_all(self, account_id:int)->PrayerRequests:
        with self.pool() as session:
            requests = session.query(PrayerRequestORM).filter(PrayerRequestORM.account_id == account_id).all().sort(PrayerRequestORM.created_at.desc())
            return self._to_prayer_requests(requests)

    def get_contact(self, account_id:int, contact_id: int)->PrayerRequests:
        with self.pool() as session:
            requests = session.query(PrayerRequestORM).filter(
                PrayerRequestORM.account_id == account_id, PrayerRequestORM.contact_id == contact_id
                ).order_by(PrayerRequestORM.created_at.desc()).all()
            return self._to_prayer_requests(requests)
        
    def get_linked_requests(self, account_id:int, request_id:int, link_id:int)->PrayerRequests:
        with self.pool() as session:
            requests = session.query(PrayerRequestORM).filter(
                PrayerRequestORM.account_id == account_id, 
                PrayerRequestORM.link_id == link_id, 
                PrayerRequestORM.id != request_id
                ).order_by(PrayerRequestORM.created_at.desc()).all()
            return self._to_prayer_requests(requests)
        
    def get_group_session_topics(self, prayer_request_ids:List[int])->Topics:
        with self.pool() as session:
            query = session.query(TopicORM).join(PrayerTopicsORM).filter(PrayerTopicsORM.prayer_request_id.in_(prayer_request_ids))
            topics = query.all()
            return self._to_topics(topics)

    def get_group_session(self, account_id:int, start_date:str, end_date:str, group_id:int)->PrayerRequests:
        with self.pool() as session:
            sentiment_case = case(
                (PrayerRequestORM.sentiment_analysis == 'negative', -1),
                (PrayerRequestORM.sentiment_analysis == 'neutral', 0),
                (PrayerRequestORM.sentiment_analysis == 'positive', 1),
                else_=None
            ).label('sentiment_number')

            prayer_case = case(
                (PrayerRequestORM.prayer_type == 'Prayer Request', -1),
                (PrayerRequestORM.prayer_type == 'Praise', 1)
            ).label('prayer_number')

            # Create the main query with joins and conditions
            query = session.query(
                PrayerRequestORM.id,
                sentiment_case,
                prayer_case,
            ).filter(
                PrayerRequestORM.created_at.between(start_date, end_date),
                PrayerRequestORM.account_id == account_id
            )
            
            # Add the group_id filter conditionally
            if group_id is not None:
                query = query.join(PrayerRequestORM.contact).filter(ContactORM.group_id == group_id)
            
            # Use subquery to mimic the CTE
            subquery = query.subquery()

            # Final query to select from the subquery and order by sentiment_number + prayer_number
            final_query = session.query(
                PrayerRequestORM
            ).join(
                subquery, subquery.c.id == PrayerRequestORM.id
            ).order_by(
                (subquery.c.sentiment_number + subquery.c.prayer_number).asc()
            )

            requests = final_query.all()
            return self._to_prayer_requests(requests)

    def get_daterange(self, account_id:int, start:str, end:str)->PrayerRequests:
        with self.pool() as session:
            requests = session.query(PrayerRequestORM).filter(
                PrayerRequestORM.account_id == account_id, 
                PrayerRequestORM.created_at >= start, PrayerRequestORM.created_at <= end).all()
            return self._to_prayer_requests(requests)

    def save(self, account_id:int, request: PrayerRequest)->PrayerRequest:
        with self.pool() as session:
            request.account_id = account_id
            ormRequest = PrayerRequestORM(
                id=request.id, account_id=account_id, contact_id=request.contact_id, 
                request=request.request, archived_at=request.archived_at)
            self._set_embeddings(ormRequest)
            # if request.request != "":
            #     self._build_prayer_topics(session, ormRequest.id, embeddings)
            session.add(ormRequest)
            session.commit()
            session.refresh(ormRequest)
            return PrayerRequest(ormRequest)
        
    def update(self, account_id:int, request: PrayerRequest)->PrayerRequest:
        with self.pool() as session:
            ormRequest = session.query(PrayerRequestORM).filter(PrayerRequestORM.account_id == account_id, PrayerRequestORM.id == request.id).first()
            ormRequest.request = request.request
            ormRequest.archived_at = request.archived_at
            embeddings = self._set_embeddings(ormRequest)
            self._rebuild_prayer_topics(session, request.id, embeddings)
            self._set_classifications(ormRequest)
            session.commit()
            session.refresh(ormRequest)
            return PrayerRequest(ormRequest)

    def _set_embeddings(self, prayer_request: PrayerRequestORM):
        embeddings = self.model.calculate_embeddings(prayer_request.request)
        prayer_request.gte_base_embedding = embeddings.get_gte_base()
        prayer_request.msmarco_base_embedding = embeddings.get_msmarco_base()
        return embeddings

    def _set_classifications(self, prayer_request: PrayerRequestORM):
        classifications = self.classifierModels.classify(prayer_request.request)
        prayer_request.prayer_type = classifications.get('prayerType')
        prayer_request.sentiment_analysis = classifications.get('sentiment')
        prayer_request.emotion_roberta = classifications.get('emotion')

    def _rebuild_prayer_topics(self, session: Session, request_id, embeddings: EmbeddingResult):
        # Delete existing prayerTopics that are related to the prayer request
        session.query(PrayerTopicsORM).filter(PrayerTopicsORM.prayer_request_id == request_id).delete()
        self._build_prayer_topics(session, request_id, embeddings)

    def _build_prayer_topics(self, session: Session, request_id, embeddings: EmbeddingResult):
        query = session.query(TopicORM).order_by(TopicORM.gte_base_embedding.cosine_distance(embeddings.get_gte_base())).limit(5)
        topics = query.all()
        for topic in topics:
            session.add(PrayerTopicsORM(prayer_request_id=request_id, topic_id=topic.id))
        
    def link_requests(self, account_id:int, id_from:int, id_to:int):
        with self.pool() as session:
            request_to = session.query(PrayerRequestORM).filter(PrayerRequestORM.account_id == account_id, PrayerRequestORM.id == id_to).first()
            request_from = session.query(PrayerRequestORM).filter(PrayerRequestORM.account_id == account_id, PrayerRequestORM.id == id_from).first()
            if not request_to or not request_from:
                raise ValueError(f"One of the prayer requests does not exist or was not saved properly")
            if request_to.link_id:
                request_from.link_id = request_to.link_id
            else:
                link = LinkORM()
                session.add(link)
                session.flush()
                request_from.link_id = link.id
                request_to.link_id = link.id
            session.commit()

    def delete(self, account_id:int, id:int):
        with self.pool() as session:
            session.query(PrayerRequestORM).filter(PrayerRequestORM.account_id == account_id, PrayerRequestORM.id == id).delete()
            session.commit()

    def get_similar_requests(self, account_id:int, request: Union[int, PrayerRequest])->PrayerRequests:
        with self.pool() as session:
            request_id = request if type(request) is int else request.id
            loadedPrayerRequest = session.query(PrayerRequestORM).filter(PrayerRequestORM.id == request_id).first()
            
            # Use coalesce to group by link_id if not null, otherwise by id
            group_by_column = func.coalesce(PrayerRequestORM.link_id, PrayerRequestORM.id)
            
            # Subquery to get the most recent row for each group
            subquery = session.query(
                func.max(PrayerRequestORM.id).label('max_id')
            ).filter(
                PrayerRequestORM.account_id == account_id,
                PrayerRequestORM.id != request_id,
                PrayerRequestORM.contact_id == loadedPrayerRequest.contact_id,
                PrayerRequestORM.archived_at == None
            ).group_by(
                group_by_column
            ).subquery()
            
            # Main query to get the rows matching the max_id from the subquery
            query = session.query(
                PrayerRequestORM
            ).join(
                subquery, subquery.c.max_id == PrayerRequestORM.id
            ).order_by(
                PrayerRequestORM.gte_base_embedding.cosine_distance(loadedPrayerRequest.gte_base_embedding)
            ).limit(5)
            
            requests = query.all()
            return self._to_prayer_requests(requests)
        
        
    def avg_linked_topics(self, account_id:int, request_id:int):
        with self.pool() as session:
            params = {"account_id": account_id, "request_id": request_id}
            query = """
                with prayer as (
                    select id, link_id
                    from prayer_request pr
                    where pr.id = :request_id and pr.account_id = :account_id
                )

                , linked_avg as (
                    select AVG(pr2.gte_base_embedding) as embedding
                    from prayer pr
                    inner join prayer_request pr2 on pr2.id = pr.id 
                        or (pr.link_id is not null AND pr2.link_id = pr.link_id)
                    group by pr2.link_id
                )

                select t.name, t.id, 1 - (t.gte_base_embedding <=> la.embedding) as score
                from topic t
                cross join linked_avg la
                order by score desc
                limit 5;
            """
            results = session.execute(text(query), params)
            return results.mappings().all()

    def _to_prayer_requests(self, requests: List[PrayerRequestORM])->PrayerRequests:
        prayer_requests = PrayerRequests()
        for request in requests:
            prayer_requests.add(PrayerRequest(request))
        return prayer_requests
    
    def _to_topics(self, topics: List[TopicORM])->List[Topic]:
        topicsList = Topics()
        for topic in topics:
            topicsList.add(Topic(topic))
        return topicsList