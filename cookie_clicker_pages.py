from js import document
from pyodide import create_proxy

def decodef(*args, **kwargs):
    document.getElementById("decoded-save-code").value = "ayylmao"
