import asyncio
import logging

from fastapi import FastAPI, File, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.excel import create_excel
from app.mail import send_results
from app.vision import analyze_photo

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fodometer")

app = FastAPI(title="FodoMeter")
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/analyze")
async def analyze(files: list[UploadFile] = File(...)):
    if not files:
        return JSONResponse({"error": "Geen foto's ontvangen"}, status_code=400)

    results = []
    errors = []

    for f in files:
        try:
            image_bytes = await f.read()
            ingredienten = await analyze_photo(image_bytes, f.content_type)
            results.append({"filename": f.filename, "ingredienten": ingredienten})
            logger.info("Analyzed %s: %d ingrediënten", f.filename, len(ingredienten))
        except Exception as e:
            logger.error("Error analyzing %s: %s", f.filename, e)
            errors.append({"filename": f.filename, "error": str(e)})

    if not results:
        return JSONResponse({"error": "Geen foto's konden worden geanalyseerd", "details": errors}, status_code=500)

    excel_bytes = create_excel(results)

    try:
        await send_results(excel_bytes, len(results))
        mail_sent = True
    except Exception as e:
        logger.error("Email verzenden mislukt: %s", e)
        mail_sent = False

    total_ingredients = sum(len(r["ingredienten"]) for r in results)

    return JSONResponse({
        "success": True,
        "photos_analyzed": len(results),
        "total_ingredients": total_ingredients,
        "mail_sent": mail_sent,
        "results": results,
        "errors": errors if errors else None,
    })
