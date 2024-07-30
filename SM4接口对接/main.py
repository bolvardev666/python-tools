from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from gmssl import sm4
import base64, json

app = FastAPI()


class Section(BaseModel):
    ORG_CODE: Optional[str] = None
    ORG_NAME: Optional[str] = None
    ORG_SIMPLE: Optional[str] = None
    PARENT_ORG_CODE: Optional[str] = None
    ORG_STATE: Optional[int] = None
    ORG_LEVEL: Optional[int] = None
    ORG_TYPE: Optional[int] = None
    ISFICTITIOUS: Optional[int] = None
    SORT_NO: Optional[int] = None
    AGENCY: Optional[int] = None
    REGION_CODE: Optional[str] = None
    COUNTY_CODE: Optional[str] = None
    WORKADDRESS: Optional[str] = None
    ORG_TEL: Optional[str] = None
    ORG_CONTACT: Optional[str] = None
    ORG_MAIL: Optional[str] = None
    FAXADDRESS: Optional[str] = None
    REMARK: Optional[str] = None
    EXTEND1: Optional[str] = None
    EXTEND2: Optional[str] = None


class Data(BaseModel):
    SERVICEID: Optional[str] = None
    MODIFYTYPE: Optional[str] = None
    ORGLIST: List[Section] = None
    ORG_CODE: Optional[str] = None
    ORG_NAME: Optional[str] = None
    ORG_SIMPLE: Optional[str] = None
    PARENT_ORG_CODE: Optional[str] = None
    ORG_STATE: Optional[int] = None
    ORG_LEVEL: Optional[str] = None
    ORG_TYPE: Optional[str] = None
    ISFICTITIOUS: Optional[int] = None
    SORT_NO: Optional[str] = None
    AGENCY: Optional[int] = None
    REGION_CODE: Optional[str] = None
    COUNTY_CODE: Optional[str] = None
    WORKADDRESS: Optional[str] = None
    ORG_TEL: Optional[str] = None
    ORG_CONTACT: Optional[str] = None
    ORG_MAIL: Optional[str] = None
    FAXADDRESS: Optional[str] = None
    REMARK: Optional[str] = None
    EXTEND1: Optional[str] = None
    EXTEND2: Optional[str] = None


class UserListInfo(BaseModel):
    IDCARD: Optional[str]
    LOGIN_NO: Optional[str]
    USER_NAME: Optional[str]
    GENDER: Optional[str]
    ORG_CODE: Optional[int]
    EMAIL: Optional[str] = None
    MOBILE: Optional[str] = None
    PASSWORD: Optional[str] = None
    TEL: Optional[str] = None
    STATUS: Optional[int]
    EFFECT_DATE: Optional[str]
    EXPIRE_DATE: Optional[str]
    REMARK: Optional[str] = None
    USER_TYPE: Optional[int] = None
    REGION_CODE: Optional[str] = None
    COMPANY_CODE: Optional[str] = None
    BZ1: Optional[str] = None
    BZ2: Optional[str] = None


class User(BaseModel):
    SERVICEID: Optional[str]
    MODIFYTYPE: Optional[str]
    USERLIST: List[UserListInfo]


class EncryptData(BaseModel):
    ENCODEPARAM: str


@app.post("/demo")
def root(edata: EncryptData):
    json_data = decrypt(edata.ENCODEPARAM)
    section = Data(**json_data)
    return section


@app.post("/user")
def get_user(edata: EncryptData):
    print(edata)
    json_data = decrypt(edata.ENCODEPARAM)
    data = User(**json_data)
    return data


def decrypt(data):
    sm4_obj = sm4.CryptSM4()
    key = "xxx".encode('utf-8')
    sm4_obj.set_key(key, sm4.SM4_DECRYPT)
    encoded_data = base64.b64decode(data)
    de_data = sm4_obj.crypt_ecb(encoded_data)
    str_data = de_data.decode("utf-8")
    json_data = json.loads(str_data)
    return json_data
