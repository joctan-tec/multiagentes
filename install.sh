#!/bin/bash
docker build -t multiagent-rag .
docker run --rm -p 8000:8000 -p 5000:5000 multiagent-rag