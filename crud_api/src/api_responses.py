import json
from typing import Dict
from http import HTTPStatus
from fastapi import Response


def bad_request_response(json_response: Dict, custom_headers: Dict) -> Response:
    return Response(
        status_code=HTTPStatus.BAD_REQUEST,
        content=json.dumps(json_response, default=str),
        headers={"Content-Type": "application/json"}.update(custom_headers)
    )


def success_response(json_response: Dict, custom_headers: Dict) -> Response:
    return Response(
        status_code=HTTPStatus.OK,
        content=json.dumps(json_response, default=str),
        headers={"Content-Type": "application/json"}.update(custom_headers)
    )


def server_error_response(json_response: Dict, custom_headers: Dict) -> Response:
    return Response(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        content=json.dumps(json_response, default=str),
        headers={"Content-Type": "application/json"}.update(custom_headers)
    )


def not_found_response(json_response: Dict, custom_headers: Dict) -> Response:
    return Response(
        status_code=HTTPStatus.NOT_FOUND,
        content=json.dumps(json_response, default=str),
        headers={"Content-Type": "application/json"}.update(custom_headers)
    )
