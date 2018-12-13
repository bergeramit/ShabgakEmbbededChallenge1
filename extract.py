import struct

TOTAL_TIME = 1984 * 60

def clean_reset(mem):
    reset = 0
    while reset != 2:
        f, length = struct.unpack("<ci", mem.read(5))
        data = mem.read(length)
        f = int(f.encode("hex"))
        if f == 0:
            reset += 1
    return mem


def main():
    time_left = TOTAL_TIME
    current_time_to_save = 150 * 4.0
    with open("shabak_challenge/external_mem_dump.bin", "rb") as mem:
        mem = clean_reset(mem)
        while time_left > 0:
            f, length = struct.unpack("<ci", mem.read(5))
            data = mem.read(length)
            f = int(f.encode("hex"))

            if f == 1:
                lon, lat = struct.unpack("<ff", data)

                time_left -= current_time_to_save
                current_time_to_save = next_time_to_save

                print "Time left: {}".format(time_left)
                if time_left == 0:
                    print "log lat: {} {}".format(lon, lat)

            elif f == 2:
                next_time_to_save = 15 * 4
                print "In a = 2"

            elif f == 3:
                next_time_to_save = 150 * 4
                print "In a = 3"


main()
