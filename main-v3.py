try:
  from couchbase.cluster import Cluster, ClusterOptions
  from couchbase_core.cluster import PasswordAuthenticator
  from couchbase_core.n1ql import N1QLQuery
except DeprecationWarning as e:
  print('Importing Couchbase caused deprecation warning')

# Test UUID Generation for Couchbase ID insertion:
from uuid import uuid4 as guid
print( '\n---\nGUID:', str(guid()), "\n---\n" )

# Connect to Couchbase Cluster and Bucket:
try:
  password_auth = PasswordAuthenticator('bigman', 'password')
  cluster = Cluster('couchbase://127.0.0.1', ClusterOptions(password_auth))
  bucket = cluster.bucket('playtime')
  collection = bucket.default_collection()
except: 
  print('Unable to connect to Couchbase Server')
  exit(1)

# Upsert Data Set:
knights = {
  'arthur': {'name': 'Arthur', 'occupation': 'King of the Britains', 'status': 'not dead yet', 'email': 'kingarthur@roundtable.co.uk', 'interests': ['Holy Grail', 'Swallows']},
  'bedevere': {'name': 'Sir Bedevere', 'email': 'sirbedevere@weighsandmeans.co.uk', 'interests': ['Justice', 'Witches', 'Ducks', 'Castle Ooooh', 'Holy Grail']},
  'galahad': {'name': 'Sir Galahad', 'interests': ['Young Women', 'Holy Grail']},
  'robin': {'name': 'Brave Sir Robin', 'quest': 'Shrubbery', 'email': 'nightsofninomore@roundtable.co.uk', 'interests': ['Shrubberies', 'Cowardice']}
}
for k, data in knights.items():
  collection.upsert("knight_"+k, data)

# Look up document by ID:
result = collection.get('knight_arthur')
print('Arthur:', result)

# Query and iterate over data set:
rows = cluster.query(N1QLQuery('SELECT meta() AS meta, name, email FROM playtime WHERE $interest IN interests', interest='Holy Grail'))
for row in rows: print(row)

