#! /bin/bash
docker run -p 5000:5000 -v ./questions:/data/questions -v ./answers:/data/answers -e NOMAD_ANSWERS_PATH=/data/answers -e NOMAD_QUESTIONS_PATH=/data/questions nomad-questionnaire
