try:
  from couchbase.cluster import Cluster, PasswordAuthenticator
  from couchbase.n1ql import N1QLQuery
except DeprecationWarning as e:
  print('Importing Couchbase caused deprecation warning')

# Test UUID Generation for Couchbase ID insertion:
# from uuid import uuid4 as guid
# print( '\n---\nGUID:', str(guid()), "\n---\n" )

# Connect to Couchbase Cluster and Bucket:
try:
  cluster = Cluster('couchbase://127.0.0.1')
  password_auth = PasswordAuthenticator('bigman', 'password')
  cluster.authenticate(password_auth)
  bucket = cluster.open_bucket('playtime')
except: 
  print('Unable to connect to Couchbase Server')
  exit(1)

# Upsert Data Set:
# knights = {
#   'arthur': {'name': 'Arthur', 'occupation': 'King of the Britains', 'status': 'not dead yet', 'email': 'kingarthur@roundtable.co.uk', 'interests': ['Holy Grail', 'Swallows']},
#   'bedevere': {'name': 'Sir Bedevere', 'email': 'sirbedevere@weighsandmeans.co.uk', 'interests': ['Justice', 'Witches', 'Ducks', 'Castle Ooooh', 'Holy Grail']},
#   'galahad': {'name': 'Sir Galahad', 'interests': ['Young Women', 'Holy Grail']},
#   'robin': {'name': 'Brave Sir Robin', 'quest': 'Shrubbery', 'email': 'nightsofninomore@roundtable.co.uk', 'interests': ['Shrubberies', 'Cowardice']}
# }
# for k, data in knights.items():
#   bucket.upsert("knight_"+k, data)

# Look up document by ID:
result = bucket.get('knight_arthur').value
print('Arthur:', result)

# Query and iterate over data set:
# bucket.n1ql_query('CREATE PRIMARY INDEX ON bucket-name').execute()
rows = bucket.n1ql_query(N1QLQuery('SELECT * FROM playtime as knight WHERE $1 in interests', 'Holy Grail'))
for row in rows: print(row)
