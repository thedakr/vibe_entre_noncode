"""
LLM client wrapper for VEntre agents.
Supports Anthropic Claude API with clean interface.
"""

from typing import List, Dict, Optional, Any
import os


class LLMClient:
    """
    Wrapper for LLM API calls with consistent interface.
    Currently supports Anthropic Claude.
    """

    def __init__(self, api_key: str = None, provider: str = "anthropic", model: str = None):
        """
        Initialize LLM client.

        Args:
            api_key: API key for the provider (or reads from env)
            provider: "anthropic" or "openai"
            model: Specific model to use (defaults to best available)
        """
        self.provider = provider
        self.api_key = api_key or self._get_api_key_from_env()

        if self.provider == "anthropic":
            try:
                from anthropic import Anthropic
                self.client = Anthropic(api_key=self.api_key)
                self.model = model or "claude-sonnet-4-5-20250929"  # Claude Sonnet 4.5 (latest)
            except ImportError:
                raise ImportError("Anthropic support requires: pip install anthropic")

        elif self.provider == "openai":
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
                self.model = model or "gpt-4-turbo-preview"
            except ImportError:
                raise ImportError("OpenAI support requires: pip install openai")

        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def _get_api_key_from_env(self) -> str:
        """Get API key from environment variables."""
        if self.provider == "anthropic":
            key = os.getenv("ANTHROPIC_API_KEY")
            if not key:
                raise ValueError("ANTHROPIC_API_KEY not found in environment")
            return key
        elif self.provider == "openai":
            key = os.getenv("OPENAI_API_KEY")
            if not key:
                raise ValueError("OPENAI_API_KEY not found in environment")
            return key

    def chat(self,
             system_prompt: str,
             messages: List[Dict[str, str]],
             temperature: float = 0.7,
             max_tokens: int = 4096) -> str:
        """
        Send a chat completion request.

        Args:
            system_prompt: System instructions for the agent
            messages: List of message dicts with 'role' and 'content'
            temperature: Randomness (0-1)
            max_tokens: Maximum response length

        Returns:
            Response text from the LLM
        """
        if self.provider == "anthropic":
            return self._chat_anthropic(system_prompt, messages, temperature, max_tokens)
        elif self.provider == "openai":
            return self._chat_openai(system_prompt, messages, temperature, max_tokens)

    def _chat_anthropic(self,
                       system_prompt: str,
                       messages: List[Dict[str, str]],
                       temperature: float,
                       max_tokens: int) -> str:
        """Anthropic-specific chat implementation."""
        response = self.client.messages.create(
            model=self.model,
            system=system_prompt,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.content[0].text

    def _chat_openai(self,
                    system_prompt: str,
                    messages: List[Dict[str, str]],
                    temperature: float,
                    max_tokens: int) -> str:
        """OpenAI-specific chat implementation."""
        # OpenAI includes system as first message
        openai_messages = [{"role": "system", "content": system_prompt}] + messages

        response = self.client.chat.completions.create(
            model=self.model,
            messages=openai_messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content

    def stream_chat(self,
                   system_prompt: str,
                   messages: List[Dict[str, str]],
                   temperature: float = 0.7,
                   max_tokens: int = 4096):
        """
        Stream chat completion (yields chunks as they arrive).

        Args:
            system_prompt: System instructions
            messages: Conversation history
            temperature: Randomness
            max_tokens: Max response length

        Yields:
            Text chunks as they arrive
        """
        if self.provider == "anthropic":
            yield from self._stream_anthropic(system_prompt, messages, temperature, max_tokens)
        elif self.provider == "openai":
            yield from self._stream_openai(system_prompt, messages, temperature, max_tokens)

    def _stream_anthropic(self,
                         system_prompt: str,
                         messages: List[Dict[str, str]],
                         temperature: float,
                         max_tokens: int):
        """Stream from Anthropic."""
        with self.client.messages.stream(
            model=self.model,
            system=system_prompt,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        ) as stream:
            for text in stream.text_stream:
                yield text

    def _stream_openai(self,
                      system_prompt: str,
                      messages: List[Dict[str, str]],
                      temperature: float,
                      max_tokens: int):
        """Stream from OpenAI."""
        openai_messages = [{"role": "system", "content": system_prompt}] + messages

        stream = self.client.chat.completions.create(
            model=self.model,
            messages=openai_messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True
        )

        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    def count_tokens(self, text: str) -> int:
        """
        Estimate token count for text.
        Note: This is an approximation. Actual tokenization varies by model.

        Args:
            text: Text to count tokens for

        Returns:
            Estimated token count
        """
        # Rough approximation: ~4 characters per token
        # For production, use provider-specific tokenizers
        return len(text) // 4

    def format_conversation_history(self,
                                    history: List[Dict],
                                    max_tokens: int = 100000) -> List[Dict[str, str]]:
        """
        Format database conversation history for LLM consumption.
        Truncates if necessary to fit within token limit.

        Args:
            history: List of conversation records from database
            max_tokens: Maximum tokens to include

        Returns:
            Formatted messages list
        """
        messages = []
        total_tokens = 0

        # Reverse to process newest first, then reverse back
        for record in reversed(history):
            role = record['role']  # 'user' or 'assistant'
            content = record['content']
            tokens = self.count_tokens(content)

            if total_tokens + tokens > max_tokens:
                break

            messages.insert(0, {"role": role, "content": content})
            total_tokens += tokens

        return messages
