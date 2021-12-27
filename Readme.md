# API Request Validation

This repository contains the code for the example described in the blog.

### Installing and executing

```bash
pipenv install
pipenv run python app.py
```

Then after try raising these requests and observe the responses

**This is for the success request.**
```bash
curl --location --request POST '127.0.0.1:5000' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": {
        "first": "Sam",
        "middle": "",
        "last": "Paul"
    },
    "date_of_birth": "2021-09-12",
    "gender": "m",
    "address": {
        "flat_number": "21",
        "locality": "kumbha marg",
        "landmark": "near josheph church",
        "pincode": "600094"
    },
    "social_presence": [
        {
            "site_name": "linkedin",
            "site_url": "https://linkedin.com/sampaul"
        },
        {
            "site_name": "github.com",
            "site_url": "https://github.com/sampaul"
        }
    ]
}'
```

**This is for the failure response**
```bash
curl --location --request POST '127.0.0.1:5000' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": {
        "first": "Sam",
        "middle": "",
        "last": false
    },
    "date_of_birth": "2021-13-12",
    "gender": "k",
    "address": {
        "locality": "kumbha marg",
        "landmark": "near josheph church",
        "pincode": "600094"
    },
    "social_presence": [
        {
            "site_name": "linkedin",
            "site_url": "https://linkedin.com/sampaul"
        },
        {
            "site_name": "github.com",
            "site_url": "https://github.com/sampaul"
        }
    ]
}'
```