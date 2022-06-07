from js import document
from pyodide import create_proxy
import cookie_clicker

def decodef(*args, **kwargs):
    save_code = document.getElementById("save-code").value
    save_code = cookie_clicker.decode(save_code)
    save_code = cookie_clicker.uncompress(save_code)
    document.getElementById("decoded-save-code").value = save_code
