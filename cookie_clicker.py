# -*- coding: UTF-8 -*-
import base64
import json
import re
import urllib.request


def decode(save_code):
    """
    Return a string containing compressed save data from a Cookie Clicker save
    code decoded from Base64 format.
    """
    # Changing some parts of the string for proper decoding.
    s = save_code.replace("%21END%21", "").replace("%3D", "=")

    # Decoding from Base64 format.
    s = s.encode()
    s = base64.b64decode(s)
    compressed_save_data = s.decode()

    return compressed_save_data


def encode(compressed_save_data):
    """
    Return a string containing a Cookie Clicker save code from compressed save
    data encoded to Base64 format.
    """
    # Encoding to Base64 format.
    s = compressed_save_data.encode()
    s = base64.b64encode(s)
    s = s.decode()

    # Changing some parts of the string for proper encoding.
    save_code = s.replace("=", "%3D") + "%21END%21"

    return save_code


def uncompress(compressed_save_data):
    """
    Return a string containing a JSON string representation of a Cookie
    Clicker's decoded (from Base64 format) and compressed save data paired
    with its appropriate metadata.
    """
    metadata = json.load(open("metadata.json", "rt"))
    # Splitting and pairing ###################################################
    data = compressed_save_data.split("|")
    save = {}
    save["Version"] = data[0]
    save["Save stats"] = dict(zip(metadata["Save stats"], data[2].split(";")))
    save["Settings"] = dict(zip(metadata["Settings"], data[3]))
    save["Stats"] = dict(zip(metadata["Stats"], data[4].split(";")))

    data[5] = data[5].split(";")
    data[5] = [i.split(",") for i in data[5][:-1]]
    save["Buildings"] = {}
    for building, building_dataset in zip(metadata["Buildings"], data[5]):
        save["Buildings"][building] = dict(
            zip(metadata["Buildings data"], building_dataset)
            )

    upgrades = ""
    for i, j in enumerate(data[6], 1):
        if i % 2 == 0:
            upgrades += f"{j} "
            continue

        upgrades += j
    else:
        data[6] = upgrades.split(" ")[:-1]

    save["Upgrades"] = dict(zip(metadata["Upgrades"], data[6]))
    save["Achievements"] = dict(zip(metadata["Achievements"], data[7]))
    save["Buffs"] = data[8][:-1].split(";") if data[8] else []
    save["Mod data"] = data[9][:-1].split(";") if data[9] else []

    # Doing some miscellaneous changes and typecasting ########################
    for k, vt in zip(save["Save stats"], metadata["Save stats types"]):
        save["Save stats"][k] = eval(vt)(save["Save stats"][k])

    for s, svt in zip(save["Stats"], metadata["Stats types"]):
        save["Stats"][s] = eval(svt)(save["Stats"][s])

    for b, bd in save["Buildings"].items():
        for d, bdvt in zip(bd, metadata["Buildings data types"]):
            save["Buildings"][b][d] = eval(bdvt)(save["Buildings"][b][d])

    for setting, value in save["Settings"].items():
        save["Settings"][setting] = "OFF" if value == "0" else "ON"

    d = {"0": False, "1": True}
    for upgrade in save["Upgrades"]:
        save["Upgrades"][upgrade] = {
            "Unlocked": d[save["Upgrades"][upgrade][0]],
            "Purchased":d[save["Upgrades"][upgrade][1]]
            }

    for achievement in save["Achievements"]:
        save["Achievements"][achievement] = {
            "Unlocked": d[save["Achievements"][achievement]]
            }

    # Output ##################################################################
    s = json.dumps(save, indent=4)
    s = "\n".join([re.sub("\.0,$", ",", line) for line in s.split("\n")])

    return s
    

def compress(save_code):
    """Rearrange a Base64 decoded save to its original format."""
    save = json.loads(save_code)

    # Translating and converting values #######################################
    for section in ("Save stats", "Stats", "Buildings"):
        if section == "Buildings":
            for building in save[section]:
                for key, value in save[section][building].items():
                    save[section][building][key] = str(value)
            else:
                continue

        for key, value in save[section].items():
            save[section][key] = str(value)

    for setting, value in save["Settings"].items():
        save["Settings"][setting] = "0" if value == "OFF" else "1"

    d = {False: "0", True: "1"}
    for i, j in save["Upgrades"].items():
        save["Upgrades"][i] = d[j["Unlocked"]] + d[j["Purchased"]]

    for i, j in save["Achievements"].items():
        save["Achievements"][i] = d[j["Unlocked"]]

    # Putting things together #################################################
    for building in save["Buildings"] :
        building_values = save["Buildings"][building].values()
        save["Buildings"][building] = ",".join(building_values)

    save["Version"] = save["Version"] + "||"
    save["Save stats"] = ";".join(save["Save stats"].values()) + "|"
    save["Settings"] = "".join(save["Settings"].values()) + "|"
    save["Stats"] = ";".join(save["Stats"].values()) + ";|"
    save["Buildings"] = ";".join(save["Buildings"].values()) + ";|"
    save["Upgrades"] = "".join(save["Upgrades"].values()) + "|"
    save["Achievements"] = "".join(save["Achievements"].values()) + "|"
    save["Buffs"] = ";".join(save["Buffs"])
    save["Mod data"] = ";".join(save["Mod data"]) if save["Mod data"] else ""

    save["Buffs"] += ";|" if save["Buffs"] else "|"
    save["Mod data"] += ";" if save["Mod data"] else ""

    save_code = "".join(save.values())

    # Output ##################################################################
    return save_code
