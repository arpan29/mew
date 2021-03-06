from rest_framework import status
from rest_framework.response import Response


class APIResponse():

    @staticmethod
    def send(data, code=status.HTTP_200_OK, error=""):
        """Overrides rest_framework response

            :param data: data to be send in response
            :param code: response status code(default has been set to 200)
            :param error: error message(if any, not compulsory)
        """
        res = {"error": error, "response": data}
        return Response(data=res, status=code)


class Includes():

    def get_include_list(self, request):
        include = request.GET.get('include', '')
        return include.split(',')
