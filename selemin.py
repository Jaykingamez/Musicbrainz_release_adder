from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from itertools import count
import amazon
import time


def login(browser):
    login_click = browser.find_element_by_link_text('Log In')
    login_click.click()
    username = browser.find_element_by_id('id-username')
    username.send_keys('Jaykin')
    password = browser.find_element_by_id('id-password')
    password.send_keys('Hacker123')
    password.send_keys(Keys.ENTER)


def add_release(browser):
    editing = browser.find_element_by_class_name('editing')
    editing.click()
    release_add = browser.find_element_by_link_text('Add Release')
    release_add.click()


def release_information(browser, album, artis, primary):
    title = browser.find_element_by_id('name')
    title.send_keys(album)
    artist = browser.find_element_by_class_name('ui-autocomplete-input')
    artist.send_keys(artis)
    time.sleep(1)
    artist.send_keys(Keys.TAB)
    release_group = browser.find_element_by_id('release-group')
    release_group.clear()
    release_group.send_keys(album)
    time.sleep(1)
    release_group.send_keys(Keys.TAB)
    select = Select(browser.find_element_by_id('primary-type'))
    select.select_by_visible_text(primary)
    select = Select(browser.find_element_by_id('status'))
    select.select_by_visible_text('Official')
    select = Select(browser.find_element_by_id('language'))
    select.select_by_visible_text('English')
    select = Select(browser.find_element_by_id('script'))
    select.select_by_visible_text('Latin')


def release_event(browser, release_date, labe):
    year = browser.find_element_by_class_name('partial-date-year')
    year.send_keys(release_date.year)
    month = browser.find_element_by_class_name('partial-date-month')
    month.send_keys(release_date.month)
    day = browser.find_element_by_class_name('partial-date-day')
    day.send_keys(release_date.day)
    select = Select(browser.find_element_by_id('country-0'))
    select.select_by_value('240')
    label = browser.find_elements_by_class_name('ui-autocomplete-input')[1]
    label.send_keys(labe)
    time.sleep(1)
    label.send_keys(Keys.TAB)
    no_barcode = browser.find_element_by_id('no-barcode')
    no_barcode.click()
    select = Select(browser.find_element_by_id('packaging'))
    select.select_by_value('7')


def external_links(browser, url):
    add_link = browser.find_element_by_class_name('value')
    add_link.send_keys(url)


def next_release_information(browser):
    button = browser.find_element_by_xpath("//div[@class='buttons']//button[@data-click='nextTab']")
    button.click()


def check_duplicate(browser, date):
    dates = []
    medium = []
    for x in range(1,len(browser.find_elements_by_xpath('//*[@id="duplicates-tab"]/fieldset/table/tbody/tr'))+1):
        dates += browser.find_elements_by_xpath(f'//*[@id="duplicates-tab"]/fieldset/table/tbody/tr[{x}]/td[5]')[0].text.split()
    for y in range(len(browser.find_elements_by_xpath('//*[@id="duplicates-tab"]/fieldset/table/tbody/tr'))):
        medium.append(''.join(browser.find_elements_by_xpath(f'//*[@id="duplicates-tab"]/fieldset/table/tbody/tr[{y+1}]/td[3]')[0].text))
    if dates.count(str(date)) > 0 and medium.count('Digital Media') > 0:
        browser.quit()
        raise Exception('Already in database')
    button = browser.find_element_by_css_selector('button[data-click="nextTab"]')
    button.click()


def input_release(browser, multi_artist, titles, durations, artist):
    inpu = browser.find_elements_by_tag_name('textarea')[-1]
    if len(multi_artist)== 0:
        for i, title, duration in zip(count(1), titles, durations):
            inpu.send_keys(f"{i}. {title} - {artist} ({duration})")
            inpu.send_keys(Keys.ENTER)
    else:
        for i, title, duration, artist in zip(count(1), titles, durations, multi_artist):
            inpu.send_keys(f"{i}. {title} - {artist} ({duration})")
            inpu.send_keys(Keys.ENTER)
    button = browser.find_element_by_css_selector('button[data-click="addDisc"]')
    button.click()
    select = Select(browser.find_elements_by_tag_name('select')[8])
    select.select_by_visible_text('Digital Media')
    button = browser.find_element_by_css_selector('button[data-click="nextTab"]')
    button.click()


def recordings(browser):
    buttons = browser.find_elements_by_class_name("edit-track-recording")
    counter = 1
    for element in buttons:
        element.click()
        time.sleep(3)
        name = browser.find_element_by_xpath(f'//*[@id="recordings"]/div/div[2]/div/fieldset/table/tbody/tr[{counter}]'
                                             f'/td[2]/'f'bdi').text
        check_name = browser.find_element_by_xpath('//*[@id="recording-assoc-bubble"]/table/tbody/tr[2]/td[2]/a').text
        if check_name.casefold() == name.casefold():
            radio = browser.find_element_by_xpath('//*[@id="recording-assoc-bubble"]/table/tbody/tr[2]/td[1]')
            radio.click()
        counter += 3
    button = browser.find_element_by_css_selector('button[data-click="nextTab"]')
    button.click()


def edit_note(browser):
    note = browser.find_element_by_id('edit-note-text')
    note.send_keys('This is done by an automated bot, contact the user if there any errors.')
    checkbox = browser.find_element_by_class_name('make-votable')
    checkbox.click()
    enter_edit = browser.find_element_by_id('enter-edit')
    enter_edit.click()


if __name__ == "__main__" :
    browser = webdriver.Chrome('D:\\chromedriver_win32\\chromedriver.exe')
    browser.get('https://musicbrainz.org/')
    login(browser)
    add_release(browser)
    release_information(browser, amazon.album, amazon.artis, amazon.primary_type)
    release_event(browser, amazon.release_date, amazon.label)
    external_links(browser, amazon.url)
    next_release_information(browser)
    check_duplicate(browser, amazon.release_date)
    input_release(browser, amazon.multi_artist, amazon.titles, amazon.durations, amazon.artis)
    recordings(browser)
    edit_note(browser)








