# A program to count and analyze the number of times Devan has sobbed
# Author: Yunfei Zheng, May 2024

# Imports
import datetime
import json
import re
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Constants
FILENAME1 = "svengers/message_1.json"
FILENAME2 = "svengers/message_2.json"
SOB_EMOJI = "\u00f0\u009f\u0098\u00ad" # What it shows up as due to bsf encoding
DEVAN_USERNAME = "Devan  :)"
MS_IN_S = 1000.0 # Number of milliseconds in a second

# Open the file and get it, then load it as a json
file1 = open(FILENAME1)
dict1 = json.loads(file1.read())
file1.close()
file2 = open(FILENAME2)
dict2 = json.loads(file2.read())
file2.close()
# get all the messages together in one List
message_list = dict1["messages"] + dict2["messages"]

total_count = 0 # Raw total of sobs
max_count = 0 # Maximum sobs in a single message
max_count_time = 0 # Time of max_count message
sob_times = [] # Array containing datetime objects
sob_counts = [] # Array containing # of sobs in a message

first_msg_time = None
last_msg_time = None

# function to find number of occurrences of a substring in a string
def numOccurrences(substr, message):
    if message == None:
        return 0
    else:
        return len(re.findall(substr, message))

# Find the correct messages
for data in message_list:
    # Only Devan's messages
    if data["sender_name"] == DEVAN_USERNAME:
        message = data.get("content")
        numOccurs = numOccurrences(SOB_EMOJI, message) # number of times sob emoji is in message
        # If contains sobbing, update all tracked values
        if numOccurs > 0:
            time_ms = data["timestamp_ms"] # time of message in ms
            # get first and last msg times
            if first_msg_time == None or time_ms < first_msg_time:
                first_msg_time = time_ms
            if last_msg_time == None or time_ms > last_msg_time:
                last_msg_time = time_ms
            # update total_count
            total_count += 1
            # update max_count
            if numOccurs > max_count:
                max_count = numOccurs
                max_count_time = time_ms
            # update times
            # To represent the multiple sobs add it that many times
            for i in range(numOccurs):
                # Convert from milliseconds to datetime object
                dt = datetime.datetime.fromtimestamp(time_ms / MS_IN_S)
                sob_times.append(dt)
            # add one to sob counts
            sob_counts.append(numOccurs)

# Analysis
print("Beginning analysis of Devan's sob emoji use...")
first_msg_date = datetime.datetime.fromtimestamp(first_msg_time / MS_IN_S).date()
last_msg_date = datetime.datetime.fromtimestamp(last_msg_time / MS_IN_S).date()
print("Devan has sobbed", total_count, "times in the Svengers chat from", first_msg_date, "to", last_msg_date)
duration = last_msg_date - first_msg_date
print("That's an average of", total_count / duration.days, "times a day!")

max_sobs_date = datetime.datetime.fromtimestamp(max_count_time / MS_IN_S)
print("The maximum number of sobs in a single message is:", max_count, "on:", max_sobs_date)

# Print out the sob graph
print("Now plotting out data on graph...")
# convert the epoch format to matplotlib date format 
mpl_data = mdates.date2num(sob_times)
# plot it
fig = plt.figure()
ax1 = fig.add_subplot(121)
ax1.hist(mpl_data, bins=50, color='green') 
locator = mdates.WeekdayLocator(byweekday=1, interval=2)
ax1.xaxis.set_major_locator(locator)
ax1.xaxis.set_major_formatter(mdates.AutoDateFormatter(locator))

ax1.set_title("Devan Sob Analysis from " + str(first_msg_date) + " to " + str(last_msg_date))
ax1.set_xlabel("Date")
ax1.set_ylabel("Sob Quantity")

fig.autofmt_xdate()

ax2 = fig.add_subplot(122)
# Convert to pie chart format
sob_num_array = [0] * (max_count + 1)
for num in sob_counts:
    sob_num_array[num] += 1
sob_num_array.remove(0)
# Currently doesn't count messages without sobs
ax2.pie(sob_num_array, labels=list(range(1, max_count + 1)))
ax2.set_title("Devan Sob Analysis: # of Sobs in a Single Message")

# show it
plt.show()