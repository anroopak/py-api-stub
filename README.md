# Py API Stub
Have you ever faced issues with intergration testing of your applications? 
Ever frowned upon by some developer because your APIs are not ready for testing?
Ever slowed down by backend developer for your front-end work?

> <b>Py-api-stub</b> helps you to turn JSON files to powerful APIs service. <br>
> Put in JSON files in a particular folder structure and boom, your API stub is ready.

## Getting started
### API and Folder structure
Consider that you have an api - POST /customer/profile. With py-api-stub, place a `post.json` file with following folder structure - `apis/customer/profile/post.json`. The json file will have the response expected from the API

Yes, what you guessed is right. The file name should be the verb (HTTP method) name.
And yes, your second guess is right. The folder structure is same as your API structure.

> Formulating this:  <br>
> `VERB /x/y/z`  =>  `./apis/x/y/z/verb.json`

### Handling a path variable
`GET /customer/[[customerID]]/profile` => `./apis/customer/:customerID/profile/get.json`

> Path variables should start with `:`

## Features
- [x] default responses for APIs for each of the method
- [x] handle path variables
- [ ] test cases for each of the feature
- [ ] add response codes
- [ ] static response based on path variables
- [ ] simple programmable apis (use an id counter, return the body, etc)
- [ ] add XML support ?


## Installing
### Docker mode
- Build the docker using - `$ docker build -t py-api-stub .`

## Run the stub app with Docker 
- The app runs on port 5000 in the Docker and 8000 on the host
- Command: `$ docker-compose up`
- API is now available on http://localhost:8000

## Maintaining API Stubs
API responses are maintained in the `./apis` folder.

## Contribution guideline
1. create an issue and discuss the requirements and way you plan to develop it
2. create a branch with the name `feat/<issue-id>` 
3. raise a pull request to master.