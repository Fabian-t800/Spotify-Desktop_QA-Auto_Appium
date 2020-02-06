import os
import psutil


class SetupAndTeardown:

    def suite_setup_appium_spotify(self):
        os.startfile('WinAppDriver.exe')

    def suite_teardown(self):
        try:
            for process in (process for process in psutil.process_iter() if process.name() == "Spotify.exe"):
                process.kill()
        except Exception:
            pass
        try:
            for process in (process for process in psutil.process_iter() if process.name() == "WinAppDriver.exe"):
                process.kill()
        except Exception:
            pass


if __name__ == "__main__":
    SetupAndTeardown().suite_setup_appium_spotify()
    # pass