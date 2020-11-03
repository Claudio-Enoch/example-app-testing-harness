# Example App Testing Harness  
Test automation project in Python to demonstrate testing approach.  
This projects wraps around a password hashing API.  

### Getting Started
- install python3.8+  
- update port in `.env` to match the API's running port
- run `python -m pytest -v tests`

### Framework 
**hash_api/** contains the api controller used to make tests more DRY 
and allow for extensions and logging to be easily added.  
**tests/** have been separated into `test_METHOD_PATH` format;
this is to facilitate readability and expanding the framework as new paths are added.  
**requirements.txt** external libraries used to facilitating testing efforts.

### Notes/Bugs:
#### `POST /hash` 
 - response id should be 'instant' but takes 5 seconds
 - hashing should return 400 for empty json obj
 - the `password` key should be required  
#### `GET /hash` 
 - hash does not return a base64 encoded sha512 password (unless this contains a salt)
 - handled multi processed requests without compounding processing time
 - alphabetical and out of bounds ids result in GO relevant errors `strconv.Atoi: parting...: invalid`
   - these should return "Hash not found" or other non GO language specific errors
#### `GET /stats` 
 - `AverageTime` broken and stays at 0 for most tests
 - `TotalRequests` is sometimes offset from actual requests ids returned
#### `POST /hash {shutdown}`
 - properly handles requests while shutting down (due to bug in POST `/hash`, these results aren't confirmed)
 - requests post shutdown correctly timeout, confirming the shutdown success

### Improvements
Given more time, I would implement logging and test reports into the code base to better explore any failing tests.  
Tests could be marked as expected failures once bugs are logged and accepted.  
The application would be dockerized, to include pulling down or mounting a copy of the hashing APIs executable.  
