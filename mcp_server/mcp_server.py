import wikipedia
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("WikipediaSearch")


@mcp.tool()
def fetch_wikipedia_info(query: str) -> dict:
    """
    Serach wikipedia based on the query and return the title, summary and url
    """
    try:
        results = wikipedia.search(query)
        if not results:
            return {"error": "No results found"}

        best_match = results[0]
        page = wikipedia.page(best_match)

        return {"title": page.title, "summary": page.summary, "url": page.url}
    except wikipedia.DisambiguationError as e:
        return {
            "error": f"Ambiguous query, try one of these {', '.join(e.options[:5])}"
        }
    except wikipedia.PageError:
        return {"error": "No wikipedia page found for the given query"}


@mcp.tool()
def list_wikipedia_sections(topic: str) -> dict:
    """
    Return a list of section titles from the wikipedia page of a given topic
    """
    try:
        page = wikipedia.page(topic)
        sections = page.sections
        return {"sections": sections}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_section_content(topic: str, section_title: str) -> dict:
    """
    Return the content of a specific section in a wikipedia article
    """

    try:
        page = wikipedia.page(topic)
        content = page.section(section_title)
        if not content:
            return {
                "error": f"Section '{section_title}' not found in the article '{topic}'"
            }
        return {"content": content}
    except Exception as e:
        return {"error": str(e)}
