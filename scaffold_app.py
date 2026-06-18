import os
import json

def write_file(path, content):
    dirname = os.path.dirname(path)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# Frontend setup
write_file("frontend/package.json", json.dumps({
  "name": "frontend",
  "private": True,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "preview": "vite preview",
    "test": "vitest run --coverage"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.66",
    "@types/react-dom": "^18.2.22",
    "@typescript-eslint/eslint-plugin": "^7.2.0",
    "@typescript-eslint/parser": "^7.2.0",
    "@vitejs/plugin-react": "^4.2.1",
    "eslint": "^8.57.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.6",
    "typescript": "^5.2.2",
    "vite": "^5.2.0",
    "vitest": "^1.4.0",
    "@vitest/coverage-v8": "^1.4.0"
  }
}, indent=2))

write_file("frontend/vite.config.ts", """// purpose: Frontend build config | enforces: Efficiency-first
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      thresholds: {
        lines: 98,
        functions: 98,
        branches: 98,
        statements: 98
      }
    }
  }
})
""")

write_file("frontend/src/App.test.tsx", """// purpose: Verify basic render | enforces: Test-first
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import React from 'react';

const App = () => <h1>Sustainability Super-App</h1>;

describe('App', () => {
  it('renders headline', () => {
    const { container } = render(<App />);
    expect(container.textContent).toMatch(/Sustainability Super-App/i);
  });
});
""")

write_file("frontend/index.html", """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Sustainability Super-App</title>
  </head>
  <body>
    <div id="root"></div>
  </body>
</html>
""")

# Backend setup
write_file("backend/pyproject.toml", """[tool.poetry]
name = "backend"
version = "0.1.0"
description = ""
authors = ["Admin <admin@example.com>"]

[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.110.0"
uvicorn = "^0.29.0"

[tool.poetry.group.dev.dependencies]
pytest = "^8.1.1"
pytest-cov = "^5.0.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.pytest.ini_options]
addopts = "--cov=app --cov-report=term-missing --cov-fail-under=98"
""")

write_file("backend/app/main.py", """# purpose: App entrypoint | enforces: Quality-first
from fastapi import FastAPI
from app.core.security import add_security_headers

app = FastAPI()

@app.middleware("http")
async def add_security_headers_middleware(request, call_next):
    response = await call_next(request)
    return add_security_headers(response)

@app.get("/health")
def health_check():
    return {"status": "ok"}
""")

write_file("backend/app/core/security.py", """# purpose: Core security | enforces: Security-first
def add_security_headers(response):
    response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response
""")

write_file("backend/tests/test_main.py", """# purpose: Verify app health | enforces: Test-first
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert "Strict-Transport-Security" in response.headers
""")

# Infra
write_file("docker-compose.yml", """version: '3.8'
services:
  backend:
    build:
      context: ./backend
    ports:
      - "8000:8000"
    environment:
      - ENV=local
  
  firebase-emulators:
    image: spine3/firebase-emulator:latest
    ports:
      - "8080:8080" # Firestore
      - "9099:9099" # Auth
      - "9199:9199" # Storage
      - "4000:4000" # UI
""")

write_file("backend/Dockerfile", """FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml .
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-root
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
""")

write_file("infra/firebase/firebase.json", json.dumps({
  "firestore": {
    "rules": "firestore.rules"
  },
  "storage": {
    "rules": "storage.rules"
  },
  "emulators": {
    "auth": { "port": 9099 },
    "firestore": { "port": 8080 },
    "storage": { "port": 9199 },
    "ui": { "enabled": True }
  }
}, indent=2))

write_file("infra/firebase/.firebaserc", json.dumps({
  "projects": {
    "default": "prompt-wars-project-3"
  }
}, indent=2))

write_file("infra/firebase/firestore.rules", """// purpose: Secure Firestore | enforces: Security-first
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if false; // Deny by default
    }
  }
}
""")

write_file("infra/firebase/storage.rules", """// purpose: Secure Storage | enforces: Security-first
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /{allPaths=**} {
      allow read, write: if false;
    }
  }
}
""")

print("App scaffolding completed.")
