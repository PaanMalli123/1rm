# 1RM Calculator — Serverless AWS API

A serverless REST API that calculates One Rep Max (1RM) estimates for the three main powerlifting movements using three well established formulas. Built with Python on AWS Lambda and exposed via API Gateway.

**WEBSITE LIVE AT:** 1rm.seenikurulla.online

---

## Architecture

```
Client → API Gateway → Lambda (Python) → JSON Response
```

The frontend is a static HTML page hosted on S3 and served through CloudFront and made secure using ACM SSL certificates.

---

## The Formulas

Three formulas are used and their average is returned, giving a more reliable estimate than any single formula alone.

| Formula  | Equation                                        |
|----------|-------------------------------------------------|
| Epley    | `weight × (1 + reps / 30)`                     |
| Brzycki  | `weight × (36 / (37 - reps))`                  |
| Lander   | `(100 × weight) / (101.3 - 2.67123 × reps)`    |

---

## Example Request

```bash
curl -X POST https://your-api-id.execute-api.region.amazonaws.com/prod/calculate \
  -H "Content-Type: application/json" \
  -d '{"lift": "squat", "weight": 100, "reps": 5, "unit": "kg"}'
```

**Response:**
```json
{
    "lift": "squat",
    "weight": 100,
    "reps": 5,
    "unit": "kg",
    "results": {
        "epley": 116.67,
        "brzycki": 112.5,
        "lander": 113.71,
        "average": 114.29
    }
}
```

---


## Stack

- **Compute:** AWS Lambda (Python 3.x)
- **API:** AWS API Gateway (REST API)
- **Frontend:** S3 + CloudFront
- **DNS:** Route 53 + ACM
- **Monitoring:** CloudWatch (automatic)
- **IAM:** AWSLambdaBasicExecutionRole only

---

