from mcp.server.fastmcp import FastMCP #type: ignore
import requests

mcp = FastMCP()

@mcp.tool()
async def search_repositories(keywords: list[str]) -> list[dict]:
    # Build the GitHub API search query
    query = " ".join([f"language:{k}" for k in keywords]) + " label:good+first+issue"
    url = f"https://api.github.com/search/repositories?q={query}&per_page=5"
    
    # Fetch data from GitHub API
    response = requests.get(url)
    if response.status_code != 200:
        return [{"error": "Failed to fetch repositories"}]
    
    data = response.json()
    repositories = data.get("items", [])
    result = []
    
    # Extract relevant repository information
    for repo in repositories:
        result.append({
            "name": repo["name"],
            "url": repo["html_url"],
            "description": repo["description"] or "No description",
            "tips": ["Look for issues labeled 'good first issue'", "Fix documentation", "Add tests"]
        })
    
    return result

if __name__ == "__main__":
    mcp.run()


