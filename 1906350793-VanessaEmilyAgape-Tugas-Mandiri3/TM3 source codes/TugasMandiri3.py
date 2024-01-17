from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import logging
from logstash_async.handler import AsynchronousLogstashHandler
from logstash_async.handler import LogstashFormatter

app = FastAPI()

# Create the logger and set it's logging level
logger = logging.getLogger("logstash")
logger.setLevel(logging.DEBUG)        

# Create the handler
handler = AsynchronousLogstashHandler(
    host='c3d0653b-ec64-4c43-bd6f-72e698c2da34-ls.logit.io', 
    port=11678, 
    ssl_enable=False, 
    ssl_verify=False,
    database_path='')
# Here you can specify additional formatting on your log record/message
formatter = LogstashFormatter()
handler.setFormatter(formatter)

# Assign handler to the logger
logger.addHandler(handler)

# Send log records to Logstash 
# logger.error('python-logstash-async: test error message.')
# logger.info('python-logstash-async: test info message.')
# logger.warning('python-logstash-async: test warning message.')
# logger.debug('python-logstash-async: test debug message.')

templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root():
    logger.info('tes')
    return {"Hello": "World"}

@app.get("/{param}", response_class=HTMLResponse)
async def get(request: Request, param: str):
    logger.debug(param)
    print("hello")
    return templates.TemplateResponse("index.html", {"request": request, "param": param})