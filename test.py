import requests
import os

# Load the GitHub PAT from an environment variable
token = os.getenv("GITHUB_TOKEN")
if not token:
    print("Error: GitHub token not found. Set the GITHUB_TOKEN environment variable.")
    exit(1)

def search_repos(keywords):
    # Build the GitHub API search query
    query = "+".join([f"language:{k.lower()}" for k in keywords]) + "+good+first+issue"
    url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page=5"

    # Set up headers with the PAT
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    try:
        # Make the GET request
        response = requests.get(url, headers=headers)
        
        # Check for successful response
        if response.status_code == 200:
            data = response.json()
            repos = data.get("items", [])
            if not repos:
                print("No repositories found for the given keywords.")
                return []

            # Process and display results
            results = []
            for repo in repos:
                repo_info = {
                    "name": repo["name"],
                    "url": repo["html_url"],
                    "description": repo["description"] or "No description",
                    "tips": [
                        "Look for issues labeled 'good first issue'",
                        "Fix typos in documentation",
                        "Add simple unit tests"
                    ]
                }
                results.append(repo_info)
                print(f"Repository: {repo_info['name']}")
                print(f"URL: {repo_info['url']}")
                print(f"Description: {repo_info['description']}")
                print("Contribution Tips:")
                for tip in repo_info['tips']:
                    print(f"  - {tip}")
                print()
            return results
        else:
            print(f"Failed to fetch repositories. Status code: {response.status_code}")
            print(response.text)
            return []
    except Exception as e:
        print(f"Error: {str(e)}")
        return []

# Example usage
if __name__ == "__main__":
    keywords = ["Python"]  # Replace with desired keywords, e.g., ["Python", "AI"]
    search_repos(keywords)