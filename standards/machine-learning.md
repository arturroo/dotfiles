# Machine Learning & AI Engineering Standards

These standards govern model selection, Vertex AI integrations, prompt engineering, and token economics.

---

## 1. Vertex AI IAM Integration

In all services and local executions leveraging Google Cloud IAM credentials (`roles/aiplatform.user`), LLM clients **MUST explicitly configure Vertex AI mode** (`vertexai=True`). Omitting this parameter causes SDKs to fall back to the consumer Developer API and fail when looking for consumer API keys.

### LangChain (`langchain-google-genai`):
```python
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    temperature=0.1,
    project=config.GOOGLE_CLOUD_PROJECT,
    location=config.GOOGLE_CLOUD_LOCATION,
    vertexai=True,
    thinking_level="low",
)
```

### Google GenAI SDK (`google-genai`):
```python
from google import genai

client = genai.Client(
    vertexai=True,
    project=config.GOOGLE_CLOUD_PROJECT,
    location=config.GOOGLE_CLOUD_LOCATION,
)
```

---

## 2. Cognitive Model Hierarchy ("The Right Model for the Job")

Select models based on task complexity, latency sensitivity, and token economics:

| Tier | Workhorse Model | Primary Use Cases | Thinking Level |
| :--- | :--- | :--- | :--- |
| **Fast / Utility** | `gemini-3.5-flash-lite` | Text classification, summarization, JSON schema extraction, intent routing | None / Disabled |
| **General Workhorse** | `gemini-3.8-flash` | Agentic tool calling, code generation, multi-step problem solving | `low` (default) |
| **Deep Reasoning** | `gemini-2.5-pro` / `gemini-3.8-pro` | Complex architectural design, multi-file refactoring, difficult math/logic | `medium` or `high` |

---

## 3. Dynamic Runtime Overrides for Operational Agility

Every agent or ML microservice must allow runtime overrides in API requests and CLI arguments:
* `model: str | None = None` (e.g. bypass quota saturation without container redeploys)
* `max_iterations: int | None = None` (tune agent loop depth dynamically)
* `thinking_level: Literal["low", "medium", "high"] | None = None` (tune latency vs reasoning depth)

---

## 4. Token Economics & Prompt Engineering

- **Context Caching:** For large, static datasets or immutable document corpora (>32k tokens), always leverage Vertex AI Context Caching to cut input latency and reduce token costs by up to 75%.
- **Zero-Pollution Tooling:**
  - Never allow tools to pass multi-megabyte payloads (Base64, raw binary) back into LLM conversation contexts.
  - Return concise metadata summaries instead (e.g., `<SAVED_BLOB: path=gs://bucket/file.png, size=2.1MB>`).
- **Structured Outputs:**
  - Enforce output constraints using Pydantic models with `response_schema` or `with_structured_output` rather than asking the LLM to format JSON in natural language.
