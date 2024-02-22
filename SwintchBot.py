'''
Copyright (c) 2024 S'(s1gnsgrfu)

This software is released under the Apache-2.0 license.
see https://github.com/s1gnsgrfu/SwintchBot/blob/master/LICENSE
'''

import flet as ft
import json
import time
import hashlib
import hmac
import base64
import uuid
import requests

# ! The token and secret are written in the key file.
# ! 1st line : token
# ! 2nd line : secret

# * URL
Domain_URL="https://api.switch-bot.com"
Device_List_URL=Domain_URL+"/v1.1/devices"

# * Variable
token=""
sign=""
t=""
nonce=""

# * HTTP Header
apiHeader = {}

def main():
    ft.app(target=FLET_Login)
    # Login_SwitchBot()
    # response=GET_Device_List()
    # for data in response:
    #    print(data)

def FLET_Login(page:ft.Page):
    page.title="Login"
    page.window_width=800
    page.window_height=500

    Logo=ft.Image(
        src=f"assets/Logo_long.png",
    )
    Text_token=ft.TextField(
            expand=False,
            label="token",
            hint_text="Enter token",
            focused_border_color="#4d82bc",
        )
    Text_secret=ft.TextField(
            expand=False,
            label="secret",
            hint_text="Enter secret",
            focused_border_color="#4d82bc",
        )
    Button_Login=ft.ElevatedButton(
                "Login",
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10),
                ),
                bgcolor="#4d82bc",
                color="#ffffff",
                width=200,
            )
    Space=ft.Column(
        height=50
    )
    Logo_View=ft.Column(
        width=300,
        controls=[
            Logo,
        ]
    )
    Text_View=ft.Column(
        width=400,
        controls=[
            Text_token,
            Text_secret,
        ],
    )

    page.horizontal_alignment=ft.CrossAxisAlignment.CENTER
    page.vertical_alignment=ft.MainAxisAlignment.CENTER
    page.bgcolor="#FFFFFF"

    page.add(Logo_View,Text_View,Button_Login,Space)
    page.update()


def GET_Request(url):
    response=requests.get(url,headers=apiHeader)
    res_data=response.json()
    if res_data['message']=='success':
        return response.json()
    else:
        return {}

def GET_Device_List():
    try:
        devices = GET_Request(Device_List_URL)["body"]
        return devices['deviceList']
    except:
        return

def Login_SwitchBot():
    # ! The amount of API calls per day is limited to 10000 times. Going over that limit will return "Unauthorized."

    # * keys -> [0]-token
    # *         [1]-secret
    keys=[]

    with open("key", "r") as f:
        keys = f.read().splitlines()

    # open token
    token = keys[0]
    # secret key
    secret = keys[1]
    nonce = uuid.uuid4()
    t = int(round(time.time() * 1000))
    string_to_sign = '{}{}{}'.format(token, t, nonce)

    string_to_sign = bytes(string_to_sign, 'utf-8')
    secret = bytes(secret, 'utf-8')

    sign = base64.b64encode(hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())
    print ('Authorization: {}'.format(token))
    print ('t: {}'.format(t))
    print ('sign: {}'.format(str(sign, 'utf-8')))
    print ('nonce: {}'.format(nonce))
    print()

    #Build api header JSON
    apiHeader['Authorization']=token
    apiHeader['Content-Type']='application/json'
    apiHeader['charset']='utf8'
    apiHeader['t']=str(t)
    apiHeader['sign']=str(sign, 'utf-8')
    apiHeader['nonce']=str(nonce)

if __name__ == "__main__":
    main()