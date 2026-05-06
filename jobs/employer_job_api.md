# Employer Job Creation API

## Endpoint
POST /api/jobs/create/

---

## Description
Allows employers to create new job postings.

---

## Request Body

{
  "title": "Python Developer",
  "description": "Django developer required",
  "company": "Infosys",
  "skills": "Python, Django",
  "experience": 2,
  "salary": 30000,
  "location": "Bangalore",
  "job_type": "full_time"
}

---

## Response

{
  "message": "Job created successfully"
}

---

## Security

- Only employers can access this API
- Authentication required