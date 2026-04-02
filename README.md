---
title: Customer Support OpenEnv
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
app_file: server/app.py
pinned: false
---

# Customer Support OpenEnv

## Overview

Customer Support OpenEnv is a real-world AI environment where agents simulate customer support workflows.  
Agents must classify issues, respond appropriately, and resolve customer tickets.

This environment follows the OpenEnv specification and supports reinforcement learning agents.

---

## Features

- Real-world customer support simulation
- Multi-step workflow
- 3 difficulty levels (easy → medium → hard)
- Deterministic grading
- Dense reward signals
- OpenEnv compliant
- Dockerized deployment

---

## Tasks

### Easy Task

**Objective:** Classify customer issue

Example:

Customer: "My payment failed"

Agent must classify: billing

Scoring:
- Correct classification: 1.0
- Incorrect: 0.0

---

### Medium Task

**Objective:** Classify + Respond

Agent must:
1. Classify issue
2. Respond to customer

Scoring:
- Classification: 0.5
- Response: 0.5

---

### Hard Task

**Objective:** Full customer support workflow

Agent must:
1. Classify
2. Respond
3. Resolve

Scoring:
- Classification: 0.3
- Response: 0.3
- Resolve: 0.4

---

## Action Space
{
"action_type": string,
"content": string
}


Available actions:

- classify
- respond
- resolve

---

## Observation Space
{
"ticket_id": string,
"customer_message": string,
"conversation_history": list,
"available_actions": list,
"status": string
}

---

## Reward

Reward range: 0.0 - 1.0

Dense reward:
- classification reward
- response reward
- resolution reward

---

## Setup

### Install dependencies
pip install fastapi uvicorn pydantic openenv-core requests openai

---

### Run server
uvicorn server.app:app --host 0.0.0.0 --port 7860

---

### Test API

Open: http://localhost:7860/docs

---

## Docker

Build container: docker build -t customer-support-env .

Run container: docker run -p 7860:7860 customer-support-env

---

## Inference

Set environment variables:export OPENAI_API_KEY=your_key

Run baseline: python inference.py

---

## OpenEnv Validation

Run: openenv validate

---

## Deployment

Deploy to Hugging Face Spaces:

- Container: Docker
- Port: 7860
- Tag: openenv

---

## Motivation

Customer support automation is one of the most important real-world AI tasks.  
This environment allows training and evaluating agents in realistic workflows.

---

## License

MIT License
