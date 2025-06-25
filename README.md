# FastAPI RAG Project

This project is a Retrieval-Augmented Generation (RAG) application built with FastAPI, Streamlit, and a PostgreSQL database with the pgvector extension.

## Features

- **FastAPI Backend:** A robust backend that provides an API for the RAG chain.
- **Streamlit Frontend:** A simple and interactive web interface for asking questions.
- **Wikipedia Knowledge Base:** The application scrapes Wikipedia articles to build its knowledge base.
- **Containerized:** The application is fully containerized using Podman, making it easy to run and deploy.
- **Deployable on Render:** Includes a `render.yaml` file for easy deployment to Render.

## Running Locally

To run the application locally, you need to have Podman installed. You also need to set your Gemini API key as an environment variable.

1.  **Set the Gemini API Key:**

    ```bash
    export GEMINI_API_KEY="YOUR_API_KEY"
    ```

2.  **Run the Application:**

    ```bash
    podman-compose up --build
    ```

    If you don't have `podman-compose` installed, you can run the services individually:

    ```bash
    # Create a network
    podman network create rag-network

    # Start the database
    podman run -d --name db --network rag-network -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=vectordb -v postgres_data:/var/lib/postgresql/data docker.io/pgvector/pgvector:pg16

    # Build and run the backend
    podman build -t backend -f backend.Dockerfile .
    podman run -d --name backend --network rag-network -p 8000:8000 -e DATABASE_URL=postgresql://user:password@db:5432/vectordb -e GEMINI_API_KEY=$GEMINI_API_KEY backend

    # Build and run the frontend
    podman build -t frontend -f frontend.Dockerfile .
    podman run -d --name frontend --network rag-network -p 8501:8501 -e BACKEND_URL=http://backend:8000 frontend
    ```

    The frontend will be available at `http://localhost:8501`.

This project includes two deployment options to showcase a range of skills:

1.  **Render (PaaS):** For easy, one-click deployment to a live URL.
2.  **Kubernetes:** For demonstrating advanced container orchestration skills on a Kubernetes cluster.

## Deployment Option 1: Render (Live Demo)

This project is configured for easy deployment to Render, a Platform-as-a-Service provider.

1.  Click the "Deploy to Render" button (you can create one that links to `https://render.com/deploy?repo=YOUR_GITHUB_REPO_URL`).
2.  Connect your GitHub repository.
3.  Render will automatically detect the `render.yaml` file and deploy the services.
4.  You will need to set the `GEMINI_API_KEY` as a secret in the Render dashboard for the `backend` service.

## Deployment Option 2: Kubernetes

To run the application on a Kubernetes cluster, you need to have `kubectl` and a local cluster (like `minikube` or `kind`) installed.

### 1. Build and Load Images

Kubernetes needs access to your container images. First, build them, then load them into your local cluster.

If you are using `minikube`, you can point your terminal to its Docker environment:

```bash
# This command configures your shell to use minikube's Docker daemon
eval $(minikube -p minikube docker-env)

# Build the images directly inside minikube's environment
podman build -t localhost/backend:latest -f backend.Dockerfile .
podman build -t localhost/frontend:latest -f frontend.Dockerfile .

# (Optional) Unset the minikube docker-env when you're done
# eval $(minikube docker-env -u)
```

### 2. Apply the Manifests

Deploy the application to your cluster using the Kustomize configuration:

```bash
kubectl apply -k kubernetes/
```

### 3. Access the Application

To access the frontend, use the `minikube service` command to get the URL:

```bash
minikube service frontend --url
```

This will open the application in your browser.
