"""
ResearchAgent — Gathers real-time market intelligence via web search.

Uses the built-in web_search server-side tool, which means the LLM
autonomously decides when and what to search without manual tool-loop handling.
"""

import anthropic


SYSTEM_PROMPT = """You are a senior market research analyst at a top-tier consulting firm.
Your task is to produce a thorough, factual research brief on a given company.

Use web search extensively to gather up-to-date information covering:
1. Company profile — founding year, HQ, business model, key products/services
2. Market position — estimated market share, competitive advantages, customer segments
3. Top 3–5 competitors — who they are and how they compare
4. Recent news & developments — significant events from the last 12 months
5. Financial highlights — revenue, growth rate, profitability (if publicly available)
6. Industry trends — major forces shaping the sector (technological, regulatory, consumer)

Return a structured, well-written research brief with clear section headers.
Cite sources implicitly by referencing company names and dates where relevant.
Be factual and concise — avoid speculation unless clearly labeled as such."""


class ResearchAgent:
    """
    Agent that uses the web_search tool to gather company and market data.

    The web_search tool is server-side: the model autonomously issues search queries,
    processes results, and synthesizes findings. We only need to handle the
    `pause_turn` stop reason in case the server-side loop hits its iteration limit.
    """

    def __init__(self, client: anthropic.Anthropic, model: str = "claude-opus-4-6"):
        self.client = client
        self.model = model
        self.tools = [
            {"type": "web_search_20260209", "name": "web_search"},
        ]

    def research(self, company: str) -> str:
        """
        Research a company and return a comprehensive text brief.

        Args:
            company: Company name (e.g. "Siemens AG", "Zalando", "SAP")

        Returns:
            A multi-section research brief as plain text.
        """
        user_message = (
            f"Research '{company}' thoroughly. "
            f"Use multiple web searches to gather current information on all six areas "
            f"listed in your instructions. Compile everything into a structured research brief."
        )

        messages = [{"role": "user", "content": user_message}]

        # Server-side tool loop — handle `pause_turn` if the model needs more iterations
        max_continuations = 5
        for _ in range(max_continuations):
            response = self.client.messages.create(
                model=self.model,
                max_tokens=8192,
                system=SYSTEM_PROMPT,
                tools=self.tools,
                messages=messages,
                thinking={"type": "adaptive"},
            )

            if response.stop_reason == "end_turn":
                break

            if response.stop_reason == "pause_turn":
                # Server-side loop hit its limit — send back assistant response to continue
                messages = [
                    {"role": "user", "content": user_message},
                    {"role": "assistant", "content": response.content},
                ]
                continue

            break  # Any other stop reason — treat as done

        # Extract all text blocks from the final response
        return "\n\n".join(
            block.text
            for block in response.content
            if hasattr(block, "text") and block.text
        )
