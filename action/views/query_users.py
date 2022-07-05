from django.http import JsonResponse
from rest_framework import status

from rest_framework.request import Request
from rest_framework.views import APIView

from action import client
from action.script import query_executor, query_checker


class QueryUsers(APIView):  # BaseApiView

    def post(self, request: Request, *args, **kwargs) -> JsonResponse:
        # Get the text from the request
        data = request.data
        text = data.get('text')
        print('Arrived to the query users view')

        if len(text) == 0:
            client.chat_postMessage(channel='#test', text="Please, provide the query")

        else:
            # Create what needed to perform query
            query = text.split()

            client.chat_postMessage(channel='#test', text='Query check and perform is started')

            # Check if the query is valid
            valid, explaination = query_checker(query)

            print(valid, explaination)

            if valid and False:
                # Perform the query
                result = query_executor(query)

                # Send the result to the channel
                client.chat_postMessage(channel='#test', text=result)
            else:
                client.chat_postMessage(channel='#test', text=f'Error:{explaination}')

        return JsonResponse({'data': 'query_user', 'status': status.HTTP_200_OK, 'text': text})