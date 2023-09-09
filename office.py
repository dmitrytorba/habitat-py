def is_active():
    return True


def lights_on():
    print("Lights on")


def lights_off():
    print("Lights off")


def office_housekeeping():
    print("Office housekeeping")
    if is_active():
        lights_on()
    else:
        lights_off()
