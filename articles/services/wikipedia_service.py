import requests

class WikipediaService:
    @staticmethod
    def search_articles(query, limit=10):
        """Search for Wikipedia articles using MediaWiki API directly"""
        try:
            # Use MediaWiki API with generator=search for efficiency
            api_url = "https://en.wikipedia.org/w/api.php"
            params = {
                "action": "query",
                "format": "json",
                "generator": "search",
                "gsrsearch": query,
                "gsrlimit": limit,
                "prop": "extracts|pageimages|info",
                "exintro": 1,
                "explaintext": 1,
                "piprop": "thumbnail",
                "pithumbsize": 500,
                "pilimit": limit,
                "inprop": "url"
            }
            
            response = requests.get(api_url, params=params)
            data = response.json()
            
            articles = []
            pages = data.get("query", {}).get("pages", {})
            
            if not pages:
                print(f"No results found for query: {query}")
                return []
            
            # Sort pages to ensure consistent ordering
            for page_id, page_info in sorted(pages.items(), key=lambda item: int(item[0])):
                title = page_info.get("title", "")
                summary = page_info.get("extract", "")
                url = page_info.get("fullurl", f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}")
                
                # Get image if available
                image_url = None
                if "thumbnail" in page_info:
                    image_url = page_info["thumbnail"]["source"]
                
                article = {
                    "article_id": str(page_id),
                    "title": title,
                    "summary": summary[:500] + "..." if len(summary) > 500 else summary,
                    "url": url,
                    "image_url": image_url,
                    "categories": ""  # Simplified - no categories for better performance
                }
                
                articles.append(article)
            
            print(f"Found {len(articles)} articles for query: {query}")
            return articles
        except Exception as e:
            print(f"Error in MediaWiki search: {e}")
            return []