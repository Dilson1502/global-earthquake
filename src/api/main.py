import os
import sys
from dotenv import load_dotenv

# Load environment variable from .env file if present.
load_dotenv()

# Get API URL
TOP_LEVEL_DIRECTORY = os.getenv("DIRECTORY_PATH")

if TOP_LEVEL_DIRECTORY:
    sys.path.append(TOP_LEVEL_DIRECTORY)


from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
from datetime import datetime
from src.transformations.earthquake import top_n_nearest_earthquakes

app = FastAPI()

# Allow cross-origin requests (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins, you can restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_root():
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html_content = f"""
    <html>
        <head>
            <title>Earthquake API</title>
            <style>
                body {{
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    font-family: Arial, sans-serif;
                    background-color: #f0f8ff;
                    color: #333;
                    text-align: center;
                }}
                h1 {{
                    font-size: 2.5em;
                    margin-bottom: 0.5em;
                }}
                p {{
                    font-size: 1.2em;
                    margin: 0.5em 0;
                }}
                a {{
                    color: #007bff;
                    text-decoration: none;
                }}
                a:hover {{
                    text-decoration: underline;
                }}
            </style>
        </head>
        <body>
            <div>
                <h1>Welcome to the Earthquake API!</h1>
                <p>Creator: Dilson Castro</p>
                <p>Current Date and Time: {current_datetime}</p>
                <p>To find earthquakes near you, please navigate to <a href="/static/index.html">this link</a>.</p>
            </div>
        </body>
    </html>
    """
    return html_content


@app.get("/earthquakes/near-me")
async def nearest_earthquakes(lat: float, lon: float, num_earthquakes: int = 10) -> Dict:
    """Get top n earthquakes near to an entered location.

    Args:
        lat (float): input latitude.
        lon (float): input longitude.
        num_earthquakes (int): Number of earthquakes to return.

    Returns:
        Dict: nearest earthquakes in json format.
    """
    earthquakes = top_n_nearest_earthquakes(input_lat=lat, input_lon=lon, number_of_earthquakes=num_earthquakes)
    return {"earthquakes": earthquakes}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=5005)