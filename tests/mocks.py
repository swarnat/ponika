"""Reusable mock response templates and helpers."""

import json
import responses
from typing import Any, Dict, Callable

# Base URL for mocked API
BASE_URL = "https://test-device:443/api"

# Standard responses
LOGIN_RESPONSE = {
    "success": True,
    "data": {
        "username": "admin",
        "token": "test-token-123",
        "expires": 3600
    }
}

LOGOUT_RESPONSE = {
    "success": True,
    "data": {
        "response": "Logged out successfully"
    }
}

# Error responses
ERROR_NOT_FOUND = {
    "success": False,
    "errors": [{
        "code": 122,
        "error": "Not found",
        "source": "endpoint",
        "section": None
    }]
}

ERROR_UNAUTHORIZED = {
    "success": False,
    "errors": [{
        "code": 401,
        "error": "Unauthorized",
        "source": "auth",
        "section": None
    }]
}

# Tailscale mock responses
TAILSCALE_CONFIG_RESPONSE = {
    "success": True,
    "data": [{
        "id": "tailscale0",
        "enabled": "1",
        "auth_key": "",
        "advert_routes": [],
        "accept_routes": "0",
        "exit_node": "0",
        "auth_type": "url",
        "default_route": "0",
        "exit_node_ip": "",
        "login_server": ""
    }]
}

TAILSCALE_STATUS_RESPONSE = {
    "success": True,
    "data": [{
        "status": "running",
        "url": "https://login.tailscale.com/...",
        "ip": ["100.64.0.1"],
        "message": []
    }]
}

# Session mock responses
SESSION_STATUS_RESPONSE = {
    "success": True,
    "data": {
        "status": "active",
        "username": "admin",
        "expires_in": 3600
    }
}

# Modems mock responses
MODEMS_STATUS_RESPONSE = {
    "success": True,
    "data": [{
        "modem_id": "2-1",
        "connection_state": "connected",
        "signal_strength": -75,
        "operator": "Test Network"
    }]
}


def login_callback(request):
    """Callback for login endpoint that validates credentials.
    
    Returns success if credentials are correct, error otherwise.
    """

    try:
        body = json.loads(request.body)
        username = body.get("username")
        password = body.get("password")

        # Validate credentials
        if username == "admin" and password == "admin":
            return (200, {}, json.dumps(LOGIN_RESPONSE))
        else:
            # Invalid credentials
            error_response = {
                "success": False,
                "errors": [{
                    "code": 401,
                    "error": "Invalid credentials",
                    "source": "auth",
                    "section": None
                }]
            }
            return (200, {}, json.dumps(error_response))
    except Exception:
        # Malformed request
        error_response = {
            "success": False,
            "errors": [{
                "code": 400,
                "error": "Bad request",
                "source": "auth",
                "section": None
            }]
        }
        return (200, {}, json.dumps(error_response))


def mock_login_with_validation():
    """Register login mock with credential validation.
    
    Must be called within a @responses.activate context.
    """
    responses.add_callback(
        responses.POST,
        f"{BASE_URL}/login",
        callback=login_callback,
        content_type="application/json",
    )


def mock_endpoint(
    method: str,
    path: str,
    response_data: Dict[str, Any],
    status: int = 200,
    include_login: bool = True,
    validate_login: bool = False
) -> None:
    """Register a mocked endpoint response.
    
    Args:
        method: HTTP method (get, post, put, delete)
        path: API path (e.g., '/tailscale/config')
        response_data: Response JSON data
        status: HTTP status code
        include_login: Whether to also mock the login endpoint
        validate_login: Whether to validate login credentials (requires correct username/password)
        
    Must be called within a @responses.activate context.
    """
    if include_login:
        if validate_login:
            mock_login_with_validation()
        else:
            responses.post(
                f"{BASE_URL}/login",
                json=LOGIN_RESPONSE,
                status=200,
            )
    
    getattr(responses, method.lower())(
        f"{BASE_URL}{path}",
        json=response_data,
        status=status,
    )


def mock_endpoint_with_callback(
    method: str,
    path: str,
    callback: Callable,
    include_login: bool = True,
    validate_login: bool = False
) -> None:
    """Register a mocked endpoint with a callback function for validation.
    
    Args:
        method: HTTP method (get, post, put, delete)
        path: API path (e.g., '/tailscale/config')
        callback: Callback function that receives request and returns (status, headers, body)
        include_login: Whether to also mock the login endpoint
        validate_login: Whether to validate login credentials
        
    Must be called within a @responses.activate context.
    
    Example callback:
        def my_callback(request):
            body = json.loads(request.body)
            if body.get('param') == 'expected':
                return (200, {}, json.dumps({'success': True, 'data': {}}))
            else:
                return (200, {}, json.dumps({'success': False, 'errors': [...]}))
    """
    if include_login:
        if validate_login:
            mock_login_with_validation()
        else:
            responses.post(
                f"{BASE_URL}/login",
                json=LOGIN_RESPONSE,
                status=200,
            )
    
    responses.add_callback(
        getattr(responses, method.upper()),
        f"{BASE_URL}{path}",
        callback=callback,
        content_type="application/json",
    )


def mock_error_response(
    method: str,
    path: str,
    error_code: int = 122,
    error_message: str = "Not found",
    error_source: str = "endpoint",
    status: int = 200,
    include_login: bool = True
) -> None:
    """Register a mocked error response.
    
    Args:
        method: HTTP method (get, post, put, delete)
        path: API path (e.g., '/tailscale/config')
        error_code: Error code
        error_message: Error message
        error_source: Error source
        status: HTTP status code
        include_login: Whether to also mock the login endpoint
        
    Must be called within a @responses.activate context.
    """
    error_response = {
        "success": False,
        "errors": [{
            "code": error_code,
            "error": error_message,
            "source": error_source,
            "section": None
        }]
    }
    
    mock_endpoint(
        method=method,
        path=path,
        response_data=error_response,
        status=status,
        include_login=include_login
    )