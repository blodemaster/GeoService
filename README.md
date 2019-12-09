## Micro GeoService on Flask

This repo contains a web application, offering geolocation service for geocoding and reverse geocoding in an asynchronous manner.

It is built with Flask, Redis, Celery, and Docker.

### Prerequisite
The application is designed to be running with docker compose. Therefore, you need to have docker installed.

### Getting started

```sh
docker-compose up --build
```

By default, the web application will be running at localhost `http://127.0.0.1:5000/`. I have provided
a basic UI page for using the service.

### Environment Variables

Be aware you might need to tweak the environment variables based on your needs. 
They are available at **variable.env**. 

### Testing
The testing is done using the Python native library unittest. 
Since the test should be running on local computer, you should have all dependencies installed inside `requirements.txt`.

To run the test, 

```sh
python tests/app.py
python tests/tasks.py
```

### Technology choices

- Flask: since the offered service is relatively simple, I choose it as it is the most widely used micro web framework for Python
- Redis: used as the message broker for Celery. It is stable and can be used for other purposes like caching
- Celery: async task queue for processing input. It is widely used and I have used it a lot.
- Vue.js: front-end framework for building the UI part. It is selected out of the familiarity.
- Gunicorn: web server for running application for production purpose

### API

As there are only four endpoints, API will be documented here as plain text.

**Geocode**

Submit the valid request as an async task for geocoding and return the location for fetching the task status and result

* **URL**:  `/geocode`
* **Method:**: `GET`
*  **URL Params**:

   `address=[str]`: valid geographic address 

* **Success Response:**

  * **Code:** 202 Accepted <br />
    **HEADERS:** `Content-Type: application/json, Location: /geocode/task/:task_id/status`
 
* **Error Response:**

  * **Code:** 400 Bad Request <br />
    **Content:** `{ error : "missing address" }`

* **Sample Call:**

  ```Python
    request.get('http://localhost:5000/geocode?address=H.+C.+Andersens+Blvd.+27,+1553+K%C3%B8benhavn+V,+Denmark')
  ```

**Geocode Task Status**

Return the task status for geocoding.

It should be got from the `Location` Headers of the geocode endpoint 

* **URL**:  `/geocode/task/:task_id/status`
* **Method:**: `GET` | `DELETE`
*  **URL Params**:

   `task_id=[str]`: 

* **Success Response:**

  * GET request
      * **Code:** 200 OK <br />
        **Content:** `{ task_id : "1234556", 'state': SUCCESS, 'result': [55.674146, 12.569553] }`
        **Description:** get coordinates back
      
      * **Code:** 200 OK <br />
        **Content:** `{ task_id : "1234556", 'state': SUCCESS, 'error': 'connect to the server failed' }`
        **Description:** cannot connect to the third party geoservice provider
        
      * **Code:** 200 OK <br />
        **Content:** `{ task_id : "1234556", 'state': STARTED }`
        **Description:** the task has started but does not receive the outcome yet
        
  * DELETE request
      * **Code:** 204 No Content 


**Reverse Geocode**

Submit the valid request as an async task for obtaining the address of provided coordinates 
and return the location for fetching the task status and result

* **URL**:  `/reverse_geocode`
* **Method:**: `GET`
*  **URL Params**:

   `cooridnates=[str]`: valid geographic coordinates by putting longitude after altitude with comma in between

* **Success Response:**

  * **Code:** 202 Accepted <br />
    **HEADERS:** `Content-Type: application/json, Location: /reverse-geocode/task/:task_id/status`
 
* **Error Response:**

  * **Code:** 400 Bad Request <br />
    **Content:** `{ error : "missing address" }`
    
  * **Code:** 400 Bad Request <br />
    **Content:** `{ error : "invalid coordinate" }`
     

* **Sample Call:**

  ```Python
    request.get('http://localhost:5000/reverse-geocode?coordinate=55.674146,12.569553')
  ```

**Reverse Geocode Task Status**

Return the task status for geocoding.

It should be got from the `Location` Headers of the reverse geocode endpoint 

* **URL**:  `/reverse-geocode/task/:task_id/status`
* **Method:**: `GET` | `DELETE`
*  **URL Params**:

   `task_id=[str]`: 

* **Success Response:**

  * GET request
      * **Code:** 200 OK <br />
        **Content:** `{ task_id : "1234556", 'state': SUCCESS, 'result': 'Tivoli, H.C. Andersens Boulevard, Kødbyen, Vesterbro, København, Københavns Kommune, Region Hovedstaden, 1553, Danmark' }`
        **Description:** get coordinates back
      
      * **Code:** 200 OK <br />
        **Content:** `{ task_id : "1234556", 'state': SUCCESS, 'error': 'connect to the server failed' }`
        **Description:** cannot connect to the third party geoservice provider
        
      * **Code:** 200 OK <br />
        **Content:** `{ task_id : "1234556", 'state': STARTED }`
        **Description:** the task has started but does not receive the outcome yet
        
  * DELETE request
      * **Code:** 204 No Content 
