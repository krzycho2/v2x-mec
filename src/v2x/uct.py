import logging
from typing import List

import pandas as pd

from src.constants import DEFAULT_LOGGER_NAME
from src.helpers.time_helpers import print_execution_time
from src.models.map_time_models import Position2d
from src.models.v2x_models import Uct, Mec, UctStats, eNodeB
from src.v2x.enodeb import get_eNodeB_id_by_location
from src.v2x.mec import get_mec_id_by_eNodeB_id

logger = logging.getLogger(DEFAULT_LOGGER_NAME)


class UctCalc:
    xx: List[float]
    yy: List[float]
    eNodeBs: List[eNodeB]

    def retrieve_ucts_and_calculate_stats(self, car_time_locations: List[List], eNodeBs: List[eNodeB],
                                          mecs: List[Mec]) -> UctStats:

        logger.debug('Retrieving UCTs...')
        self.eNodeBs = eNodeBs
        self.parse_fcd_data_and_assign_ucts_to_mecs(car_time_locations, mecs)

        uct_stats = self.calculate_uct_stats(mecs)

        logger.debug('Max uct frequency: %f', uct_stats.max_uct_freq)
        logger.debug('Min uct frequency: %f', uct_stats.min_uct_freq)
        logger.debug('Summary uct count for all MECs: %d', uct_stats.all_uct_count)

        return uct_stats

    def parse_fcd_data_and_assign_ucts_to_mecs(self, car_time_locations: List[List], mecs: List[Mec]):
        car_groups = self.preprocess_data_and_get_car_groups(car_time_locations, mecs)
        self.retrieve_ucts(car_groups, mecs)

    # TODO: Optimize not to duplicate code in runs
    @print_execution_time
    def preprocess_data_and_get_car_groups(self, car_time_locations: List[List], mecs: List[Mec]):
        df = pd.DataFrame(car_time_locations, columns=['time_step', 'car_id', 'x', 'y'])
        df['x'] = df['x'].astype('float').round(decimals=1)
        df['y'] = df['y'].astype('float').round(decimals=1)
        df['time_step'] = df['time_step'].astype('float')

        duplicated_coords = df[['x', 'y']].drop_duplicates()
        duplicated_coords['eNodeB_id'] = duplicated_coords.apply(
            lambda row: get_eNodeB_id_by_location(Position2d(row.x, row.y), self.eNodeBs), axis=1)
        duplicated_coords['mec_id'] = duplicated_coords.apply(lambda row: get_mec_id_by_eNodeB_id(row.eNodeB_id, mecs),
                                                              axis=1)
        df = pd.merge(df, duplicated_coords, on=['x', 'y'])
        car_groups = df.groupby('car_id')

        self.xx = duplicated_coords['x']
        self.yy = duplicated_coords['y']

        return car_groups

    @print_execution_time
    def retrieve_ucts(self, car_groups, mecs: List[Mec]):
        for group_name, car_group in car_groups:
            car_group['is_uct'] = car_group['mec_id'] != car_group['mec_id'].shift()
            uct_rows = car_group[car_group['is_uct'] == True]

            index0 = car_group.index[0]
            for index, uct_row in uct_rows.iterrows():
                time_step = uct_row['time_step']

                if index == index0:
                    continue

                mec = next(filter(lambda mec: mec.Id == uct_row['mec_id'], mecs), None)
                uct = Uct(time=time_step)  # todo
                mec.ucts.append(uct)

    def calculate_uct_stats(self, mecs: List[Mec]) -> UctStats:
        uct_stats = UctStats()

        uct_stats.mecs_uct_stats = []
        for mec in mecs:
            mec_dict = {'mec_id': mec.Id,
                        'included_eNodeBs': mec.included_eNodeBs,
                        'uct_freq': self.get_uct_frequency_for_mec(mec),
                        'uct_count': len(mec.ucts)}
            uct_stats.mecs_uct_stats.append(mec_dict)

        uct_stats.max_uct_freq = max(map(lambda mec: self.get_uct_frequency_for_mec(mec), mecs))
        uct_stats.min_uct_freq = min(map(lambda mec: self.get_uct_frequency_for_mec(mec), mecs))
        uct_stats.all_uct_count = sum(map(lambda mec: len(mec.ucts), mecs))

        return uct_stats

    def get_uct_frequency_for_mec(self, mec: Mec):
        if len(mec.ucts) in [0, 1]:
            return 0

        max_time = max(map(lambda uct: uct.time, mec.ucts))
        min_time = min(map(lambda uct: uct.time, mec.ucts))
        period = abs(max_time - min_time)

        return len(mec.ucts) / period
