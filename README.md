# Minimal Image FastAPI Endpoints

### A quick and easy to use template to create image CRUD apps. Built around FastAPI and using Pydantic data models for fast queries. 

---

## Main objectives

- To create a light and easily configurable barebones backend API solution to handle image CRUD.

- To provide an index of uploaded images to 

- Allow for basic filter based image manipulation. (ie adjusting HSV, blurring, denoise etc.)

## Main Features

- Supports b64 and binary encoding for image blob handling.
- Image statistics and metrics endpoint for quick querying and sorting of image data.
- Saving image from endpoint to local storage.  
- Basic user authentication via JWT and support for guest interactions.
- Database integration for user login and statistics.
- Dynamic in-memory or disk caching of images.
- Quickly pull images from an URL link or local file on the server.

## Requirements


Based on `fastapi-nano` by rednafi : https://github.com/rednafi/fastapi-nano