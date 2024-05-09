# CV Screening Application

## Description
This CV Screening Application is a web-based tool designed to assist in the automated screening of job applicants' CVs against specific job descriptions. It leverages advanced NLP techniques to evaluate and score CVs based on their relevance to the job requirements.

## Features
- **CV Upload**: Users can upload CVs in PDF or DOCX format.
- **Job Description Upload**: Users can upload job descriptions to which the CVs will be compared.
- **Scoring System**: The application provides a suitability score from 1 to 10.
- **Explanation**: A brief explanation of the score based on the CV and job description analysis.

## Technologies Used
- Flask: For the backend server and API.
- OpenAI's GPT-3.5-turbo: For processing and analyzing CVs.
- Gunicorn: As the WSGI HTTP Server.
- Render: Deployment platform.

## Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/cv-screening-app.git
cd cv-screening-app
