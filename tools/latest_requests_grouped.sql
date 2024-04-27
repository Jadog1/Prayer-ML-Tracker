with prayers as (
	Select c.name || ': \n' || string_agg(pr.request, '\n\n') as prayer
	from prayer_request pr
	inner join contact c on c.id = pr.contact_id
	where pr.created_at::date = '04/15/24'
	group by c.name
)
select string_agg(prayer, '\n --- \n')
from prayers;