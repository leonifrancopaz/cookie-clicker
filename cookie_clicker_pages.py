from js import document
import cookie_clicker

def du_trans_button(*args, **kwargs):
    save_code = document.getElementById("input").value
    save_code = cookie_clicker.decode(save_code)
    save_code = cookie_clicker.uncompress(save_code)
    document.getElementById("output").value = save_code

def ce_trans_button(*args, **kwargs):
    du_save_code = document.getElementById("input").value
    du_save_code = cookie_clicker.compress(du_save_code)
    du_save_code = cookie_clicker.encode(du_save_code)
    document.getElementById("output").value = du_save_code

def change_to_du(*args, **kwargs):
    document.getElementById("input-label").value = "Save code"
    document.getElementById("input").value = ""
    document.getElementById("transform-button").setAttribute("pys-onclick", "du_trans_button")

def change_to_ce(*args, **kwargs):
    document.getElementById("input-label").value = "Uncompressed and decoded save"
    document.getElementById("input").value = ""
    document.getElementById("transform-button").setAttribute("pys-onclick", "ce_trans_button")
