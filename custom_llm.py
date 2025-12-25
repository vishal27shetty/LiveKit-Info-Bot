from __future__ import annotations

import os
from dataclasses import asdict, dataclass
from typing import Any, Literal
from urllib.parse import urlparse

import httpx

import openai
from livekit.agents import llm
from livekit.agents.inference.llm import LLMStream as _LLMStream        
from livekit.agents.llm import ToolChoice, utils as llm_utils
from livekit.agents.llm.chat_context import ChatContext
from livekit.agents.llm.tool_context import FunctionTool, RawFunctionTool
from livekit.agents.types import (
    DEFAULT_API_CONNECT_OPTIONS,
    NOT_GIVEN,
    APIConnectOptions,
    NotGivenOr,
)
from livekit.agents.utils import is_given
from openai.types import ReasoningEffort
from openai.types.chat import ChatCompletionToolChoiceOptionParam, completion_create_params

lk_oai_debug = int(os.getenv("LK_OPENAI_DEBUG", 0))

Verbosity = Literal["low", "medium", "high"]
PromptCacheRetention = Literal["in_memory", "24h"]


@dataclass
class _LLMOptions:
    model: str 
    user: NotGivenOr[str]
    safety_identifier: NotGivenOr[str]
    prompt_cache_key: NotGivenOr[str]
    temperature: NotGivenOr[float]
    top_p: NotGivenOr[float]
    parallel_tool_calls: NotGivenOr[bool]
    tool_choice: NotGivenOr[ToolChoice]
    store: NotGivenOr[bool]
    metadata: NotGivenOr[dict[str, str]]
    max_completion_tokens: NotGivenOr[int]
    service_tier: NotGivenOr[str]
    reasoning_effort: NotGivenOr[ReasoningEffort]
    verbosity: NotGivenOr[Verbosity]
    prompt_cache_retention: NotGivenOr[PromptCacheRetention]
    extra_body: NotGivenOr[dict[str, Any]]
    extra_headers: NotGivenOr[dict[str, str]]
    extra_query: NotGivenOr[dict[str, str]]



class CustomLLM(llm.LLM):
    def __init__(
        self,
        *,
        model: str = "gpt-4o-mini",
        api_key: NotGivenOr[str] = os.getenv("OPEN_API_KEY"),
        base_url: NotGivenOr[str] = NOT_GIVEN,
        client: openai.AsyncClient | None = None,
        user: NotGivenOr[str] = NOT_GIVEN,
        safety_identifier: NotGivenOr[str] = NOT_GIVEN,
        prompt_cache_key: NotGivenOr[str] = NOT_GIVEN,
        temperature: NotGivenOr[float] = NOT_GIVEN,
        top_p: NotGivenOr[float] = NOT_GIVEN,
        parallel_tool_calls: NotGivenOr[bool] = NOT_GIVEN,
        tool_choice: NotGivenOr[ToolChoice] = NOT_GIVEN,
        store: NotGivenOr[bool] = NOT_GIVEN,
        metadata: NotGivenOr[dict[str, str]] = NOT_GIVEN,
        max_completion_tokens: NotGivenOr[int] = NOT_GIVEN,
        timeout: httpx.Timeout | None = None,
        max_retries: NotGivenOr[int] = NOT_GIVEN,
        service_tier: NotGivenOr[str] = NOT_GIVEN,
        reasoning_effort: NotGivenOr[ReasoningEffort] = NOT_GIVEN,
        verbosity: NotGivenOr[Verbosity] = NOT_GIVEN,
        prompt_cache_retention: NotGivenOr[PromptCacheRetention] = NOT_GIVEN,
        extra_body: NotGivenOr[dict[str, Any]] = NOT_GIVEN,
        extra_headers: NotGivenOr[dict[str, str]] = NOT_GIVEN,
        extra_query: NotGivenOr[dict[str, str]] = NOT_GIVEN,
        _provider_fmt: NotGivenOr[str] = NOT_GIVEN,
        _strict_tool_schema: bool = True,
    ) -> None:
        """
        Create a new instance of OpenAI LLM.

        ``api_key`` must be set to your OpenAI API key, either using the argument or by setting the
        ``OPENAI_API_KEY`` environmental variable.
        """
        super().__init__()

        self._opts = _LLMOptions(
            model=model,
            user=user,
            temperature=temperature,
            parallel_tool_calls=parallel_tool_calls,
            tool_choice=tool_choice,
            store=store,
            metadata=metadata,
            max_completion_tokens=max_completion_tokens,
            service_tier=service_tier,
            reasoning_effort=reasoning_effort,
            safety_identifier=safety_identifier,
            prompt_cache_key=prompt_cache_key,
            top_p=top_p,
            verbosity=verbosity,
            prompt_cache_retention=prompt_cache_retention,
            extra_body=extra_body,
            extra_headers=extra_headers,
            extra_query=extra_query,
        )
        self._provider_fmt = _provider_fmt or "openai"
        self._strict_tool_schema = _strict_tool_schema
        self._client = client or openai.AsyncClient(
            api_key=api_key if is_given(api_key) else None,
            base_url=base_url if is_given(base_url) else None,
            max_retries=max_retries if is_given(max_retries) else 0,
            http_client=httpx.AsyncClient(
                timeout=timeout
                if timeout
                else httpx.Timeout(connect=15.0, read=5.0, write=5.0, pool=5.0),
                follow_redirects=True,
                limits=httpx.Limits(
                    max_connections=50,
                    max_keepalive_connections=50,
                    keepalive_expiry=120,
                ),
            ),
        )

    @property
    def model(self) -> str:
        return self._opts.model

    @property
    def provider(self) -> str:
        return self._client._base_url.netloc.decode("utf-8")
    
    

    def chat(
        self,
        *,
        chat_ctx: ChatContext,
        tools: list[FunctionTool | RawFunctionTool] | None = None,
        conn_options: APIConnectOptions = DEFAULT_API_CONNECT_OPTIONS,
        parallel_tool_calls: NotGivenOr[bool] = NOT_GIVEN,
        tool_choice: NotGivenOr[ToolChoice] = NOT_GIVEN,
        response_format: NotGivenOr[
            completion_create_params.ResponseFormat | type[llm_utils.ResponseFormatT]
        ] = NOT_GIVEN,
        extra_kwargs: NotGivenOr[dict[str, Any]] = NOT_GIVEN,
    ) -> LLMStream:
        extra = {}
        if is_given(extra_kwargs):
            extra.update(extra_kwargs)

        if is_given(self._opts.extra_body):
            extra["extra_body"] = self._opts.extra_body

        if is_given(self._opts.extra_headers):
            extra["extra_headers"] = self._opts.extra_headers

        if is_given(self._opts.extra_query):
            extra["extra_query"] = self._opts.extra_query

        if is_given(self._opts.metadata):
            extra["metadata"] = self._opts.metadata

        if is_given(self._opts.user):
            extra["user"] = self._opts.user

        if is_given(self._opts.max_completion_tokens):
            extra["max_completion_tokens"] = self._opts.max_completion_tokens

        if is_given(self._opts.temperature):
            extra["temperature"] = self._opts.temperature

        if is_given(self._opts.service_tier):
            extra["service_tier"] = self._opts.service_tier

        if is_given(self._opts.reasoning_effort):
            extra["reasoning_effort"] = self._opts.reasoning_effort

        if is_given(self._opts.safety_identifier):
            extra["safety_identifier"] = self._opts.safety_identifier

        if is_given(self._opts.prompt_cache_key):
            extra["prompt_cache_key"] = self._opts.prompt_cache_key

        if is_given(self._opts.top_p):
            extra["top_p"] = self._opts.top_p

        if is_given(self._opts.verbosity):
            extra["verbosity"] = self._opts.verbosity

        if is_given(self._opts.prompt_cache_retention):
            extra["prompt_cache_retention"] = self._opts.prompt_cache_retention

        parallel_tool_calls = (
            parallel_tool_calls if is_given(parallel_tool_calls) else self._opts.parallel_tool_calls
        )
        if is_given(parallel_tool_calls):
            extra["parallel_tool_calls"] = parallel_tool_calls

        tool_choice = tool_choice if is_given(tool_choice) else self._opts.tool_choice  # type: ignore
        if is_given(tool_choice):
            oai_tool_choice: ChatCompletionToolChoiceOptionParam
            if isinstance(tool_choice, dict):
                oai_tool_choice = {
                    "type": "function",
                    "function": {"name": tool_choice["function"]["name"]},
                }
                extra["tool_choice"] = oai_tool_choice
            elif tool_choice in ("auto", "required", "none"):
                oai_tool_choice = tool_choice
                extra["tool_choice"] = oai_tool_choice

        if is_given(response_format):
            extra["response_format"] = llm_utils.to_openai_response_format(response_format)  # type: ignore

        return LLMStream(
            self,
            model=self._opts.model,
            provider_fmt=self._provider_fmt,
            strict_tool_schema=self._strict_tool_schema,
            client=self._client,
            chat_ctx=chat_ctx,
            tools=tools or [],
            conn_options=conn_options,
            extra_kwargs=extra,
        )
    
    
    


class LLMStream(_LLMStream):
    def __init__(
        self,
        llm: CustomLLM,
        *,
        model: str = "gpt-4o-mini",
        provider_fmt: str,
        strict_tool_schema: bool,
        client: openai.AsyncClient,
        chat_ctx: llm.ChatContext,
        tools: list[FunctionTool | RawFunctionTool],
        conn_options: APIConnectOptions,
        extra_kwargs: dict[str, Any],
    ) -> None:
        super().__init__(
            llm,
            model=model,
            provider_fmt=provider_fmt,
            strict_tool_schema=strict_tool_schema,
            client=client,
            chat_ctx=chat_ctx,
            tools=tools,
            conn_options=conn_options,
            extra_kwargs=extra_kwargs,
        )