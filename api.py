'''
 Main Run File, It Executes the server

$$$$$$$$\ $$\       $$$$$$\   $$$$$$\
$$  _____|$$ |     $$  __$$\ $$  __$$\
$$ |      $$ |     $$ /  \__|$$ /  $$ |
$$$$$\    $$ |     \$$$$$$\  $$$$$$$$ |
$$  __|   $$ |      \____$$\ $$  __$$ |
$$ |      $$ |     $$\   $$ |$$ |  $$ |
$$$$$$$$\ $$$$$$$$\\$$$$$$  |$$ |  $$ |
\________|\________|\______/ \__|  \__|




'''


import sys
import os

os.environ["GIT_PYTHON_REFRESH"] = "quiet"

sys.path.append("./objects")
sys.path.append("./helpers")
sys.path.append("./config")

print("Starting!!!!!!")

from Server import Server


s = Server()
s.start()

print("Done!")
