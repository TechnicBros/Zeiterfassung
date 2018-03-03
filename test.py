uid = [42, 961, 411, 85, 88, 99]
if len(uid) == 5:
    uid = str(uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3]) + str(uid[4])
else:
    uid = str(uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3])
print(uid)