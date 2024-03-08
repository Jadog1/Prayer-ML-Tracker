from ..repo.orm import OpenPool
from ..repo.prayerRequests import PrayerRequestRepoImpl
from ..repo.contacts import ContactRepoImpl
from ..dto.groups import Group
import os
from dotenv import load_dotenv
load_dotenv()
pg_uri = os.environ.get('PRAYERS_PG_DATABASE_URL')

# Replace Account with the actual class name for the user model
user_id = 1
pool = OpenPool(pg_uri)
prayerRepo = PrayerRequestRepoImpl(pool)
contactRepo = ContactRepoImpl(pool)

import pandas as pd 
import json

# Load json object, and get the Categories array to use as a dataframe
with open('src/scraped_data/Prayermate.json') as f:
    data = json.load(f)
    categories = data['Categories']

prayerRequests = []
for category in categories:
    for subject in category['subjects']:
        for prayerRequest in subject['cards']:
            prayerRequests.append({
                'category': category['name'],
                'subject': subject['name'],
                'prayerRequest': prayerRequest['text'],
                'archivedDate': prayerRequest['archivedDate'] if prayerRequest['archived'] else None,
                'stackGroup': prayerRequest['stackGroup'],
            })

df = pd.DataFrame(prayerRequests)

groups = df['category'].unique()
for group in groups:
    group = Group().from_dict({'name': group})
    contactRepo.save_group(user_id, group)

from ..dto.contacts import Contact
all_groups = contactRepo.get_groups(user_id).to_dataframe()
contacts = df.groupby(['category', 'subject']).size().reset_index(name='counts')
for index, row in contacts.iterrows():
    group = all_groups[all_groups['name'] == row['category']]
    group_id = group['id'].values[0]
    contact = Contact().from_dict({'name': row['subject'], 'group_id': int(group_id)})
    contactRepo.save_contact(user_id, contact)

from ..dto.prayerRequests import PrayerRequest, PrayerRequests
from ..dto.link import Link
# Create a dataframe to map stackGroup to a unique integer link_id, order by stackGroup
# Also create a column count to keep track of the number of prayer requests in each stackGroup
stackGroups = df['stackGroup'].unique()
stackGroups = pd.DataFrame(stackGroups, columns=['stackGroup']).sort_values(by='stackGroup')
stackGroups['count'] = df.groupby('stackGroup').size().reset_index(name='counts')['counts']
stackGroups = stackGroups[stackGroups['count'] > 1]
stackGroups.reset_index(inplace=True)
stackGroups['link_id'] = stackGroups.index + 1

for index, row in stackGroups.iterrows():
    link = Link().from_dict({'id': row['link_id']})
    prayerRepo.save_link(link.id)


from ..dto.prayerRequests import PrayerRequest, PrayerRequests
from ..repo.prayerRequests import PrayerRequestRepoImpl
from ..dto.contacts import Contact
from ..repo.orm import ContactORM
contacts = df.groupby(['category', 'subject']).size().reset_index(name='counts')
with pool() as session:
    for index, row in df.iterrows():
        contactOrm = session.query(ContactORM).filter(ContactORM.name == row['subject'] and ContactORM.group.name == row['category']).first()
        contact_id = contactOrm.id
        stackGroupRow = stackGroups[stackGroups['stackGroup'] == row['stackGroup']]
        link_id = None if stackGroupRow.empty else int(stackGroupRow['link_id'].values[0])
        prayerRequest = PrayerRequest().from_dict({
            'contact_id': int(contact_id),
            'request': row['prayerRequest'],
            'archived_at': row['archivedDate'],
            'link_id': link_id
        })
        prayerRepo.save(user_id, prayerRequest)