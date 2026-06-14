from database import (
    get_current_rider,
    get_waiting_participants,
    set_status,
    get_queue_length
)

AVG_RIDE_TIME = 2  # minutes


def call_next_rider():
    current = get_current_rider()

    if current:
        return False

    waiting = get_waiting_participants()

    if not waiting:
        return False

    next_rider = waiting[0]
    token = next_rider[1]

    set_status(token, "ON_TRACK")

    return True


def complete_current_rider():
    current = get_current_rider()

    if not current:
        return False

    token = current[1]

    set_status(token, "COMPLETED")

    return True


def skip_current_rider():
    current = get_current_rider()

    if not current:
        return False

    token = current[1]

    set_status(token, "SKIPPED")

    return True


def get_estimated_wait_time(position):
    if position is None:
        return 0

    return position * AVG_RIDE_TIME


def get_queue_stats():
    waiting = len(get_waiting_participants())

    current = get_current_rider()

    riders_served = 0

    return {
        "waiting": waiting,
        "current": current,
        "served": riders_served
    }


def get_next_five_tokens():
    waiting = get_waiting_participants()

    return waiting[:5]