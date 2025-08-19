from gui.halcyon_gui import HalcyonGUI

hud = HalcyonGUI()
hud.show()

# Connect these:
thalamus.gui.on("state", hud.push_state)
thalamus.gui.on("final", hud.push_final)
thalamus.gui.on("token", hud.push_token)
thalamus.gui.on("log",   hud.push_log)
