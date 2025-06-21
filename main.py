
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BUILTWITH_API_KEY = "db612c1d-d217-4c3c-8fc5-be9de57ed6dd"

@app.get("/scan/")
async def scan_website(url: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10)
            builtwith_response = await client.get(
                f"https://api.builtwith.com/v20/api.json?KEY={BUILTWITH_API_KEY}&LOOKUP={url}"
            )

        headers = dict(response.headers)
        status = response.status_code
        tech_info = builtwith_response.json()

        return {
            "status": status,
            "headers": headers,
            "tech_stack": tech_info,
            "url": url
        }
    except Exception as e:
        return {"error": str(e)}
