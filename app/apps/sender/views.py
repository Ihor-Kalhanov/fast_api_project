from fastapi import APIRouter
from celery.result import AsyncResult
from fastapi import Body
from fastapi.responses import JSONResponse
from app.worker import create_task, send_email
from app.apps.sender.schemas import EmailSchema

sender_router = APIRouter()


@sender_router.post("/tasks", status_code=201)
def run_task(payload=Body(...)):
    task_type = payload["task"]
    task = create_task.delay(int(task_type))
    return JSONResponse({"task_id": task.id})


@sender_router.get("/tasks/{task_id}")
def get_status(task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JSONResponse(result)


@sender_router.post('/tasks/')
async def add_email(email: EmailSchema):

    task = send_email.delay(email.email)
    result = AsyncResult(task.id)
    print(f'*********{result.__dict__}****************')
    if result.status == 'SUCCESS':
        print(f'*********{result}****************')
        return {"message": "Emails Sent! Thank you for your patience."}
    return {"message": "Problems."}

