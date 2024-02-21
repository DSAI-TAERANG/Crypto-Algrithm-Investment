#!/usr/bin/env python
# coding: utf-8

# In[9]:


pip install pyupbit


# In[10]:


#라이브러리 불러오기

import time
import pyupbit
import datetime
import requests


# In[11]:


# API KEY 접속하기

access = "bx0aPM9RQxqW2bZGJAYNZUb5V9xRxr3uDQ5MxSWS"
secret = "VIYIGdoiCDten39kGP1RcISz4bVQIQKR2nZ1VXhx"
upbit = pyupbit.Upbit(access, secret)


# In[31]:


#전략 target price 함수

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price


# In[23]:


# OHICV 확인해보기

ticker="KRW-BTC"
df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
print(df)


# In[32]:


# 시작 시간 받아오는 함수

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time


# In[33]:


def get_ma15(ticker):
    """15일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=15)
    ma15 = df['close'].rolling(15).mean().iloc[-1]
    return ma15


# In[34]:


def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0


# In[35]:


def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]


# In[36]:


# 로그인

upbit = pyupbit.Upbit(access, secret)
print("autotrade start")


# In[ ]:


# 자동매매 시작

while True: #무한 루프 생성
    try:
        now = datetime.datetime.now() #현재 시간 얻기
        start_time = get_start_time("KRW-BTC") #시작 시간
        end_time = start_time + datetime.timedelta(days=1) #다음날 시간 얻기

        if start_time < now < end_time - datetime.timedelta(seconds=10): #매수 조건 (10초를 빼서 8시 59분 50초까지)
            target_price = get_target_price("KRW-BTC", 0.5) #변동성 돌파 전략 
            ma15 = get_ma15("KRW-BTC") #15일 이동평균선 가져오기
            current_price = get_current_price("KRW-BTC") #현재가 조회
            if target_price < current_price and ma15 < current_price:
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order("KRW-BTC", krw*0.9995) #수수료 고려
                    
        else: #매도 조건
            btc = get_balance("BTC")
            if btc > 0.00008:
                upbit.sell_market_order("KRW-BTC", btc*0.9995)
        time.sleep(1)
        
    except Exception as e:
        print(e)
        time.sleep(1)


# In[ ]:




