# Token
TOKEN = 'TOKEN'

# group information
group = {'admin': {'id': -100123456789},
         'pixel': {'id': -100123456789, 'main_topic': 654321},
         'macos': {'id': -100123456789},
         'foss': {'id': -100123456789},
         'test': {'id': -100123456789}}

# list of groups with privacy enabled privacy mode
enabled_privacy_group = [-100123456789]
delete_after = 10 # hours

allowed_group = []
for item in group.items():
    allowed_group.append(item[1]['id'])
