from typing import List

from src.models.map_time_models import CarInfo
from src.models.v2x_models import Uct, Mec, UctStats
from src.v2x.mec import get_mec_by_location


def calculate_and_print_uct_stats(car_time_locations: List[CarInfo], mecs: List[Mec]):

    print('Calculating UCTs...')
    assign_ucts_to_mecs(car_time_locations, mecs)

    uct_stats = calculate_uct_stats(mecs)

    print('Max uct frequency:', uct_stats.max_uct_freq)
    print('Min uct frequency:', uct_stats.min_uct_freq)
    print('Summary uct count for all MECs:', uct_stats.all_uct_count)


def assign_ucts_to_mecs(car_time_locations: List[CarInfo], mecs: List[Mec]):
    """Retrieves UCTs and calculates statistics for them.

    """
    for car in car_time_locations:
        for i in range(len(car.time_locations) - 1):
            location1 = car.time_locations[i].location
            location2 = car.time_locations[i+1].location
            mec1 = get_mec_by_location(location1, mecs)
            mec2 = get_mec_by_location(location2, mecs)

            if mec1 is None:
                raise ValueError(f'Location out range of any MEC! Location: ({location1.x}, {location1.y})')

            if mec2 is None:
                raise ValueError(f'Location out range of any MEC! Location: ({location2.x}, {location2.y})')

            if mec1.Id != mec2.Id:
                uct_time = (car.time_locations[i].time + car.time_locations[i+1].time) / 2  # average time
                uct = Uct(uct_time, mec2.Id)

                mec1.ucts.append(uct)


def calculate_uct_stats(mecs: List[Mec]) -> UctStats:
    uct_stats = UctStats()
    uct_stats.max_uct_freq = max(map(lambda mec: get_uct_frequency_for_mec(mec), mecs))
    uct_stats.min_uct_freq = min(map(lambda mec: get_uct_frequency_for_mec(mec), mecs))
    uct_stats.all_uct_count = sum(map(lambda mec: len(mec.ucts), mecs))

    return uct_stats


def get_uct_frequency_for_mec(mec: Mec):
    if len(mec.ucts) in [0, 1]:
        return 0

    max_time = max(map(lambda uct: uct.time, mec.ucts))
    min_time = min(map(lambda uct: uct.time, mec.ucts))
    period = abs(max_time - min_time)

    return len(mec.ucts) / period
