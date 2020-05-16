from pyathena import connect
from django.conf import settings


class AthenaClient():

    @staticmethod
    def __init__(self):
        self.cursor = connect(
            aws_access_key_id=settings.EXTERNAL_SERVICES["AWS"]["ATHENA"]["ACCESS_KEY"],
            aws_secret_access_key=settings.EXTERNAL_SERVICES["AWS"]["ATHENA"]["SECRET_KEY"],
            region_name=settings.EXTERNAL_SERVICES["AWS"]["ATHENA"]["REGION_NAME"],
            s3_staging_dir=settings.EXTERNAL_SERVICES["AWS"]["ATHENA"]["STAGING_DIR"]
        ).cursor()

    def fetch_query_results(self, query):
        self.cursor.execute(query)
        return self.cursor
