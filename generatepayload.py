import os

import pandas as pd
from pymongo import MongoClient

mongousername = os.environ["MANGOU"]
mongopassword = os.environ["MANGOP"]


client = MongoClient(
    f"mongodb+srv://{mongousername}:{mongopassword}@blabla.qjokq.mongodb.net/?retryWrites=true&w=majority"
)

usersarr = [
    ["PATRICK", "U03RANJ8PDL"],
    ["CEASAR", "U0233NKSUE7"],
    ["KYLE", "U03RH8RBN75"],
    ["ISONE", "U03RKPM1U6Q"],
    ["MAK", "U049NEAJ7EW"],
    ["MARVIN", "U04HNAMTXBP"],
    ["TRIXIA", "U04JNNV7JTS"],
]


def payloadconstructor(invoiceid):
    def getsold():
        dbname = "mlb_sold_inventory"
        colname = "mlbsoldinventories"
        db = client[dbname]
        col = db[colname]
        soldmongoresults = col.find_one({})
        solddf = pd.DataFrame(soldmongoresults["data"])

        return solddf

    def getslackuserid(assigned):
        for user in usersarr:
            username = user[0]
            slackid = user[1]
            # print(type(assigned))
            # print(type(username))
            if str(assigned) == str(username):
                print("MATCH")
                touseslackid = slackid
                break
            else:
                touseslackid = "U03RPEH25L3"
        return touseslackid

    solddf = getsold()
    # print(solddf)
    invoicerow = solddf.loc[solddf["invoiceId"] == str(invoiceid)]
    print(invoicerow)
    assigned = invoicerow["ASSIGNED"].values.item()
    urgent = invoicerow["URGENT"].values.item()
    if urgent is True:
        urgentstr1 = ":alert:"
        urgentstr2 = "- URGENT:alert:"
    else:
        urgentstr1 = ""
        urgentstr2 = ""
    getslackuserid(assigned)

    payload = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{urgentstr1}PURCHASE REQUEST - {invoiceid} {urgentstr2}*",
                },
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*INVOICE ID:* \n {invoiceid}"},
                    {
                        "type": "mrkdwn",
                        "text": "*SEC:* \n {}".format(invoicerow["section"].values.item()),
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*ROW:* \n {}".format(invoicerow["row"].values.item()),
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*QTY:* \n {}".format(invoicerow["quantity"].values.item()),
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Event name:* \n {}".format(invoicerow["event_name"].values.item()),
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Event date:* \n {}".format(invoicerow["event_date"].values.item()),
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Total SOLD Cost:* \n {}".format(invoicerow["total"].values.item()),
                    },
                ],
            },
            {
                "type": "section",
                "fields": [
                    # {
                    # 	"type": "mrkdwn",
                    # 	"text": "*ASSIGNED TO:* \n <@%s>"%(slackid)
                    # },
                    {
                        "type": "mrkdwn",
                        "text": "*CUSTOMER:* \n {}".format(invoicerow["Customer"].values.item()),
                    },
                ],
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": "*PRIMARY LINK:*"},
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "PRIMARY LINK",
                        "emoji": True,
                    },
                    "value": "click_me_123",
                    "url": "{}".format(invoicerow["Primary_Link"].values.item()),
                    "action_id": "button-action",
                },
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": "*INVOICE LINK*"},
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "INVOICE LINK",
                        "emoji": True,
                    },
                    "value": "click_me_123",
                    "url": "{}".format(invoicerow["SBINVOICELINK"].values.item()),
                    "action_id": "button-action",
                },
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": "*SOLD INVENTORY LINK:*"},
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "SOLD INVENTORY LINK",
                        "emoji": True,
                    },
                    "value": "click_me_123",
                    "url": "{}".format(invoicerow["SBSOLDLINK"].values.item()),
                    "action_id": "button-action",
                },
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": "*INVENTORY LINK:*"},
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "INVENTORY LINK",
                        "emoji": True,
                    },
                    "value": "click_me_123",
                    "url": "{}".format(invoicerow["SBINVENTORYLINK"].values.item()),
                    "action_id": "button-action",
                },
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "emoji": True,
                            "text": "Purchased",
                        },
                        "style": "primary",
                        "value": f"Purchased - {invoiceid}",
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "emoji": True,
                            "text": "Reassign",
                        },
                        "style": "danger",
                        "value": f"Reassign - {invoiceid}",
                    },
                ],
            },
        ]
    }
    # print(payload)
    return payload


# invoiceid = '63452253'
# payloadconstructor(invoiceid)
