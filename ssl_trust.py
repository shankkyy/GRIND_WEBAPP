"""Make HTTPS clients trust the operating system certificate store.

httpx verifies against the certifi bundle. On this machine that bundle does
not contain the issuer for Supabase, so auth and database calls fail with
CERTIFICATE_VERIFY_FAILED. This patch must run before httpx creates a client.
"""
import ssl
import sys

import truststore

import httpx._config as httpx_config


def _create_ssl_context(verify=True, cert=None, trust_env=True):
    if verify is True:
        return truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    return _original_create_ssl_context(verify=verify, cert=cert, trust_env=trust_env)


_original_create_ssl_context = httpx_config.create_ssl_context
httpx_config.create_ssl_context = _create_ssl_context

_transport = sys.modules.get("httpx._transports.default")
if _transport is not None:
    _transport.create_ssl_context = _create_ssl_context
