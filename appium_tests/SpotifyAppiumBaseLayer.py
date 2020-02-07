from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from robot.api import logger as robologger

def singleton(cls):
    instances = {}

    def _singleton():
      if cls not in instances:
          instances[cls] = cls()
      return instances[cls]
    return _singleton

@singleton
def connect_to_spotify_appium():
    desired_caps = {}
    desired_caps["app"] = "Spotify.exe"
    desired_caps["automationName"] = "winappdriver"
    driver = webdriver.Remote(
        command_executor='http://127.0.0.1:4723',
        desired_capabilities=desired_caps)
    driver.implicitly_wait(5)
    return driver


class SpotifyAppiumBaseLayer:

    def __init__(self):
        self.driver = connect_to_spotify_appium()

    def browse(self):
        return self.driver.find_element_by_name("Browse")

    def ret_driver(self):
        return self.driver

    def _driver_wait(self, locator_of_element, locator_strategy=None):
        """
        :param locator_strategy: Otherwise it will call for accessibility_id.
        :param locator_of_element: Locator of the element that needs to be found. Needs to be XPATH.
        :return: Webdriver element if it's been found, after it's been loaded.
        """
        try:
            if locator_strategy.lower() == "xpath":
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator_of_element)))
            elif locator_strategy.lower() == "accessibility_id" or locator_strategy.lower() == "automation_id":
                WebDriverWait(self.driver, 10).until(EC.visibility_of(self.driver.find_element_by_accessibility_id(locator_of_element)))
            elif locator_strategy.lower() == "name":
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(By.NAME, locator_of_element))
        finally:
            pass

    def search_field(self):
        self._driver_wait("//*[@LocalizedControlType='search']", "xpath")
        return self.driver.find_element_by_xpath("//*[@LocalizedControlType='search']")

    def search_results_window(self):
        self._driver_wait("view-content", "accessibility_id")

    def search_result_first_row(self):
        return self.driver.find_element_by_xpath("//*[@Name='Search' and @LocalizedControlType='document']/*")

    def search_results_second_row(self):
        return self.driver.find_element_by_xpath("//*[@Name='Search' and @LocalizedControlType='document']/*[2]")

    def search_results_third_row(self):
        try:
            if self.driver.find_element_by_xpath("//*[@Name='Search' and @LocalizedControlType='document']/*[3]").get_attribute('Name') == "Song":
                return self.driver.find_element_by_xpath("//*[@Name='Search' and @LocalizedControlType='document']/*[3]")
        except IndexError:
            pass

    def currently_playing_song_title(self):
        self._driver_wait("nowplaying-track-link", "accessibility_id")
        return self.driver.find_element_by_accessibility_id("nowplaying-track-link")

    def friends_pane(self):
        self._driver_wait(self.driver.find_element_by_accessibility_id("iframe-budy-list"), "accessibility_id")

    def playlist(self, playlist_name):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, f"//*[@LocalizedControlType='text' and @Name='{playlist_name}']")))
        return self.driver.find_element_by_xpath(f"//*[@LocalizedControlType='text' and @Name='{playlist_name}']")

    def songs_in_playlist(self):
        elements = self.driver.find_elements_by_xpath("//*[@LocalizedControlType='table']")[2].find_elements_by_xpath("//*[@LocalizedControlType='text']")
        elements.pop(0)
        elements.pop(0)
        for el in elements:
            if el.text[0].isdigit() or el.text is None:
                elements.remove(el)
        return elements

    def find_song_in_playlist(self, song_name):
        """
        :param song_name: Song name that needs to be searched for. Assumes you've already clicked the desired playlist
        :return: Song's webelement
        """
        try:
            return self.driver.find_elements_by_xpath("//*[@LocalizedControlType='table']")[2].find_elements_by_xpath(
                f"//*[@LocalizedControlType='text' and @Name='{song_name}']")[0]
        except IndexError:
            raise AssertionError(f"The song {song_name} was searched for but was not found.")

    def find_song(self, song_name):
        """
        :param song_name: WebElement of the song that needs to be interacted with.
        :return:
        """
        return self.driver.find_elements_by_xpath("//*[@LocalizedControlType='table']")[2].find_elements_by_xpath(f"//*[@LocalizedControlType='text' and @Name='{song_name}']")[0]

    def remove_song_from_playlist_button(self):
        """
        :return: WebElement. Remove song from playlist.
        """
        return self.driver.find_element_by_xpath("//*[@LocalizedControlType = 'text' and @Name='Remove from this Playlist']")

    def play_button(self):
        """
        :return: WebElement. Play button.
        """
        return self.driver.find_elements_by_xpath("//*[@Name='Player controls' and @LocalizedControlType='complementary']")[0]

    def player_ui_frame(self):
        return self.driver.find_element_by_accessibility_id("view-player-footer")

    def now_playing_cluster(self):
        return self.player_ui_frame().find_element_by_xpath("//*[@LocalizedControlType='content info']")

    def shuffle_button(self):
        return self.driver.find_element_by_accessibility_id("player-button-shuffle")

    def prev_button(self):
        return self.driver.find_element_by_accessibility_id("player-button-previous")

    def play_button_ui(self):
        return self.driver.find_element_by_accessibility_id("player-button-play")

    def next_button(self):
        return self.driver.find_element_by_accessibility_id("player-button-next")

    def repeat_button(self):
        return self.driver.find_element_by_accessibility_id("player-button-repeat")

    def control_bar(self):
        return self.driver.find_element_by_xpath("//*[@Name='Player controls']").find_elements_by_xpath('//*')[3]

    def time_remaining(self):
        return self.driver.find_element_by_xpath("//*[@Name='Player controls']").find_elements_by_xpath('//*')[4]

    def queue_button(self):
        return self.driver.find_element_by_accessibility_id("player-button-queue")

    def connected_device(self):
        return self.driver.find_element_by_accessibility_id("player-button-devices")

    def mute_button(self):
        return self.driver.find_element_by_xpath("//*[@Name='Mute' and @LocalizedControlType='button']")

    def volume_bar(self):
        return self.player_ui_frame().find_elements_by_xpath("//*")[9]

    def time_elapsed_element(self):
        """
        :return: Webelement. Time elapsed (Left side of the webplayer's UI).
        """
        return self.driver.find_elements_by_xpath("//*[@Name='Player controls' and @LocalizedControlType='complementary']")[0].find_elements_by_xpath("//*[@LocalizedControlType='text']")[0]

    def new_playlist_button(self):
        """
        :return: WebElement. Playlist button.
        """
        return self.driver.find_elements_by_name("Create New Playlist")[0]

    def green_create_playlist_button(self):
        """
        :return: Webelement. Green create playlist button.
        """
        return self.driver.find_element_by_name("Create")

    def name_field_for_playlist(self):
        """"
        :return: Webelement. Name field that needs to be sent keys for the name of the newly created playlist.
        """
        return self.driver.find_element_by_name("Name")

    def delete_button(self):
        """
        First Delete button encountered after context menu clicking
        :return: Webelement. Delete button.
        """
        return self.driver.find_element_by_name("Delete")

    def red_delete_button(self):
        """
        Last Delete button that needs to be clicked in order for the song playlist to be deleted
        :return: Red delete button of the element
        """
        return self.driver.find_element_by_name("DELETE")

    def profile_menu(self):
        """
        :return: Webelement of the profile menu.
        """
        return self.driver.find_element_by_accessibility_id("profile-menu-toggle")

    def menu_element(self, menu_element_name):
        """
        :param menu_element_name: Name of the element that would need to be clicked in order to enter the desired menu.
        :return:
        """
        return self.driver.find_element_by_name(menu_element_name)

    def toggle_element_name(self, toggle_name):
        """
        :param toggle_name: Name of the toggle element that needs to be clicked to change the toggle state.
        :return:
        """
        return self.driver.find_elements_by_xpath(f"//*[@Name='{toggle_name}']")[1]

    def home_button(self):
        return self.driver.find_element_by_name("Home")

    def create_playlist_window(self):
        if self.driver.find_element_by_name("Create Playlist").get_property("IsEnabled") == True:
            print("CPW ok!")
            return self.driver.find_element_by_name("Create Playlist")

    # def drag_and_drop(self, source_playlist, song_name, target_playlist):
    #     # --- 0: Element identification ----
    #     tp = self.playlist(target_playlist)
    #     sp = self.playlist(source_playlist)
    #     sp.click()
    #     song = self.driver.find_elements_by_xpath("//*[@LocalizedControlType='table']")[2].find_elements_by_xpath(f"//*[@LocalizedControlType='text' and @Name='{song_name}']")[0]
    #     # --- 0: Element identification ----
    #     time.sleep(3)
    #     # --- 1: Drag and drop implementation ----
    #     actions = ActionChains(self.driver)
    #     actions.click_and_hold(song)
    #     actions.move_by_offset(30, 50)
    #     actions.move_by_offset(10, 10)
    #     actions.move_to_element_with_offset(tp, 10, 10)
    #     actions.release()
    #     actions.perform()
    #     # --- 1: Drag and drop implementation ----
    #     # --- 2: Assertion ----
    #     tp.click()
    #     try:
    #         songs = self.songs_in_playlist()
    #         song_present = [song for song in songs if song.text == song_name]
    #         if len(song_present) == 0:
    #             raise AssertionError(f"Song named {song_name} should have been in the playlist, but it isn't.")
    #     except Exception as err:
    #         print(err)
    #     # --- 2: Assertion ----
    #     # --- 3: Breakdown ----
    #     song = self.driver.find_elements_by_xpath("//*[@LocalizedControlType='table']")[2].find_elements_by_xpath(
    #         f"//*[@LocalizedControlType='text' and @Name='{song_name}']")[0]
    #     actions.context_click(song)
    #     actions.perform()
    #     remove_button = self.driver.find_element_by_xpath("//*[@LocalizedControlType = 'text' and @Name='Remove from this Playlist']")
    #     remove_button.click()
    #     # --- 3: Breakdown ----

    # def play_song_functionality(self):
    #     time.sleep(3)
    #     # --- 0: Element Identification ----
    #     play_button = self.driver.find_elements_by_xpath("//*[@Name='Player controls' and @LocalizedControlType='complementary']")[0]
    #     time_elapsed_element = play_button.find_elements_by_xpath("//*[@LocalizedControlType='text']")[0]
    #     # --- 0: Element Identification ----
    #     # --- 1: Initial steps for validation ----
    #     time_elapsed_before = parse(time_elapsed_element.text).time()
    #     play_button.click()
    #     time.sleep(3)
    #     play_button.click()
    #     # --- 1: Initial steps for validation ----
    #     # --- 2: Validation ----
    #     if time_elapsed_before < parse(time_elapsed_element.text).time():
    #         return True
    #     else:
    #         raise AssertionError(f"The time elapsed after the play button was clicked should have been greater than the current time elapsed. \n "
    #                              f"Time before: {time_elapsed_before} \n"
    #                              f"Time after: {parse(time_elapsed_element.text).time}")
    #     # --- 2: Validation ----

    # def create_new_playlist(self, playlist_name):
    #     # --- 0: Identify elements ----
    #     new_playlist_button = self.driver.find_element_by_name("Create New Playlist")
    #     time.sleep(2)
    #     new_playlist_button.click()
    #     green_create_button = self.driver.find_element_by_name("Create")
    #     name_field_for_playlist = self.driver.find_element_by_name("Name")
    #     # --- 0: Identify elements ----
    #     # --- 1: Playlist creation actions ----
    #     name_field_for_playlist.send_keys(playlist_name)
    #     green_create_button.click()
    #     # --- 1: Playlist creation actions ----
    #     # --- 2: Validation ----
    #     try:
    #         if self.playlist(playlist_name).text == playlist_name:
    #             pass
    #     except Exception:
    #         raise AssertionError(f"The playlist with the name {playlist_name} should have been present. It is currently not found.")
    #     # --- 2: Validation ----
    #     # --- 3: Teardrown ----
    #     time.sleep(2)
    #     np = self.playlist(playlist_name)
    #     actions = ActionChains(self.driver)
    #     actions.context_click(np)
    #     actions.perform()
    #     delete_button = self.driver.find_element_by_name("Delete")
    #     actions = ActionChains(self.driver)
    #     actions.click(delete_button)
    #     actions.perform()
    #     red_delete_button = self.driver.find_element_by_name("DELETE")
    #     actions = ActionChains(self.driver)
    #     actions.click(red_delete_button)
    #     actions.perform()
    #     # --- 3: Teardrown ----
    #
    # def test_toggle_functionality(self):
    #     # --- 0: Identify elements ----
    #     arrow_down_menu = self.driver.find_element_by_accessibility_id("profile-menu-toggle")
    #     time.sleep(2)
    #     # --- 0: Identify elements ----
    #     # --- 1: Accessing the settings menu ---
    #     actions = ActionChains(self.driver)
    #     actions.click(arrow_down_menu)
    #     actions.perform()
    #     settings_button = self.driver.find_element_by_name("Settings")
    #     actions = ActionChains(self.driver)
    #     actions.pause(1)
    #     actions.click(settings_button)
    #     actions.perform()
    #     # --- 1: Accessing the settings menu ---
    #     # --- 2: Toggle interaction ---
    #     try:
    #         explicit_content = self.driver.find_elements_by_xpath("//*[@Name='Allow playback of explicit-rated content.']")[1]
    #         music_quality = self.driver.find_elements_by_xpath("//*[@Name ='Normalize volume - Set the same volume level for all songs']")[1]
    #         # print(f"Before: {explicit_content.get_attribute('Toggle.ToggleState')}")
    #         # print(f"Before: {music_quality.get_attribute('Toggle.ToggleState')}")
    #         explicit_content_toggle_state_before = explicit_content.get_attribute('Toggle.ToggleState')
    #         music_quality_toggle_state_before = music_quality.get_attribute('Toggle.ToggleState')
    #         actions = ActionChains(self.driver)
    #         actions.click(explicit_content)
    #         actions.click(music_quality)
    #         actions.perform()
    #         # print(f"After: {explicit_content.get_attribute('Toggle.ToggleState')}")
    #         # print(f"After: {music_quality.get_attribute('Toggle.ToggleState')}")
    #     except Exception as err:
    #         print(err)
    #     # --- 2: Toggle interaction ---
    #     # --- 3: Validation ---
    #     if explicit_content_toggle_state_before != explicit_content.get_attribute('Toggle.ToggleState'):
    #         return True
    #     else:
    #         raise AssertionError(f"The toggle action did not have any effect.")
    #     # --- 3: Validation ---

    def toggle_element(self, toggle_element_description):
        return self.driver.find_elements_by_xpath(f"//*[@Name='{toggle_element_description}']")[1]

    def play_button(self):
        return self.driver.find_elements_by_xpath("//*[@Name='Player controls' and @LocalizedControlType='complementary']")[0]

    def find_element(self, element):
        # self.driver.find_element_by_accessibility_id("player-button-shuffle")
        self._wait_for_element("accessibility_id", locator_value="player-button-shuffle")

    def _wait_for_element(self, locator_strategy=None, locator_key=None, locator_value=None, locator_kv=None):
        number_of_attempts = 0
        while number_of_attempts < 3:
            try:
                if locator_strategy.lower() == "xpath":
                    element = self.driver.find_element_by_xpath(f"//*[@{locator_key}='{locator_value}']")
                    return element
                elif locator_strategy.lower() == "accessibility_id":
                    element = self.driver.find_element_by_accessibility_id(f"{locator_value}")
                    return element
                elif locator_strategy.lower() == "name":
                    element = self.driver.find_element_by_name(f"{locator_value}")
                    return element
            except Exception:
                robologger.debug(f"Tried to locate element. Attempt number {number_of_attempts}")
                time.sleep(0.5)
                number_of_attempts += 1
                continue
            finally:
                if number_of_attempts == 3:
                    robologger.warn("3 attempts were made but element couldn't be located.")

if __name__ == '__main__':
    # playlist = SpotifyAppiumBaseLayer().playlist('extra_heavy_metal')
    # playlist.click()
    # song = SpotifyAppiumBaseLayer().find_song('Strangler')
    # actions = ActionChains(SpotifyAppiumBaseLayer().ret_driver())
    # actions.move_to_element(song)
    # actions.perform()
    p = SpotifyAppiumBaseLayer()
    p.find_element(SpotifyAppiumBaseLayer().driver.find_element_by_xpath("//*[@Name='Mute' and @LocalizedControlType='button']"))


