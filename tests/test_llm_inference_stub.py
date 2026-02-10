from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path


def _load_llm_inference_with_stubs():
    root = Path(__file__).resolve().parents[1]
    path = root / "evaluation" / "llm_inference.py"

    # Stub torch
    torch_stub = types.SimpleNamespace()
    torch_stub.bfloat16 = object()
    torch_stub.float16 = object()
    torch_stub.LongTensor = list
    torch_stub.FloatTensor = list

    # Stub tiktoken
    class DummyEncoding:
        def encode(self, text, add_special_tokens=True):
            return [0] * len(text)

    tiktoken_stub = types.SimpleNamespace(get_encoding=lambda name: DummyEncoding())

    # Stub transformers
    class DummyTokenizer:
        eos_token_id = 0

        def __init__(self):
            self.chat_template = ""

        def apply_chat_template(self, messages, tokenize=False, add_generation_prompt=True):
            return "prompt"

        def encode(self, text, add_special_tokens=True):
            return [0] * len(text)

        def decode(self, tokens):
            return "STOP"

        def convert_tokens_to_ids(self, token):
            return 1

    class DummyAutoTokenizer:
        @classmethod
        def from_pretrained(cls, *args, **kwargs):
            return DummyTokenizer()

    class DummyStoppingCriteria:
        pass

    class DummyStoppingCriteriaList(list):
        pass

    def dummy_pipeline(*args, **kwargs):
        def _call(prompt, **call_kwargs):
            return [{"generated_text": "pipeline output"}]
        return _call

    transformers_stub = types.SimpleNamespace(
        AutoTokenizer=DummyAutoTokenizer,
        StoppingCriteria=DummyStoppingCriteria,
        StoppingCriteriaList=DummyStoppingCriteriaList,
        pipeline=dummy_pipeline,
    )

    # Stub openai
    class DummyResponse:
        def __init__(self, content):
            self.choices = [types.SimpleNamespace(message=types.SimpleNamespace(content=content))]

    class DummyChatCompletion:
        @staticmethod
        def create(model, messages):
            return DummyResponse("hello   world")

    openai_stub = types.SimpleNamespace(api_key=None, ChatCompletion=DummyChatCompletion)

    # Stub huggingface_hub
    huggingface_stub = types.SimpleNamespace(login=lambda token=None: None)

    # Stub google genai to avoid importing heavy deps/warnings.
    google_module = types.ModuleType("google")
    genai_module = types.ModuleType("google.genai")
    genai_types_module = types.ModuleType("google.genai.types")
    setattr(google_module, "genai", genai_module)

    sys.modules.setdefault("torch", torch_stub)
    sys.modules.setdefault("tiktoken", tiktoken_stub)
    sys.modules.setdefault("transformers", transformers_stub)
    sys.modules["openai"] = openai_stub
    sys.modules.setdefault("huggingface_hub", huggingface_stub)
    sys.modules.setdefault("tqdm", types.SimpleNamespace())
    sys.modules.setdefault("google", google_module)
    sys.modules.setdefault("google.genai", genai_module)
    sys.modules.setdefault("google.genai.types", genai_types_module)

    spec = importlib.util.spec_from_file_location("llm_inference", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[arg-type]
    return module


def test_llm_inference_openai_branch():
    module = _load_llm_inference_with_stubs()
    llm = module.LLMInference(llm_name="OpenAI/gpt-3.5-turbo")
    answer = llm.answer([{"role": "user", "content": "hi"}])
    assert answer == "hello world"


def test_custom_stopping_criteria():
    module = _load_llm_inference_with_stubs()
    tokenizer = module.AutoTokenizer.from_pretrained("dummy")
    criteria = module.CustomStoppingCriteria(["STOP"], tokenizer, input_len=0)
    assert criteria([[0]], None) is True
