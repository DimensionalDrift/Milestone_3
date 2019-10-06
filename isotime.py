# ISO Time Helper Script


# Takes two numbers and returns an ISO 8601 formated time
def toisostring(h, m):
    return "PT" + str(h) + "H" + str(m) + "M"


# Takes an ISO 8601 time and returns hours and mins
def fromisostring(time):
    val = time.strip("PT").replace("M", "").split("H")
    print(val)
    return "%02d:%02d" % (int(val[0]), int(val[1]))


# Function to convert time string into a ISO 8601 format
def converttime(time):
    # If the times are not valid, return a blank string
    if ":" not in time:
        return ""
    # Split the string
    time = time.split(":")

    # Loop over the items in the list, where there is a leading zero,
    # remove it
    for i in range(len(time)):
        if time[i][0] == "0":
            time[i] = time[i][1]

    # Return the ISO compatible string
    return toisostring(time[0], time[1])


# Function to add two times together and return the sum in ISO 8601 format
def addtime(t1, t2):
    # If the times are not valid, return a blank string
    if ":" not in t1 or ":" not in t2:
        return ""
    # Split the string
    t1 = t1.split(":")
    t2 = t2.split(":")

    # Convert the times into minutes
    t1 = int(t1[1]) + (int(t1[0]) * 60)
    t2 = int(t2[1]) + (int(t2[0]) * 60)

    # Add the times together
    tt = t1 + t2

    # Convert back to hours and minutes
    tt = divmod(tt, 60)

    # Return the ISO compatible string
    return toisostring(tt[0], tt[1])
