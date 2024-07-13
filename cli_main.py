import sys
import ui_api
import ui_timer

if len(sys.argv) > 1:
    if sys.argv[1].endswith(".spdtarg"):
        ui_timer.TimerUI(sys.argv[1])
    else:
        ui_api.PasswordApp()
else:
    ui_api.PasswordApp()