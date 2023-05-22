from .config import ac, client
from rest_framework.views import APIView
from redisearch.query import Query
from rest_framework.response import Response

# Create your views here. 
class SearchViewView(APIView):
    http_method_names = ('get',)
    
    def get(self, request):
        search = request.query_params.get('search')
        language = request.query_params.get('language', 'english')
        result = {}

        if search:
            search = search.strip()
            language = language.lower()
            if language == 'nepali':
                q = Query(f'@nepali_name:{search}*')

                res = client.search(q)     
                result = set([doc_id.nepali_name for doc_id in res.docs])
            else:
                q = Query(f'@english_name:{search}*')

                res = client.search(q)     
                result = set([doc_id.english_name for doc_id in res.docs])

        return Response({'result':result})
       
class AutocompletedViewView(APIView):
    http_method_names = ('get',)
    
    def get(self, request):
        search = request.query_params.get('search')
        result = {}

        if search:
            search = search.strip()

            # Getting suggestions
            result = [i.string for i in ac.get_suggestions(search, fuzzy = True)]

        return Response({'result':result})
