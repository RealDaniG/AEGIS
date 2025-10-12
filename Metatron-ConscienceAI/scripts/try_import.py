import importlib, traceback
try:
    m = importlib.import_module("scripts.web_chat_server")
    print("Imported:", m)
    print("App:", getattr(m, "app", None))
except Exception as e:
    print("Import failed:", e)
    traceback.print_exc()
