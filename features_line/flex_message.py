from linebot.models import (FlexSendMessage)



def flex_iot():
    flex_msg = FlexSendMessage(
        alt_text='Control IoT',
        contents={
                "type": "carousel",
                "contents": [
                    {
                        "type": "bubble",
                        "hero": {
                            "type": "image",
                            "size": "full",
                            "aspectRatio": "20:13",
                            "aspectMode": "cover",
                            "url": "https://sv1.picz.in.th/images/2021/05/27/PAUHsf.jpg"
                        },
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "ควบคุมไฟ",
                                    "wrap": True,
                                    "weight": "bold",
                                    "size": "xl"
                                },
                                {
                                    "type": "box",
                                    "layout": "baseline",
                                    "contents": []
                                }
                            ]
                        },
                        "footer": {
                            "type": "box",
                            "layout": "vertical",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "button",
                                    "style": "primary",
                                    "action": {
                                        "type": "postback",
                                        "label": "เปิดไฟ 1",
                                        "data": "3"
                                    }
                                },
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "postback",
                                        "label": "ปิดไฟ 1",
                                        "data": "4"
                                    },
                                    "style": "primary"
                                },
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "postback",
                                        "label": "เปิดไฟ 2",
                                        "data": "5"
                                    },
                                    "style": "primary"
                                },
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "postback",
                                        "label": "ปิดไฟ 2",
                                        "data": "6"
                                    },
                                    "style": "primary"
                                }
                            ]
                        }
                    },
                    {
                        "type": "bubble",
                        "hero": {
                            "type": "image",
                            "size": "full",
                            "aspectRatio": "20:13",
                            "aspectMode": "cover",
                            "url": "https://sv1.picz.in.th/images/2021/05/27/PAUHsf.jpg"
                        },
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "ควบคุมน้ำ/ละอองน้ำ",
                                    "wrap": True,
                                    "weight": "bold",
                                    "size": "xl"
                                },
                                {
                                    "type": "box",
                                    "layout": "baseline",
                                    "flex": 1,
                                    "contents": []
                                }
                            ]
                        },
                        "footer": {
                            "type": "box",
                            "layout": "vertical",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "button",
                                    "flex": 2,
                                    "style": "primary",
                                    "action": {
                                        "type": "postback",
                                        "label": "เปิดน้ำ",
                                        "data": "10"
                                    }
                                },
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "postback",
                                        "label": "ปิดน้ำ",
                                        "data": "9"
                                    },
                                    "style": "primary"
                                },
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "postback",
                                        "label": "เปิดละอองน้ำ",
                                        "data": "8"
                                    },
                                    "style": "primary"
                                },
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "postback",
                                        "label": "ปิดละอองน้ำ",
                                        "data": "7"
                                    },
                                    "style": "primary"
                                }
                            ]
                        }
                    }
                ]
            }
    )
    return flex_msg