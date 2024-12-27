from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from typing import Dict
from datetime import datetime
from src.transformations.earthquake import top_n_nearest_earthquakes

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def read_root():
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html_content = f"""
    <html>
        <head>
            <title>Home</title>
        </head>
        <body>
            <h1>Welcome to the Earthquake API!</h1>
            <p>Creator: Dilson Castro</p>
            <p>Current Date and Time: {current_datetime}</p>
            <p>To find earthquakes near you, please navigate to <a href="http://localhost:5005/docs/">This Link</a>.
            </p>
        </body>
    </html>
    """
    return html_content


@app.get("/earthquakes/near-me")
async def nearest_earthquakes(lat: float, lon: float) -> Dict:
    """Get top n earthquakes near to an entered location
    Args:
        lat (float): input latitud.
        lon (float): input longitude.
    Returns:
        Dict: nearest earthquakes in json format.
    """
    earthquakes = top_n_nearest_earthquakes(input_lat=lat, input_lon=lon)
    return {"earthquakes": earthquakes}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=5005)
