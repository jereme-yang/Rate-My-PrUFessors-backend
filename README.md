# GatorEvals Scraper & API Backend

This repository powers the GatorEvals integration in the [Rate My PRUFessors browser extension](https://github.com/jereme-yang/Rate-My-PrUFessors).

The browser extension enhances the ONE.UF course search by displaying both **Rate My Professors (RMP)** and **GatorEvals** ratings directly alongside each instructor’s name. While RMP ratings are fetched live via GraphQL, GatorEvals ratings are served through a custom API powered by this repository.

## Overview

This repository contains:

- A **GitHub Actions workflow** to automatically scrape data from [GatorEvals](https://gatorevals.aa.ufl.edu/)
- Python scripts to clean and process the data
- AWS Lambda function code to serve scraped data through a public REST API
- DynamoDB integration to store professor evaluation data

## Features

- ✅ Fully automated scraping pipeline using **GitHub Actions**
- 📦 Data hosted in **DynamoDB** and served by **AWS Lambda**
- 🔁 Easily updatable and extensible backend
- 🔒 API access can be restricted to prevent unauthorized usage (e.g. API key, IAM roles, or IP whitelisting)

## Usage

### 1. Scraping GatorEvals

The scraping logic is implemented in `scraper.py` and scheduled to run via GitHub Actions. The workflow parses instructor evaluations and formats them into a JSON structure.

You can run the scraper manually with:

```bash
python scraper.py
```

The output will be saved as evals.json

## Deploying to AWS

The AWS Lambda function is located in the `lambda/` directory. After running the scraper and generating the latest `evals.json`, you can upload the data to DynamoDB and deploy the Lambda function to serve it.

### Steps to Deploy

1. **Upload Data to DynamoDB**

   - Use the AWS Console or a script to update your DynamoDB table with the contents of `evals.json`.
   - Make sure the table has a primary key that matches how your Lambda function queries professor names.

2. **Deploy Lambda Function**

   - The Lambda function handler is located in `lambda/handler.py` (or `index.js` if using Node.js).
   - You can deploy it manually using the AWS Console, or automate it using:

     - **AWS SAM CLI**
     - **Terraform**
     - **Serverless Framework**

3. **Set Up API Gateway**

   - Connect the Lambda function to an API Gateway to expose it as a public REST endpoint.
   - Example endpoint:  
     ```
     GET /?profname=Shu%20Huang
     ```

4. **(Optional) Secure the API**

   - Enable authentication with an API key or AWS IAM roles
   - Restrict access with IP whitelisting or usage plans
   - Configure CORS to allow only requests from trusted domains (like your browser extension)

### Example API Response

```json
{
  "d1": 1.4,
  "d2": 3.5,
  "d3": 1.4,
  "d4": 3.5,
  "d5": 1.4,
  "d6": 3.5
}
```
