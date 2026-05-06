# Job Listing API Documentation

## 1. Get All Jobs
GET /api/jobs/
Description: Returns all active jobs

---

## 2. Featured Jobs
GET /api/jobs/?featured=true

---

## 3. Latest Jobs
GET /api/jobs/?latest=true

---

## 4. Search Jobs
GET /api/jobs/?search=python

Description:
Search jobs using keyword (title, description)

---

## 5. Filters

### Skill Filter
GET /api/jobs/?skill=python

### Location Filter
GET /api/jobs/?location=bangalore

### Salary Filter
GET /api/jobs/?min_salary=20000

### Experience Filter
GET /api/jobs/?experience=2

### Job Type Filter
GET /api/jobs/?job_type=full_time

---

## 6. Pagination
GET /api/jobs/?page=1

---

## Sample Response

[
  {
    "id": 1,
    "title": "Python Developer",
    "company": "TCS",
    "location": "Bangalore",
    "salary": 30000
  }
]