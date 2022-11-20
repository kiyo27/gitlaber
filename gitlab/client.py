import requests

import gitlab.const
from gitlab.config import GitLabConfigParser
from typing import Any, Dict, Optional

import time


class GitLab:
    def __init__(
        self,
        url: Optional[str] = None,
        private_token: Optional[str] = None,
        user_agent: str = gitlab.const.USER_AGENT,
    ) -> None:
        self._base_url = self._get_base_url(url)
        self._url = f"{self._base_url}/api/v4"
        self.private_token = private_token
        self.session = requests.Session()
        self.headers = {"User-Agent": user_agent}

        self._set_auth_info()

    @classmethod
    def merge_config(cls, config: GitLabConfigParser) -> "GitLab":
        url = config.url or gitlab.const.DEFAULT_URL

        return cls(url=url, private_token=config.private_token)

    def _prepare_send_data(self, post_data, raw: bool = False):
        if raw and post_data:
            return (None, post_data, "application/octet-stream")
        return (post_data, None, "application/json")

    def _set_auth_info(self) -> None:
        if self.private_token:
            self.headers["PRIVATE-TOKEN"] = self.private_token

    def get_session_opts(self) -> Dict[str, Any]:
        return {
            "headers": self.headers.copy(),
        }

    def _get_base_url(self, url: Optional[str] = None) -> str:
        if not url:
            return gitlab.const.DEFAULT_URL
        return url.rstrip("/")

    def _build_url(self, path: str) -> str:
        return f"{self._url}{path}"

    def http_request(
        self,
        verb: str,
        path: str,
        query_data: Optional[Dict[str, Any]] = None,
        post_data: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        max_retries: int = 10,
        **kwargs,
    ) -> requests.Response:

        query_data = query_data or {}
        url = self._build_url(path)

        params = {}
        opts = self.get_session_opts()

        if "query_parameters" in kwargs:
            for k, v in kwargs.items():
                params[k] = v
        json, data, content_type = self._prepare_send_data(post_data, raw)

        opts["headers"]["Content-type"] = content_type

        cur_retries = 0
        while True:
            try:
                result = self.session.request(
                    method=verb,
                    url=url,
                    json=json,
                    data=data,
                    params=params,
                    **opts,
                )

            except requests.ConnectionError:
                if max_retries == -1 or cur_retries < max_retries:
                    cur_retries += 1
                    wait_time = 2**cur_retries * 0.1
                    time.sleep(wait_time)
                    continue

                raise

            if 200 <= result.status_code < 300:
                return result

    def http_get(
        self,
        path: str,
        query_data: Optional[Dict[str, Any]] = None,
        streamed: bool = False,
        raw: bool = False,
        **kwargs: Any,
    ):
        query_data = query_data or {}
        result = self.http_request("get", path, query_data=query_data, **kwargs)
        if (
            result.headers["Content-Type"] == "application/json"
            and not streamed
            and not raw
        ):
            json_result = result.json()
            return json_result

        else:
            return result

    def http_put(
        self,
        path: str,
        query_data: Optional[Dict[str, Any]] = None,
        post_data: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        **kwargs: Any,
    ) -> requests.Response:
        query_data = query_data or {}
        post_data = post_data or {}

        result = self.http_request(
            "put", path, query_data=query_data, post_data=post_data, raw=raw, **kwargs
        )

        return result
