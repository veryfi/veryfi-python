class VeryfiClientError(Exception):
    optional_fields = ["error", "code"]

    def __init__(self, raw_response, **error_info):
        for field_name in self.optional_fields:
            setattr(self, field_name, error_info.get(field_name))

        self.raw_response = raw_response
        self.status = raw_response.status_code

        if getattr(self, "error"):
            super().__init__(f"{self.status}, {getattr(self, 'error')}")

    @staticmethod
    def from_response(raw_response):
        """Veryfi API returns error messages with a json body
        like:
        {
            'status': 'fail',
            'error': 'Human readable error description.'
        }
        """
        error_cls = _error_map.get(raw_response.status_code) or VeryfiClientError
        return error_cls(raw_response, **raw_response.json())


class UnauthorizedAccessToken(VeryfiClientError):
    pass


class BadRequest(VeryfiClientError):
    pass


class ResourceNotFound(VeryfiClientError):
    pass


class UnexpectedHTTPMethod(VeryfiClientError):
    pass


class AccessLimitReached(VeryfiClientError):
    pass


class InternalError(VeryfiClientError):
    pass


_error_map = {
    400: BadRequest,
    404: ResourceNotFound,
    401: UnauthorizedAccessToken,
    405: UnexpectedHTTPMethod,
    409: AccessLimitReached,
    500: InternalError,
}
