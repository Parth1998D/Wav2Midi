from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from audio_to_midi_master import audio2midi
from fastapi.staticfiles import StaticFiles
from urllib import request
#import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)


@app.get("/", response_class=HTMLResponse)
def home(req: Request):
    return templates.TemplateResponse("index.html", {"request": req})


@app.post("/")
async def process(wavfile: UploadFile = File(...)):
    wav_file_name = wavfile.filename
    midi_file_name = wav_file_name.split('.')[0] + '.mid'
    try:
        contents = await wavfile.read()
        with open("media/" + wav_file_name, 'wb') as f:
            f.write(contents)
        await audio2midi.run("media/" + wav_file_name, "media/" + midi_file_name)
    # except Exception:
    #     print("exception")
    finally:
        await wavfile.close()
        return FileResponse("media/" + midi_file_name, filename=midi_file_name)


@app.post("/link")
async def process(wavlink: str = Form(...)):
    wav_file_name = wavlink.split('/')[-1]
    midi_file_name = wav_file_name.split('.')[0] + '.mid'
    try:
        request.urlretrieve(wavlink, "media/"+wav_file_name)
        await audio2midi.run("media/" + wav_file_name, "media/" + midi_file_name)
    # except Exception:
    #     print("exception")
    finally:
        return FileResponse("media/" + midi_file_name, filename=midi_file_name)


# if __name__ == "__main__":
#     uvicorn.run(app)

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info")