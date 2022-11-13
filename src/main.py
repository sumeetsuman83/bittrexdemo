from fastapi import FastAPI, Body, Depends
import uvicorn
import hashlib
import hmac
import json
import os
import requests
import sys
import time
from CheckSchema import UserSignupSchema, UserLoginSchema
from JwtUtils import SignJwt, JwtBearer
import json
import ast
from PasswordUtils import EncryptPassword, DecryptPassword
from decouple import config

api_key = config("api_key")
api_private_key = config("api_private_key")


app=FastAPI()
logindatapath=config("logindatapath")


@app.get("/healthcheck")
def HealthCheck():
    return {"Status":200,"Message":"The service is working fine"}


@app.get("/summary/markets",dependencies=[Depends(JwtBearer())])
def GetMarketSummary():
    url = config("allmarketsummary")
    timestamp = str(int(time.time()*1000))
    payload=""
    if (isinstance(payload, dict)):
        content_hash = hashlib.sha512(bytes(json.dumps(payload), "utf-8")).hexdigest()
    else:
        content_hash = hashlib.sha512(payload.encode()).hexdigest()
    presign = timestamp + url + "GET" + content_hash
    signature = hmac.new(api_private_key.encode(), presign.encode(), hashlib.sha512).hexdigest()
    headers = {
          'Api-Key': api_key,
          'Api-Timestamp': timestamp,
          'Api-Content-Hash': content_hash,
          'Api-Signature': signature
    }
    return requests.get(url, headers=headers).json()
    

@app.get("/summary/market/{cmpname}",dependencies=[Depends(JwtBearer())])
def GetCompanySummary(cmpname: str):
    url=config("onecompanysummary")
    url = f'{url}{cmpname}/summary'
    timestamp = str(int(time.time()*1000))
    payload=""
    if (isinstance(payload, dict)):
        content_hash = hashlib.sha512(bytes(json.dumps(payload), "utf-8")).hexdigest()
    else:
        content_hash = hashlib.sha512(payload.encode()).hexdigest()
    presign = timestamp + url + "GET" + content_hash
    signature = hmac.new(api_private_key.encode(), presign.encode(), hashlib.sha512).hexdigest()
    headers = {
          'Api-Key': api_key,
          'Api-Timestamp': timestamp,
          'Api-Content-Hash': content_hash,
          'Api-Signature': signature
    }
    return requests.get(url, headers=headers).json()




@app.post("/user/register")
def CreateUser(user: UserSignupSchema = Body(...)):
    print(logindatapath)
    with open(logindatapath) as f:
        data = json.load(f)
    # data=ast.literal_eval(data)
    print(data)
    print(type(data))
    if len([i for i in data if i["Email"]==str(user.email)])>=1:
        return {"Status":200,"Message":"Email Id already registered"}
    encryptedpass=EncryptPassword(user.password)
    data.append({"Email":str(user.email),"Password":encryptedpass.decode()})
    with open(logindatapath, "w") as final:
        json.dump(data, final)
    return {"Status":201,"Message":"User successfully registered"}





@app.post("/user/login")
def UserLogin(user: UserLoginSchema = Body(...)):
    if CheckUser(user):
        return SignJwt(user.email)
    return {
        "error": "Wrong login details!"
    }


def CheckUser(data: UserLoginSchema):
    with open(logindatapath) as f:
        data_ = json.load(f)
    print(type(data_))
    password=[i["Password"] for i in data_ if i["Email"]==data.email][0].encode('utf-8')
    print(password)
    if DecryptPassword(password)==data.password:
            return True
    return False




if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0",port=5000)