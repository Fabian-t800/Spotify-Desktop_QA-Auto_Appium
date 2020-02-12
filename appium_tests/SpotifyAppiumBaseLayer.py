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
    """
    :return: Connection to the Spotify Desktop App via WinAppDriver. WinAppDriver (essentially a listener) must be executed prior to test suite execution
    """
    desired_caps = {}
    desired_caps["app"] = "Spotify.exe"
    desired_caps["automationName"] = "winappdriver"
    driver = webdriver.Remote(
        command_executor='http://127.0.0.1:4723',
        desired_capabilities=desired_caps)
    driver.implicitly_wait(2)
    return driver


class SpotifyAppiumBaseLayer:

    def __init__(self):
        self.driver = connect_to_spotify_appium()

    def browse(self):
        """
        :return: Returns a Webelement containing the browse button.
        """
        return self.driver.find_element_by_name("Browse")

    def ret_driver(self):
        """
        :return: Returns the self.driver element. Is important especially for the use in the ActionChains class that allow you to chain together a series of actions.
        """
        return self.driver

    def _driver_wait(self, locator_of_element, locator_strategy=None):
        """
        An abstraction of the wait class, implemented as to create more readable code.
        Deprecated at this point (in this implementation)
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
        """
        :return: WebElement containing the search field.
        """
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@LocalizedControlType='search']")))
        # self._driver_wait("//*[@LocalizedControlType='search']", "xpath")
        return self.driver.find_element_by_xpath("//*[@LocalizedControlType='search']")

    def search_results_window(self):
        """
        :return: Doesn't return anything, just waits for the element to show up. Move it to helper class?
        """
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.driver.find_element_by_accessibility_id("view-content")))

    def search_result_first_row(self):
        """
        :return: First row of text of the search results
        """
        return self.driver.find_element_by_xpath("//*[@Name='Search' and @LocalizedControlType='document']/*")

    def search_results_second_row(self):
        """
        :return: Second row of text of the search results
        """
        return self.driver.find_element_by_xpath("//*[@Name='Search' and @LocalizedControlType='document']/*[2]")

    def search_results_third_row(self):
        """
        :return: Third row of text of the search results, if it exists.
        """
        try:
            if self.driver.find_element_by_xpath("//*[@Name='Search' and @LocalizedControlType='document']/*[3]").get_attribute('Name') == "Song":
                return self.driver.find_element_by_xpath("//*[@Name='Search' and @LocalizedControlType='document']/*[3]")
        except IndexError:
            pass

    def currently_playing_song_title(self):
        """
        Waits for the currently playing song title webelement to be visible.
        :return: Webelement. currently playing song title.
        """
        # self._driver_wait("nowplaying-track-link", "accessibility_id")
        WebDriverWait(self.driver, 10).until(EC.visibility_of(self.driver.find_element_by_accessibility_id("nowplaying-track-link")))
        return self.driver.find_element_by_accessibility_id("nowplaying-track-link")

    def friends_pane(self):
        """
        Waits for the friends pane webelement to  be visible.
        :return: Nothing.
        """
        WebDriverWait(self.driver, 10).until(EC.visibility_of(self.driver.find_element_by_accessibility_id("iframe-budy-list")))
        # self._driver_wait(self.driver.find_element_by_accessibility_id("iframe-budy-list"), "accessibility_id")

    def playlist(self, playlist_name):
        """
        Waits for the playlist to be present.
        :param playlist_name: Name of the playlist who's webelement will be returned.
        :return: The playlist webelement.
        """
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, f"//*[@LocalizedControlType='text' and @Name='{playlist_name}']")))
        return self.driver.find_element_by_xpath(f"//*[@LocalizedControlType='text' and @Name='{playlist_name}']")

    def songs_in_playlist(self):
        """
        :return: A list of webelements. The list is cleaned up of unnecessary elements.
        """
        elements = self.driver.find_elements_by_xpath("//*[@LocalizedControlType='table']")[2].find_elements_by_xpath("//*[@LocalizedControlType='text']")
        elements.pop(0)
        elements.pop(0)
        for el in elements:
            if el.text[0].isdigit() or el.text is None:
                elements.remove(el)
        return elements

    def read_songs_from_playlist(self):
        """
        :return: List of Webelements that contain the songs
        """
        try:
            return self.driver.find_elements_by_xpath("//*[@LocalizedControlType='table']")[2].find_elements_by_xpath(
                f"//*[@LocalizedControlType='text']")
        except IndexError:
            raise AssertionError(f"Error occured, the list was empty.")

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
        """
        :return: Webelement containing the player ui frame.
        """
        return self.driver.find_element_by_accessibility_id("view-player-footer")

    def now_playing_cluster(self):
        """
        :return: Webelement containing the now playing ui cluster.
        """
        return self.player_ui_frame().find_element_by_xpath("//*[@LocalizedControlType='content info']")

    def shuffle_button(self):
        """
        :return: Webelement Containing the shuffle button
        """
        return self.driver.find_element_by_accessibility_id("player-button-shuffle")

    def prev_button(self):
        """
        :return: Webelement containing the "previous" button.
        """
        return self.driver.find_element_by_accessibility_id("player-button-previous")

    def play_button_ui(self):
        """
        :return: Webelement containing the play button. Can
        """
        return self.driver.find_element_by_accessibility_id("player-button-play")

    def next_button(self):
        """
        :return: Webelement containing the "next" button.
        """
        return self.driver.find_element_by_accessibility_id("player-button-next")

    def repeat_button(self):
        """
        :return: Webelement containing the "repeat" button
        """
        return self.driver.find_element_by_accessibility_id("player-button-repeat")

    def control_bar(self):
        """
        :return: Webelement containing the the control bar.
        """
        return self.driver.find_element_by_xpath("//*[@Name='Player controls']").find_elements_by_xpath('//*')[3]

    def time_remaining(self):
        """
        :return: Webelement containing the time remaining.
        """
        return self.driver.find_element_by_xpath("//*[@Name='Player controls']").find_elements_by_xpath('//*')[4]

    def queue_button(self):
        """
        :return: Webelement containing the queue button
        """
        return self.driver.find_element_by_accessibility_id("player-button-queue")

    def connected_device(self):
        """
        :return: Webelement containing the connected devices button.
        """
        return self.driver.find_element_by_accessibility_id("player-button-devices")

    def mute_button(self):
        """
        :return: Webelement containing the mute button.
        """
        return self.driver.find_element_by_xpath("//*[@Name='Mute' and @LocalizedControlType='button']")

    def volume_bar(self):
        """
        :return: Webelement containing the volume bar
        """
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
        """
        :return: Webelement containing the home button
        """
        return self.driver.find_element_by_name("Home")

    def create_playlist_window(self):
        """
        :return: Identifies and returns the "Create new playlist window", after the create new playlist button has been pressed.
        """
        if self.driver.find_element_by_name("Create Playlist").get_property("IsEnabled") == True:
            print("CPW ok!")
            return self.driver.find_element_by_name("Create Playlist")

    def toggle_element(self, toggle_element_description):
        """
        :param toggle_element_description: Description of the toggle element that needs to be returned.
        :return: Webelement containing the toggle button.
        """
        return self.driver.find_elements_by_xpath(f"//*[@Name='{toggle_element_description}']")[1]

    def find_element(self, element):
        WebDriverWait(self.driver, 10).until(EC.visibility_of(self.driver.find_element_by_accessibility_id("player-button-shuffle")))
        return self.driver.find_element_by_accessibility_id("player-button-shuffle")

    def _wait_for_element(self, locator_strategy=None, locator_key=None, locator_value=None, locator_kv=None):
        """
        Custom wait method that uses polling.
        Currently unused and unstable
        :param locator_strategy:
        :param locator_key:
        :param locator_value:
        :param locator_kv:
        :return:
        """
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
    p = SpotifyAppiumBaseLayer()
    time.sleep(2)
    p.playlist("Super_jazz").click()
    q = p.read_songs_from_playlist()
    print(q)
    print(len(q))
    for element in q:
        print(element.text)


