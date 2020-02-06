*** Settings ***
Library           appium_tests/SpotifyAppiumHelperClass.py
Resource          keywords.robot
Library           ../appium_tests/SetupAndTeardown.py

*** Keywords ***
Press New Playlist Button
    click_on_new_playlist_button

Suite teardown
    suite_teardown

Teardown - Delete newly created empty playlist
    create_new_playlist_teardown    ${playlist_name_create_new_pl}

Click home button
    press_home_button

Enter name into the name field
    [Arguments]    ${playlist_name_create_new_pl}
    send_keys_to_playlist_name_field    ${playlist_name_create_new_pl}

Press Create Playlist Button
    press_create_playlist

Validate if the playlist has been created
    new_playlist_creation_validation    ${playlist_name_create_new_pl}

Click on Profile menu
    profile_menu_click

Click the Settings menu element
    [Arguments]    ${menu_element_name}
    menu_element_click    ${menu_element_name}

Determine the toggle's current state
    [Arguments]    ${toggle_element_description}
    ${initial_toggle_state}=    toggle_element_current_state    ${toggle_element_description}
    set global variable    ${initial_toggle_state}

Click the toggle button
    [Arguments]    ${toggle_element_description}
    toggle_element_click    ${toggle_element_description}

Assert if the toggle state has changed
    assert_toggle_state    ${initial_toggle_state}    ${final_toggle_state}

Determine the toggle's current state again
    ${final_toggle_state}    toggle_element_current_state    ${toggle_element_description}
    set global variable    ${final_toggle_state}

Wait for time to elapse
    wait_for_time    ${wait_time}

Click play button
    click_the_play_button

Read the time elapsed timer
    ${initial_time_elapsed}=    time_elapsed_timer
    set global variable    ${initial_time_elapsed}

Read the time elapsed timer again
    ${final_time_elapsed}=    time_elapsed_timer
    set global variable    ${final_time_elapsed}

Assert if it had any effect
    assert_play_functionality    ${initial_time_elapsed}    ${final_time_elapsed}

Click source playlist
    [Arguments]    ${source_playlist}
    click_on_playlist    ${source_playlist}

Drag and drop song from source playlist to target playlist
    [Arguments]    ${song_name}    ${target_playlist_name}
    drag_and_drop_action    ${song_name}    ${target_playlist_name}

Click on target playlist
    click_on_playlist    ${target_playlist_name}

Assert if the song has been successfully dragged and dropped
    assert_drag_and_drop_functionality    ${song_name}

Drag and drop tc teardown
    drag_and_drop_teardown    ${song_name}

Maximize window
    max_win
