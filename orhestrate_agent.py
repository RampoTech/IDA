from phi.agent import Agent, RunResponse
from phi.model.groq import Groq
import dotenv
import os
import streamlit as st
from Constants import ORHESTRATE_AGENT_SYSTEMPROMPT

dotenv.load_dotenv()

def orhestrate_agent(input_message):
    # Load the Groq API key from the environment (set this in your .env file as GROQ_API_KEY)
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY not set. Please add it to your environment or .env file.")

    orhestrate_agent = Agent(
        model=Groq(
            id="llama-3.3-70b-versatile",
            api_key=api_key,
            system_prompt=ORHESTRATE_AGENT_SYSTEMPROMPT
            ),
        markdown=True
    )


    # Get the response in a variable
    content = ""
    # optional Streamlit placeholder to update UI as chunks arrive
    placeholder = None
    try:
        placeholder = st.empty()
    except Exception:
        placeholder = None

    def _extract_text(part):
        # handle several possible shapes of streamed parts
        if isinstance(part, RunResponse):
            return getattr(part, "content", "") or getattr(part, "text", "") or ""
        if isinstance(part, dict):
            return part.get("delta") or part.get("content") or part.get("text", "") or ""
        return getattr(part, "delta", "") or getattr(part, "content", "") or getattr(part, "text", "") or (str(part) if part is not None else "")

    stream = orhestrate_agent.run(input_message, stream=True)

    try:
        # try to iterate the stream (typical for streaming APIs)
        for part in stream:
            chunk = _extract_text(part)
            if not chunk:
                continue
            content += chunk
            print(chunk, end="", flush=True)
            if placeholder:
                placeholder.markdown(content)
    except TypeError:
        # not iterable: treat as a single RunResponse
        chunk = _extract_text(stream)
        content += chunk
        print(chunk)
        if placeholder:
            placeholder.markdown(content)

    print()  # newline after stream finishes
    return content

# Print the response in the terminal
# agent.print_response("Share a 2 sentence horror story.")