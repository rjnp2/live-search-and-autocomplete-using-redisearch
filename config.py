from redis import ResponseError
from redisearch import AutoCompleter, Client, IndexDefinition, TextField

index_definition = IndexDefinition(prefix=['doc:'])
client = Client('index-document')

SCHEMA = (
  TextField('english_name'),
  TextField('nepali_name'),
)

try:
  client.info()
except ResponseError:
    # Index does not exist. We need to create it!
    client.create_index(SCHEMA, definition=index_definition)

ac = AutoCompleter('ac')
