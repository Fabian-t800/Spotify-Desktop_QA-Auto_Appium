from appium_tests.SpotifyAppiumBaseLayer import SpotifyAppiumBaseLayer
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from dateutil.parser import parse
import time
from robot.api import logger as robologger
from selenium.webdriver.common.touch_actions import TouchActions


class SpotifyAppiumHelperClass:

    def __init__(self):
        # SABL = Spotify Appium Base Layer
        self.SABL = SpotifyAppiumBaseLayer()

    def click_on_browse(self):
        self.SABL.browse().click()

    def max_win(self):
        """
        Maximizes the window using windows key presses.
        :return:
        """
        self.SABL.home_button().click()
        actions = ActionChains(self.SABL.ret_driver())
        actions.send_keys(Keys.COMMAND + Keys.ARROW_UP + Keys.COMMAND)
        actions.perform()

    def click_on_search(self):
        """
        Clicks on the search field.
        :return:
        """
        self.SABL.search_field().click()

    def enter_search_keyword(self, keyword):
        """
        :param keyword: A string containing the search term to be entered into the search field
        """
        self.SABL.search_field().send_keys(keyword)

    def read_top_result_artist(self):
        """
        :return: Top search result, artist.
        """
        return self.SABL.top_search_result()

    def wait_for_search_results_window(self):
        """
        :return: Waits for search result window.
        """
        self.SABL.search_field()

    def read_result_row_one(self):
        """
        :return: Returns a string containing the name of the search result.
        """
        return self.SABL.search_result_first_row().get_attribute('Name')

    def read_results_row_two(self):
        """
        :return: Returns a string for the second search result row (can be album or song name)
        """
        return self.SABL.search_results_second_row().get_attribute('Name')

    def read_results_row_three(self):
        """
        :return: A string containing the results of the 3rd result row, if it exists.
        """
        try:
            return self.SABL.search_results_third_row().get_attribute('Name')
        except AttributeError:
            return None

    def whats_playing_song_name(self):
        """
        :return: String containing the value of the what's playing cluster.
        """
        return self.SABL.currently_playing_song_title().get_attribute("Name")

    def click_play_button(self):
        """
        Clicks on the play button
        """
        self.SABL.play_button().click()

    # def proper_search(self, keyword):
    #     """
    #     :param keyword: Search using a
    #     :return:
    #     """
    #     self.click_on_search()
    #     self.enter_search_keyword(keyword)
    #     self.wait_for_search_results_window()
    #     # return self.read_result_row_one(), self.read_results_row_two(), self.read_results_row_three()
    #     self.check_search_functionality(keyword)

    def check_search_functionality(self, keyword):
        """
        Asserts if the search functionality works. If it doesn't work it raises an AssertionError.
        :param keyword: Keyword to be searched for
        """
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
        """
        :param playlist_name: Name of the playlist that needs to be clicked.
        :return:
        """
        self.SABL.playlist(playlist_name).click()

    def click_on_new_playlist_button(self):
        """
        Clicks on the new playlist button.
        """
        self.SABL.new_playlist_button().click()

    def send_keys_to_playlist_name_field(self, playlist_name):
        """
        Sends a string via the .send_keys() method to the new playlist name field.
        :param playlist_name: Name of the new playlist that needs to be entered
        """
        self.SABL.name_field_for_playlist().send_keys(playlist_name)

    def press_create_playlist(self):
        """
        Clicks the create new playlist button (Create new playlist green button from within the new new playlist creation window)
        """
        self.SABL.green_create_playlist_button().click()

    def press_home_button(self):
        """
        Clicks home button from the UI.
        """
        self.SABL.home_button().click()

    def create_new_playlist_teardown(self, playlist_name):
        """
        Deletes the newly created playlist thus getting back to the original state.
        :param playlist_name: Name of the playlist that was used in the creation of the new playlist
        """
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
        """
        Validates that the new playlist was indeed created
        :param playlist_name: String containing the name of the newly created playlist
        """
        try:
            if self.SABL.playlist(playlist_name) == playlist_name:
                robologger.console("The song was present in the playlist list. Test has passed.")
        except Exception:
            raise AssertionError(f"The newly created playlist called: {playlist_name} should have been present in the list. It was not.")

    def profile_menu_click(self):
        """
        :return: Clicks on the profile menu (the menu that let's you enter the settings menu, account menu etc)
        """
        self.SABL.profile_menu().click()

    def menu_element_click(self, menu_element_name):
        """
        Clicks the menu element with the specified name (menu_element_name)
        :param menu_element_name: Name of the element that will be clicked
        """
        self.SABL.menu_element(menu_element_name).click()

    def toggle_element_current_state(self, toggle_element_description):
        """
        :param toggle_element_description: Full description of the toggle element
        :return: Returns a string containing the current toggle state
        """
        return self.SABL.toggle_element(toggle_element_description).get_attribute('Toggle.ToggleState')

    def toggle_element_click(self, toggle_element_description):
        """
        Clicks on the toggle element
        :param toggle_element_description: Full description of the toggle element
        """
        self.SABL.toggle_element(toggle_element_description).click()

    def assert_toggle_state(self, initial_toggle_state, final_toggle_state):
        """
        Asserts if the toggle states are different after being clicked.
        If this fails (both toggle states are the same) then an assertion error is raised.
        :param initial_toggle_state: Toggle state before the click
        :param final_toggle_state: Toggle state after the click
        """
        if initial_toggle_state != final_toggle_state:
            robologger.console(f"The test has passed. Initial state was {initial_toggle_state} and the final state was {final_toggle_state}")
        else:
            raise AssertionError(f"The toggle action did not have any effect. Initial state should have been different.\n"
                                 f"Initial state was: {initial_toggle_state} \n"
                                 f"Final state was: {final_toggle_state}.")

    def click_the_play_button(self):
        """
        Clicks on the play button
        """
        self.SABL.play_button().click()

    def wait_for_time(self, time_to_wait):
        """
        :param time_to_wait: Number of seconds the execution of the test case is paused.
        """
        time.sleep(int(time_to_wait))

    def time_elapsed_timer(self):
        """
        :return: Returns a parsed timer. Used to compare before and after times.
        """
        return parse(self.SABL.time_elapsed_element().text).time()

    def assert_play_functionality(self, initial_time_elapsed, final_time_elapsed):
        """
        Asserts if the play functionality works by comparing the time before and after the play button was pressed.
        :param initial_time_elapsed: First reading of the time elapsed
        :param final_time_elapsed: Final reading of the time elapsed
        """
        if initial_time_elapsed < final_time_elapsed:
            robologger.console(f"Play functionality has worked. \n"
                               f"Initial time elapsed was: {initial_time_elapsed}\n"
                               f"Final time elapsed was: {final_time_elapsed}")
        else:
            raise AssertionError(f"The time elapsed after the play button was clicked should have been greater than the current time elapsed. \n "
                                 f"Time before: {initial_time_elapsed} \n"
                                 f"Time after: {final_time_elapsed}")

    def drag_and_drop_action(self, song_name, target_playlist):
        """
        Performs the drag and drop action
        :param song_name: Name of the song that needs to be dragged and dropped to another playlist
        :param target_playlist: The playlist where the selected song needs to be dropped
        """
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
        """
        Asserts if the drag and drop action was successfully completed. Raises an assertion error if it isn't.
        :param song_name: Name of the song that would need to present in the target playlist

        """
        try:
            songs = self.SABL.songs_in_playlist()
            song_present = [song for song in songs if song.text == song_name]
            if len(song_present) == 0:
                raise AssertionError(f"Song named {song_name} should have been in the playlist, but it isn't.")
        except Exception as err:
            robologger.warn(f"An unexpected error has occurred: {err}.")

    def drag_and_drop_teardown(self, song_name):
        """
        Deletes the song that was dragged and dropped, so as to go back to the intial testing state.
        :param song_name: Name of the song that was dragged from one playlist to another
        """
        song = self.SABL.find_song_in_playlist(song_name)
        actions = ActionChains(self.SABL.ret_driver())
        actions.context_click(song)
        actions.perform()
        self.SABL.remove_song_from_playlist_button().click()

    def ui_test_bottom_console(self):
        """
        Checks for if all the elemets are present in the lower UI console.
        """
        try:
            self.SABL.player_ui_frame()
            self.SABL.now_playing_cluster()
            self.SABL.shuffle_button()
            self.SABL.prev_button()
            self.SABL.play_button_ui()
            self.SABL.next_button()
            self.SABL.repeat_button()
            self.SABL.control_bar()
            self.SABL.time_elapsed_element()
            self.SABL.time_remaining()
            self.SABL.queue_button()
            self.SABL.connected_device()
            self.SABL.mute_button()
            self.SABL.volume_bar()
        except Exception as err:
            robologger.warn(f"An element was not detected and this is the error: {err}")
            raise AssertionError("Not all bottom ui elements were present.")
            pass

    def move_mouse_to_volume_bar(self):
        """
        Moves the mouse over to the volume bar.
        """
        actions = ActionChains(self.SABL.ret_driver())
        actions.move_to_element_with_offset(self.SABL.mute_button(), 60, 20)
        actions.pause(5)
        actions.perform()

    def scrolling_actions(self):
        """
        An implementation on the scroll action using WinAppDriver, however currently winappdriver doesn't seem to support mouse scrolling.
        Not used because of the afor mentioned reasons.
        :return:
        """
        tactions = TouchActions(self.SABL.ret_driver())
        tactions.scroll(10, 10)
        tactions.perform()

    def read_songs_from_target_playlist(self):
        """
        Reads the songs from a playlist.
        If the list of songs is empty then an assertion error is raised.
        :return:
        """
        if len(self.SABL.songs_in_playlist()) > 0:
            robologger.console(self.SABL.read_songs_from_playlist())
        else:
            raise AssertionError("the playlist should have contained songs, instead it did not.")



    # def ui_test_bottom_console(self):
    #     elements = []
    #     try:
    #         # elements.append(self.SABL.player_ui_frame())
    #         # elements.append(self.SABL.now_playing_cluster())
    #         # elements.append(self.SABL.shuffle_button())
    #         # elements.append(self.SABL.prev_button())
    #         # elements.append(self.SABL.play_button_ui())
    #         # elements.append(self.SABL.next_button())
    #         # elements.append(self.SABL.repeat_button())
    #         # elements.append(self.SABL.control_bar())
    #         # elements.append(self.SABL.time_elapsed_element())
    #         # elements.append(self.SABL.time_remaining())
    #         # elements.append(self.SABL.queue_button())
    #         # elements.append(self.SABL.connected_device())
    #         # elements.append(self.SABL.mute_button())
    #         # elements.append(self.SABL.volume_bar())
    #         # 14 elements
    #         for element in elements:
    #             robologger.warn(f"\n Webelement text: {element.text}\n"
    #                   f"Webelement: {element}\n")
    #         # for element in elements:
    #         #     actions = ActionChains(self.SABL.ret_driver())
    #         #     actions.move_to_element(element)
    #         #     actions.pause(2)
    #         #     actions.perform()
    #     except Exception as err:
    #         robologger.warn(f"An element was not detected and this is the error: {err}")
    #         raise AssertionError("Not all bottom ui elements were present.")
    #         pass

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
