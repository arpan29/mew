import jsonschema
import logging

from orb.core.exceptions import InvalidInputException


class BaseValidator():

    def validate(self):
        raise NotImplementedError("Validate method is not implemented.")


class RequestValidator(BaseValidator):

    schema = None

    def validate(self, data):
        if not self.schema:
            raise InvalidInputException("Validator Schema is missing.")
        validator = jsonschema.Draft7Validator(self.schema)
        errors = validator.iter_errors(data)
        error_info = []
        for error in errors:
            if hasattr(error, "message"):
                error_info.append(error.message)

        if error_info:
            raise InvalidInputException("Request Validation Failed.", error_info)

        logging.info("Request JSON Schema Validated.")
        return True
