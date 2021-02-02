# nfl-events-api

# Usage

1. Git clone ```git clone https://github.com/atsushii/nfl-events-api.git```

2. Build image and run container ```docker-compose up --build -d```

3. Send Get request to API with form-data

# unittest coverage

```
Name                                      Stmts   Miss  Cover
-------------------------------------------------------------
project/__init__.py                          20      0   100%
project/config.py                             3      0   100%
project/constants.py                          3      0   100%
project/tests/test_endpoint.py               11      0   100%
project/tests/test_execute_nfl_api.py        28      0   100%
project/tests/test_request_validator.py      23      0   100%
project/utils/__init__.py                     0      0   100%
project/utils/execute_nfl_api.py             57     10    82%
project/utils/validate_request.py            34      0   100%
-------------------------------------------------------------
TOTAL                                       179     10    94%
```

# Stack

Python/Flask/Docker/unittest

# Note

I uploaded the .env file on GitHub which is contained the API key. Because it is a just sample API. I will not do that if it is a real project.



