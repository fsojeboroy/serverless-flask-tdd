from flask_accepts import accepts
from flask_accepts.utils import for_swagger, ma_field_to_reqparse_argument
from flask_restx.swagger import parse_docstring

from app_context import api, ma


def to_swagger_model(api, ma_schema, model_name=None):
    return for_swagger(api=api, schema=ma_schema, model_name=model_name,
                       operation='dump')


class RequestWrapper:
    """Deserialize request, serialize response, and manage swagger documentation.
    @decorator class for flask_restx Resource methods that will deserialize
    query parameters and payloads then serialize the response.
    Also responsible for swagger documentation.

    Attributes:
        query_params_schema (marshmallow.Schema): request query parameter
            schema.
        schema (marshmallow.Schema): request payload schema.
        response_schema (marshmallow.Schema): response schema.
        swagger_model (flask_restx.model.Model): expected response for swagger
            documentation.
        params (dict): dictionary of query parameters for swagger documentation
        body (flask_restx.model.Model): payload for swagger documentation.

    Returns:
        A json serialized from response_schema (if supplied) of the result of
        the function to be decorated.
    """

    def __init__(self, query_params_schema=None, schema=None,
                 response_schema=None, success_code=200):
        self.query_params_schema = query_params_schema
        self.schema = schema
        self.response_schema = response_schema
        self.swagger_model = to_swagger_model(
            api, response_schema) if response_schema else None
        self.params = {
            k: {**ma_field_to_reqparse_argument(v),
                "location": "values"}
            for k, v in query_params_schema.fields.items()} \
            if query_params_schema else {}
        if self.params:
            for _k, v in self.params.items():
                v['type'] = str(v['type'])
        self.body = for_swagger(schema, api) if schema else {}
        self.success_code = success_code

    def __call__(self, func, *args, **kwargs):
        """Decorator function
        Returns the serialized value of method if response_schema is supplied.
        """

        parsed_docstring = parse_docstring(func)
        description = parsed_docstring.get('details')
        summary = parsed_docstring.get('summary')

        @accepts(
            query_params_schema=self.query_params_schema,
            schema=self.schema,
            api=api
        )
        @api.doc(params=self.params, body=self.body,
                 description=description if description else '',
                 summary=summary if summary else '')
        @api.response(self.success_code, 'Success', self.swagger_model)
        def inner(*args, **kwargs):
            response = func(*args, **kwargs)
            return self.response_schema.dump(response) \
                if self.response_schema else response
        return inner
