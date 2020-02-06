from appium_tests.SpotifyAppiumBaseLayer import SpotifyAppiumBaseLayer
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from dateutil.parser import parse
import time
from robot.api import logger as robologger


class SpotifyAppiumHelperClass:

    def __init__(self):
        # SABL = Spotify Appium Base Layer
        self.SABL = SpotifyAppiumBaseLayer()

    def click_on_browse(self):
        self.SABL.browse().click()

    def max_win(self):
        self.SABL.home_button().click()
        actions = ActionChains(self.SABL.ret_driver())
        actions.send_keys(Keys.COMMAND + Keys.ARROW_UP + Keys.COMMAND)
        actions.perform()

    def click_on_search(self):
        self.SABL.search_field().click()

    def enter_search_keyword(self, keyword):
        self.SABL.search_field().send_keys(keyword)

    def read_top_result_artist(self):
        return self.SABL.top_search_result()

    def wait_for_search_results_window(self):
        self.SABL.search_field()

    def read_result_row_one(self):
        return self.SABL.search_result_first_row().get_attribute('Name')

    def read_results_row_two(self):
        return self.SABL.search_results_second_row().get_attribute('Name')

    def read_results_row_three(self):
        try:
            return self.SABL.search_results_third_row().get_attribute('Name')
        except AttributeError:
            return None

    def whats_playing_song_name(self):
        return self.SABL.currently_playing_song_title().get_attribute("Name")

    def click_play_button(self):
        self.SABL.play_button().click()

    def proper_search(self, keyword):
        self.click_on_search()
        self.enter_search_keyword(keyword)
        self.wait_for_search_results_window()
        # return self.read_result_row_one(), self.read_results_row_two(), self.read_results_row_three()
        self.check_search_functionality(keyword)

    def check_search_functionality(self, keyword):
        if self.read_result_row_one().lower() == keyword.lower():
            robologger.console(f"{keyword} is equal to {self.read_result_row_one()}")
        else:
            raise AssertionError(f"Expected would be that the search keyword {keyword} to be equal with the search results {self.read_result_row_one()}")

    def whats_playing_artist_name(self):
        actions = ActionChains(self.SABL.ret_driver())
        actions.move_to_element(self.SABL.currently_playing_artist_name())
        actions.perform()
        return self.SABL.currently_playing_artist_name()

    def click_on_playlist(self, playlist_name):
        self.SABL.playlist(playlist_name).click()

    def click_on_new_playlist_button(self):
        self.SABL.new_playlist_button().click()

    def send_keys_to_playlist_name_field(self, playlist_name):
        self.SABL.name_field_for_playlist().send_keys(playlist_name)

    def press_create_playlist(self):
        self.SABL.green_create_playlist_button().click()

    def press_home_button(self):
        self.SABL.home_button().click()

    def create_new_playlist_teardown(self, playlist_name):
        np = self.SABL.playlist(playlist_name)
        actions = ActionChains(self.SABL.ret_driver())
        actions.context_click(np)
        actions.perform()
        actions = ActionChains(self.SABL.ret_driver())
        actions.click(self.SABL.delete_button())
        actions.perform()
        actions = ActionChains(self.SABL.ret_driver())
        actions.click(self.SABL.red_delete_button())
        actions.perform()

    def new_playlist_creation_validation(self, playlist_name):
        try:
            if self.SABL.playlist(playlist_name) == playlist_name:
                robologger.console("The song was present in the playlist list. Test has passed.")
        except Exception:
            raise AssertionError(f"The newly created playlist called: {playlist_name} should have been present in the list. It was not.")

    def profile_menu_click(self):
        self.SABL.profile_menu().click()

    def menu_element_click(self, menu_element_name):
        self.SABL.menu_element(menu_element_name).click()

    def toggle_element_current_state(self, toggle_element_description):
        return self.SABL.toggle_element(toggle_element_description).get_attribute('Toggle.ToggleState')

    def toggle_element_click(self, toggle_element_description):
        self.SABL.toggle_element(toggle_element_description).click()

    def assert_toggle_state(self, initial_toggle_state, final_toggle_state):
        if initial_toggle_state != final_toggle_state:
            robologger.console(f"The test has passed. Initial state was {initial_toggle_state} and the final state was {final_toggle_state}")
        else:
            raise AssertionError(f"The toggle action did not have any effect. Initial state should have been different.\n"
                                 f"Initial state was: {initial_toggle_state} \n"
                                 f"Final state was: {final_toggle_state}.")

    def click_the_play_button(self):
        self.SABL.play_button().click()

    def wait_for_time(self, time_to_wait):
        time.sleep(int(time_to_wait))
        return True

    def time_elapsed_timer(self):
        return parse(self.SABL.time_elapsed_element().text).time()

    def assert_play_functionality(self, initial_time_elapsed, final_time_elapsed):
        if initial_time_elapsed < final_time_elapsed:
            robologger.console(f"Play functionality has worked. \n"
                               f"Initial time elapsed was: {initial_time_elapsed}\n"
                               f"Final time elapsed was: {final_time_elapsed}")
        else:
            raise AssertionError(f"The time elapsed after the play button was clicked should have been greater than the current time elapsed. \n "
                                 f"Time before: {initial_time_elapsed} \n"
                                 f"Time after: {final_time_elapsed}")

    def drag_and_drop_action(self, song_name, target_playlist):
        robologger.debug("Drag and drop method entered.")
        driver = self.SABL.ret_driver()
        robologger.debug(f"Driver is: {driver}")
        song = self.SABL.find_song_in_playlist(song_name)
        robologger.debug(f"Song's webelement is: {song}\n"
                        f"Song's name is: {song.text}")
        robologger.debug(f"Target playlist name is: {target_playlist}")
        tp = self.SABL.playlist(target_playlist)
        robologger.debug(f"Target playlist is: {tp}")
        actions = ActionChains(driver)
        actions.move_to_element(song)
        actions.click_and_hold(song)
        actions.move_by_offset(30, 50)
        actions.move_by_offset(10, 10)
        actions.move_to_element_with_offset(tp, 10, 10)
        actions.release()
        actions.perform()

    def assert_drag_and_drop_functionality(self, song_name):
        try:
            songs = self.SABL.songs_in_playlist()
            song_present = [song for song in songs if song.text == song_name]
            if len(song_present) == 0:
                raise AssertionError(f"Song named {song_name} should have been in the playlist, but it isn't.")
        except Exception as err:
            robologger.warn(f"An unexpected error has occurred: {err}.")

    def drag_and_drop_teardown(self, song_name):
        song = self.SABL.find_song_in_playlist(song_name)
        actions = ActionChains(self.SABL.ret_driver())
        actions.context_click(song)
        actions.perform()
        self.SABL.remove_song_from_playlist_button().click()

    def ui_test_bottom_console(self):
        pass

# if __name__ == '__main__':
#     SpotifyAppiumHelperClass().suite_setup()
#     # try:
#     #     close_spotify_app()
#     # except Exception as err:
#     #     robologger.debug(f"Spotify app was not opened. {err} has occured. Proceeding to open the Spotify App.")
#     #     pass
#     # SpotifyAppiumHelperClass().click_on_browse()
#     # SpotifyAppiumHelperClass().close_spotify()
#     # SpotifyAppiumHelperClass().click_on_search()
#     # print(SpotifyAppiumHelperClass().whats_playing_artist_name())
#     # print(SpotifyAppiumHelperClass().whats_playing_song_name())
#     # print(SpotifyAppiumHelperClass().proper_search("Sweet home alabama"))
