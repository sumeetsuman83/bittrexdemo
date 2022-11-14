
# Bittrex-Demo
It is a micro-service app to fetch crypto currency market updates from below
site.

https://bittrex.github.io/api/v3
https://bittrex.github.io/api/v3#tag-Markets





## API Reference

#### Createuser

```http
  POST /user/register
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `fullname` | `string` |**Required**. Name of new user |
| `email` | `string` | **Required**. Email id of new user |
| `password` | `string` | **Required**. Password for new user |

It returns a json response with messages like {
  "Status": 201,
  "Message": "User successfully registered"
} if the registration is successfull
or
{
  "Status": 200,
  "Message": "Email Id already registered"
} if the user is already registered.

#### UserLogin

```http
  POST /user/login
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `email` | `string` | **Required**. Email id of the registerd user |
| `password` | `string` | **Required**. Password for user login |

This api is used to login and if the email and password matches in out database, a JwtBearer token will be returned back as a json response and that token is required to call the other api's to get market summary.
eg:
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoic3VtZWV0c3VtYW42M0BnbWFpbC5jb20iLCJleHBpcmVzIjoxNjY4NDM5MzgyLjQ1MjA1OH0.g8NyZ_qODfaJeqiA3BzoZlxB9sRv6SruLy5R8nVnEOQ"
}
This token will be valid for next 10 mins.


#### CompleteMarketSummary

```http
  GET /summary/markets
```
It needs a JwtBearer token to access. This api will return a json response with all market summary.

#### MarketSummaryforsinglemarket

```http
  GET /summary/market/{cmpname}
```
"cmpname" refers to the market for which details are required.
It needs a JwtBearer token to access. This api will return a json response with "cmpname" company market summary.
IF the "cmpname" is invalid it will return below response:
{
  "code": "MARKET_DOES_NOT_EXIST"
}

#### HealthCheck

```http
  GET /healthcheck
```
It return a json response as 
{
  "Status": 200,
  "Message": "The service is working fine"
}
if the container is up and running

##  Implementation Steps
1) We need to "api_key" and "api_private_key" to access Bittrex market.Those two keys needs to be put in the .env file present in ./src folder.
2) To create this keys please follow steps given in this post "https://bittrex.zendesk.com/hc/en-us/articles/360031921872-How-to-create-an-API-key-".
3) Clone this repo.
3) Write down the keys in .env file we can directly run "docker-compose up --build" to build and start the micro-service.
4) Create a new user.
5) Login and get the JWT token.This token will be valid for 10 mins.
6) Use the token to get market summary.
## Authors

- [sumeetsuman83](https://github.com/sumeetsuman83)

