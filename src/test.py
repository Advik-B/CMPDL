from cursepy import CurseClient
from v import api_key

c = CurseClient(api_key)
game = c.game(432) # Minecraft
addon = c.addon(400012) # Ex Nihilo: Sequentia

for file in addon.files():  # type: ignore
    print(file.download_url)

