# Token
TOKEN = 'TOKEN'

# group information
group = {'admin': {'id': -100123456789},
         'pixel': {'id': -100123456789, 'main_topic': 654321},
         'macos': {'id': -100123456789},
         'foss': {'id': -100123456789},
         'test': {'id': -100123456789}}

allowed_group = []
for item in group.items():
    allowed_group.append(item[1]['id'])
