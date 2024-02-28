"""
Copyright (c) 2024 S'(s1gnsgrfu)

This software is released under the Apache-2.0 license.
see https://github.com/s1gnsgrfu/SwintchBot/blob/master/LICENSE
"""

import asyncio
import base64
import hashlib
import hmac
import json
import pathlib
import time
import uuid

import flet as ft
import requests


class Device:
    def __init__(self, device_id, device_name, device_type):
        self.device_id = device_id
        self.device_name = device_name
        self.device_type = device_type

    # device_list=ft.


# ! The token and secret are written in the key file.
# ! 1st line : token
# ! 2nd line : secret

# * URL
Domain_URL = "https://api.switch-bot.com"
Device_List_URL = Domain_URL + "/v1.1/devices"

# * Variable
token = ""
sign = ""
t = ""
nonce = ""

# * HTTP Header
apiHeader = {}


def main():
    ft.app(target=FLET_Login)
    # Login_SwitchBot()
    # response=GET_Device_List()
    # response=Login_SwitchBot()
    # for data in response:
    #    print(data)


def FLET_Login(page: ft.Page):
    page.title = "Login"
    page.window_width = 1000
    page.window_height = 600
    page.theme_mode = ft.ThemeMode.LIGHT

    def Route_Change(route):
        # page.views.clear()
        # page.views.append(LOGIN_View)

        # ---DEBUG---
        page.views.append(HOME_DEV)
        ChangePage(0)
        response = [
            {
                "deviceId": "FFFFFFFFFFFF",
                "deviceName": "プラグ1",
                "deviceType": "Plug",
                "enableCloudService": True,
                "hubDeviceId": "000000000000",
            },
            {
                "deviceId": "FFFFFFFFFFFF",
                "deviceName": "テープライト",
                "deviceType": "Strip Light",
                "enableCloudService": True,
                "hubDeviceId": "000000000000",
            },
            {
                "deviceId": "FFFFFFFFFFFF",
                "deviceName": "ハブミニ",
                "deviceType": "Hub Mini",
                "hubDeviceId": "000000000000",
            },
            {
                "deviceId": "FFFFFFFFFFFF",
                "deviceName": "温湿度計",
                "deviceType": "Meter",
                "enableCloudService": True,
                "hubDeviceId": "FFFFFFFFFFFF",
            },
            {
                "deviceId": "FFFFFFFFFFFF",
                "deviceName": "プラグ3",
                "deviceType": "Plug",
                "enableCloudService": True,
                "hubDeviceId": "000000000000",
            },
            {
                "deviceId": "FFFFFFFFFFFF",
                "deviceName": "プラグ2",
                "deviceType": "Plug",
                "enableCloudService": True,
                "hubDeviceId": "000000000000",
            },
            {
                "deviceId": "FFFFFFFFFFFF",
                "deviceName": "スイッチ",
                "deviceType": "Bot",
                "enableCloudService": True,
                "hubDeviceId": "FFFFFFFFFFFF",
            },
        ]
        for i in response:
            devices.append(Device(i["deviceId"], i["deviceName"], i["deviceType"]))
        Main_home_page.controls = device_con()
        page.update()
        # ---DEBUG---

        if page.route == "/main":
            ChangePage(0)

    # --LOGIN--
    LOGIN_Logo = ft.Image(
        src=f"assets/Logo_long.png",
    )

    LOGIN_Text_token = ft.TextField(
        expand=False,
        label="token",
        hint_text="Enter token",
        focused_border_color="#4d82bc",
        color="#000000",
    )

    LOGIN_Text_secret = ft.TextField(
        expand=False,
        label="secret",
        hint_text="Enter secret",
        focused_border_color="#4d82bc",
        color="#000000",
    )

    global devices
    devices = []

    def LOGIN_Click(e):
        response = Login_SwitchBot()
        if response == False:
            e.control.page.snack_bar = ft.SnackBar(
                ft.Text("Login Failed", color="#ffffff"), bgcolor="#ff4a4a"
            )
            e.control.page.snack_bar.open = True
            e.control.page.update()
        else:
            page.go("/main")
            for i in response:
                devices.append(Device(i["deviceId"], i["deviceName"], i["deviceType"]))
            Main_home_page.controls = device_con()
            page.update()

    def device_con():
        items = []
        print(devices)
        for data in devices:
            items.append(
                ft.Container(
                    content=ft.Text(
                        data.device_name,
                        color="#ffffff",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                    ),
                    margin=5,
                    padding=10,
                    width=140,
                    height=110,
                    border_radius=10,
                    ink=True,
                    bgcolor="#FF0000",
                    on_click=lambda e: print("clicked"),
                )
            )
        return items

    LOGIN_Button_Login = ft.ElevatedButton(
        "Login",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        bgcolor="#4d82bc",
        color="#ffffff",
        width=200,
        on_click=LOGIN_Click,
    )

    LOGIN_Space = ft.Column(height=50)

    LOGIN_Logo_Con = ft.Column(
        width=300,
        controls=[
            LOGIN_Logo,
        ],
    )

    LOGIN_Text_Con = ft.Column(
        width=400,
        controls=[
            LOGIN_Text_token,
            LOGIN_Text_secret,
        ],
    )

    LOGIN_View = ft.View(
        "/",
        [LOGIN_Logo_Con, LOGIN_Text_Con, LOGIN_Button_Login, LOGIN_Space],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
    )
    # --LOGIN--

    # --HOME--
    page_name = ["Home", "Scenes", "Settings"]

    Main_home_page = ft.Row(
        spacing=0,
        controls=device_con(),
        wrap=True,
    )

    Main_scenes_page = ft.Container(
        content=ft.Text("Clickable transparent with Ink"),
        margin=5,
        padding=10,
        alignment=ft.alignment.center,
        width=150,
        height=150,
        border_radius=10,
        ink=True,
        bgcolor="#00FF00",
        on_click=lambda e: print("Clickable transparent with Ink clicked!"),
    )

    Main_settings_page = ft.Container(
        content=ft.Text("Clickable transparent with Ink"),
        margin=10,
        padding=10,
        alignment=ft.alignment.center,
        width=150,
        height=150,
        border_radius=10,
        ink=True,
        bgcolor="#0000FF",
        on_click=lambda e: print("Clickable transparent with Ink clicked!"),
    )

    def ChangePage(index):
        page.views.clear()
        if index == 0:
            page.views.append(HOME_DEV)
        elif index == 1:
            page.views.append(SCENCES_DEV)
        elif index == 2:
            page.views.append(SETTINGS_DEV)
        page.update()

    def HOME_NavigationBar_Selected(index):
        print(f"Selected: {page_name[index]}")
        ChangePage(index)

    Navigation = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(
                icon=ft.icons.HOME_OUTLINED,
                selected_icon=ft.icons.HOME_FILLED,
                label=page_name[0],
            ),
            ft.NavigationDestination(
                icon=ft.icons.HOURGLASS_EMPTY_OUTLINED,
                selected_icon=ft.icons.HOURGLASS_FULL_OUTLINED,
                label=page_name[1],
            ),
            ft.NavigationDestination(
                icon=ft.icons.SETTINGS_OUTLINED,
                selected_icon=ft.icons.SETTINGS,
                label=page_name[2],
            ),
        ],
        height=50,
        surface_tint_color="#d9d9d9",
        indicator_color="#d9d9d9",
        on_change=lambda e: HOME_NavigationBar_Selected(e.control.selected_index),
    )

    HOME_DEV = ft.View(
        "/main",
        [Main_home_page, Navigation],
    )

    SCENCES_DEV = ft.View(
        "/main",
        [Main_scenes_page, Navigation],
    )

    SETTINGS_DEV = ft.View(
        "/main",
        [Main_settings_page, Navigation],
    )

    # --HOME--

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = Route_Change
    page.on_view_pop = view_pop
    page.go(page.route)


def GET_Request(url):
    response = requests.get(url, headers=apiHeader)
    res_data = response.json()
    if res_data["message"] == "success":
        return response.json()
    else:
        return {}


def GET_Device_List():
    try:
        devices = GET_Request(Device_List_URL)["body"]
        return devices["deviceList"]
    except:
        return False


def Login_SwitchBot():
    # ! The amount of API calls per day is limited to 10000 times. Going over that limit will return "Unauthorized."

    # * keys -> [0]-token
    # *         [1]-secret
    keys = []

    path = pathlib.Path("key")

    if not path.exists():
        path.touch()
    with path.open("r") as f:
        keys = f.read().splitlines()

    # open token
    # secret key
    if len(keys) < 2:
        token = ""
        secret = ""
    else:
        token = keys[0]
        secret = keys[1]

    nonce = uuid.uuid4()
    t = int(round(time.time() * 1000))
    string_to_sign = "{}{}{}".format(token, t, nonce)

    string_to_sign = bytes(string_to_sign, "utf-8")
    secret = bytes(secret, "utf-8")

    sign = base64.b64encode(
        hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest()
    )
    print("Authorization: {}".format(token))
    print("t: {}".format(t))
    print("sign: {}".format(str(sign, "utf-8")))
    print("nonce: {}".format(nonce))
    print()

    # Build api header JSON
    apiHeader["Authorization"] = token
    apiHeader["Content-Type"] = "application/json"
    apiHeader["charset"] = "utf8"
    apiHeader["t"] = str(t)
    apiHeader["sign"] = str(sign, "utf-8")
    apiHeader["nonce"] = str(nonce)

    return GET_Device_List()


if __name__ == "__main__":
    main()
