from cursepy import CurseClient
from v import api_key

c = CurseClient(api_key)

addon = c.addon(552574)
print(addon.name)