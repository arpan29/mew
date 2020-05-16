from rest_framework.views import APIView
from mew.core.utils import APIResponse


class RUOK(APIView):
    """
    """

    def get(self, request):
        return APIResponse.send({"message": "imok"})
