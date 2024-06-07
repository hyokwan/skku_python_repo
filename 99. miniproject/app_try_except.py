# -*- coding: utf-8 -*-
"""app.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1NTz03Lt6xH696dd3KJRDOUmTOH251flH
"""

# Commented out IPython magic to ensure Python compatibility.
!pip install fastapi uvicorn
!pip install  nest-asyncio pyngrok
from google.colab import drive
drive.mount("/content/gdrive")
# %cd /content/gdrive/MyDrive/Colab Notebooks/code2024/Session - 미니프로젝트

"""# 모델 불러오기"""

import pickle
from tensorflow.keras.models import load_model
import pandas as pd

# 서버 관리용 fastapi 의존 라이브러리
import uvicorn

# fast api 라이브러리
from fastapi import FastAPI

# 인터페이스 데이터 관리를 위한 라이브러리
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware
origins = ["*"]

app = FastAPI(title="ML API")

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 origin 허용
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

with open("./dlcore_sellout_skku.dump","rb") as fr:
    loadedRef = pickle.load(fr)
# 0:feature 1: labels 2: preprocessing
# loadedRef

loadedRef

class InDataset(BaseModel):
    inPromotion : str
    inHoliday : str
    inPropercent : float
    inHclus : int

loadedModel = load_model("./dlcore_sellout_skku_last.h5")

loadedModel.summary()

loadedRef

preProcessingFunc = loadedRef["preprocessing"]

# 전처리 함수 불러오기
ynLabel = preProcessingFunc[0]
promotionScaler = preProcessingFunc[2]
hclusScaler = preProcessingFunc[3]

@app.post("/predictdl", status_code=200)
async def predictDl(x:InDataset):
    try:
        print(x)
        # 화면입력데이터 변수 할당
        inPromotion = x.inPromotion
        inHoliday = x.inHoliday
        inPropercent =x.inPropercent
        inHclus = x.inHclus
        print("step1")
        # 입력데이터 전처리
        inPromotionCvt = ynLabel.transform( [inPromotion] )[0]
        inHolidayCvt = ynLabel.transform( [inHoliday] )[0]
        inPropercentCvt = promotionScaler.transform( [[inPropercent]] )[0][0]
        inHclusCvt = hclusScaler.transform( [[inHclus]] )[0][0]
        print("step2")
        # 예측을 위한 데이터셋 생성
        testData = pd.DataFrame( [[ inPromotionCvt, inHolidayCvt, inPropercentCvt, inHclusCvt ]] )
        # 예측
        print(testData)
        predictValue =  int(loadedModel.predict( testData)[0][0])
        print(predictValue)
        result = {"prediction":predictValue}
    except Exception as e:
        print(e)
        result = {"prediction":"00"}
    return result

# # print(x)
# # 화면입력데이터 변수 할당
# # inPromotion = x.inPromotion
# # inHoliday = x.inHoliday
# # inPropercent =x.inPropercent
# # inHclus = x.inHclus
# inPromotion = "N"
# inHoliday = "N"
# inPropercent = 0.0
# inHclus = 1
# print("step1")
# # 입력데이터 전처리
# inPromotionCvt = ynLabel.transform( [inPromotion] )[0]
# inHolidayCvt = ynLabel.transform( [inHoliday] )[0]
# inPropercentCvt = promotionScaler.transform( [[inPropercent]] )[0][0]
# inHclusCvt = hclusScaler.transform( [[inHclus]] )[0][0]
# print("step2")
# # 예측을 위한 데이터셋 생성
# testData = pd.DataFrame( [[ inPromotionCvt, inHolidayCvt, inPropercentCvt, inHclusCvt ]] )
# # 예측
# print(testData)
# predictValue =  int(loadedModel.predict( testData)[0][0])
# print(predictValue)
# result = {"prediction":predictValue}
# result

@app.get("/")
async def root():
    return {"message":"server is running"}

import nest_asyncio
from pyngrok import ngrok
import uvicorn

auth_token = "2hN39uPNEVwsHR4UMPoPQpGTI21_3eQv6mRq5YK8zjdv9Es5v"
ngrok.set_auth_token(auth_token)
ngrokTunnel = ngrok.connect(8000)
print("공용 URL", ngrokTunnel.public_url)
nest_asyncio.apply()
uvicorn.run(app, port=8000)

# import uvicorn
# if __name__ == "__main__":
#     uvicorn.run("app:app", host="0.0.0.0", port=9999, log_level="debug",
#                 proxy_headers=True, reload=True)

