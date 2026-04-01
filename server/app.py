from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any

from environment.env import CustomerSupportEnv
from environment.models import Action
from environment.grader import EnvironmentGrader
import uvicorn

app = FastAPI()

env = CustomerSupportEnv()
grader = EnvironmentGrader()


class StepRequest(BaseModel):
    action_type: str
    content: str = None


@app.post("/reset")
def reset():
    observation = env.reset()

    return {
        "observation": observation.dict(),
        "reward": 0.0,
        "done": False,
        "info": {}
    }


@app.post("/step")
def step(request: StepRequest):

    action = Action(
        action_type=request.action_type,
        content=request.content
    )

    observation, reward, done, info = env.step(action)

    return {
        "observation": observation.model_dump(),
        "reward": reward,
        "done": done,
        "info": info
    }


@app.get("/state")
def state():

    state = env.state()

    scores = grader.grade_all(state)

    return {
        "state": state.model_dump(),
        "scores": scores
    }

def main():
    uvicorn.run(
        "server.app:app",
        host="0.0.0.0",
        port=7860,
        reload=False
    )


if __name__ == "__main__":
    main()