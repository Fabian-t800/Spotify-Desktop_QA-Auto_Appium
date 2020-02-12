*** Settings ***
Suite Setup       Maximize window
Resource          keywords.robot
Resource          Helper_kw.robot

*** Test Cases ***
Create new playlist
    [Setup]
    Click home button
    Press New Playlist Button
    Enter name into the name field    ${playlist_name_create_new_pl}
    Press Create Playlist Button
    Then Validate if the playlist has been created
    [Teardown]    Teardown - Delete newly created empty playlist

Toggle functionality test
    [Setup]    Click home button
    Click on Profile menu
    Click the Settings menu element    ${menu_element_name}
    Determine the toggle's current state    ${toggle_element_description}
    Click the toggle button    ${toggle_element_description}
    Determine the toggle's current state again
    Assert if the toggle state has changed

Play song functionality
    [Setup]    Click home button
    Click play button
    Read the time elapsed timer
    Wait for time to elapse
    Click play button
    Read the time elapsed timer again
    Assert if it had any effect

Drag and drop functionality
    [Setup]    Click home button
    Click source playlist    ${source_playlist_name}
    Drag and drop song from source playlist to target playlist    ${song_name}    ${target_playlist_name}
    Click on target playlist
    Assert if the song has been successfully dragged and dropped

Delete song from playlist test
    Drag and drop tc teardown

Bottom Console UI Test
    Click home button
    Verify bottom ui console

Search functionality test
    Click home button
    Click search field
    Type in search keyword    ${search_term}
    Verify search results

Songs are present in a given playlist
    Click home button
    Click on the desired playlist     ${searched_playlist}
    Read the song from the playlist


Volume Scroll Functionality
    Click home button
    Move mouse over the volume bar
    Scroll mouse
