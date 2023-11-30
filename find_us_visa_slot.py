import json
import http.client
import multiprocessing
from multiprocessing import Event
import time
import threading
import datetime
import pygame
import simpleaudio

conn = http.client.HTTPSConnection("www.usvisascheduling.com")
headers = {
#  Copy paste Header from Network tab
}

def getTS():
    # Get the current datetime
    current_datetime = datetime.datetime.now()

    # Convert datetime to milliseconds since the epoch
    return int(current_datetime.timestamp() * 1000)


def fetch_schedule(payload):
    conn.request("POST",
                 "/en-US/custom-actions/?route=/api/v1/schedule-group/get-family-ofc-schedule-days&cacheString=" + str(
                     getTS()), payload, headers)
    return conn.getresponse()


def refresh_session():
    payload = ''
    conn.request("GET", "/en-US/custom-actions/?route=/api/v1/session/valid&cacheString=" + str(getTS()), payload,
                 headers)
    res = conn.getresponse()
    data = res.read()
    # print(data.decode("utf-8"))


def mumbai():
    return "parameters={\"primaryId\":\"796d1907-048e-ee11-a821-001dd8030ef7\",\"applications\":[\"796d1907-048e-ee11-a821-001dd8030ef7\"],\"scheduleDayId\":\"b27614f2-7ac3-ed11-83fd-001dd803c225\",\"scheduleEntryId\":\"3c1e1840-8ec3-ed11-83fd-001dd803c225\",\"postId\":\"486bf614-b0db-ec11-a7b4-001dd80234f6\"}"


def chennai():
    return "parameters={\"primaryId\":\"796d1907-048e-ee11-a821-001dd8030ef7\",\"applications\":[\"796d1907-048e-ee11-a821-001dd8030ef7\"],\"scheduleDayId\":\"b27614f2-7ac3-ed11-83fd-001dd803c225\",\"scheduleEntryId\":\"3c1e1840-8ec3-ed11-83fd-001dd803c225\",\"postId\":\"3f6bf614-b0db-ec11-a7b4-001dd80234f6\"}"


def hyd():
    return "parameters={\"primaryId\":\"796d1907-048e-ee11-a821-001dd8030ef7\",\"applications\":[\"796d1907-048e-ee11-a821-001dd8030ef7\"],\"scheduleDayId\":\"b27614f2-7ac3-ed11-83fd-001dd803c225\",\"scheduleEntryId\":\"3c1e1840-8ec3-ed11-83fd-001dd803c225\",\"postId\":\"436bf614-b0db-ec11-a7b4-001dd80234f6\"}"


def print_res(res, location):
    data = res.read()
    response = data.decode("utf-8")
    # print(response)
    if '401 Unauthorized' not in response:
        date = json.loads(response)['ScheduleDays'][000]['Date'].split('T')[0]
        # print(date)
        date_split = date.split('-')
        if date_split[0] == '2023' and date_split[1] == '12':
            print(location + " BOOK BOOK BOOK!!! || date " + date + " !!")
            print(datetime.datetime.now())
            alert()
        if date_split[0] == '2024' and date_split[1] == '01':
            print(location + " BOOK BOOK BOOK!!! || date " + date + " !!")
            print(datetime.datetime.now())
            alert()
        elif date_split[0] == '2024':
            print(location + ' : !MONTH MONTH MONTH is ' + date)
        # else:
            # alert()
    else:
        print("UN-AUTH in " + location)

def fetch_earliest_schedule():

    # Creating threads for each function
    thread1 = threading.Thread(target=print_res(fetch_schedule(mumbai()), ' MUMBAI '))
    thread2 = threading.Thread(target=print_res(fetch_schedule(chennai()), ' CHENNAI '))
    thread3 = threading.Thread(target=print_res(fetch_schedule(hyd()), ' HYDERABAD '))

    # Starting threads
    thread1.start()
    thread2.start()
    thread3.start()

    # Waiting for threads to complete (optional)
    thread1.join()
    thread2.join()
    thread3.join()


def alert():
    # Initialize Pygame
    pygame.init()

    # Load the MP3 file
    # Replace 'path_to_mp3_file.mp3' with your MP3 file
    pygame.mixer.music.load('/path/to/mp3/file.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()
    time.sleep(3)
    # Keep the program running while the MP3 is playing
    # while pygame.mixer.music.get_busy():
    #     pygame.time.Clock().tick(10) # Adjust the playback speed if needed

    # Quit Pygame
    pygame.quit()


def main():
    for i in range(5000):
        print("Run # " + str(i))
        fetch_earliest_schedule()
        time.sleep(1)

main()