
import e2b
print(f"E2B Version: {e2b.__version__}")
from e2b import Sandbox
print("Sandbox attributes:")
print([a for a in dir(Sandbox) if "mcp" in a.lower()])
try:
    sb = Sandbox.create(api_key="test") # This might fail auth but we just want to see instance attributes if possible, or class attributes
except:
    pass

