import datetime
import io
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse, StreamingResponse

from service.people import PeopleService

app = FastAPI()

# Enable CORS (keep for compatibility)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins for simplicity
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory
static_dir = Path(__file__).parent.parent / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

service = PeopleService()

@app.get("/")
async def read_root():
    """Serve the main HTML page."""
    html_path = static_dir / "index.html"
    return FileResponse(html_path)

@app.get("/stat_for_month")
def get_file_from_string(dt: datetime.date):
    # The content you want to serve as a file
    file_content_bytes = service.get_people_for_month(dt=dt).encode("utf-8")
    # Create an in-memory byte buffer
    bytes_io = io.BytesIO(file_content_bytes)

    headers = {
        'Content-Disposition': f'attachment; filename="{dt}.csv"'
    }

    return StreamingResponse(
        bytes_io,
        media_type="text/plain",
        headers=headers
    )