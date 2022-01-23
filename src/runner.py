import json
import logging
from typing import List

from src.constants import DEFAULT_LOGGER_NAME, RUNS_CONFIG_KEY, RUN_ID_CONFIG_KEY, RUN_CONFIG_CONFIG_KEY, \
    DEFAULT_CONFIG_CONFIG_KEY, eNB_MEC_ID_CONFIG_KEY, MEC_INCLUDED_eNodeB_IDS
from src.helpers.drawing import save_sim_image
from src.helpers.time_helpers import print_execution_time
from src.models.v2x_models import eNodeB, UctStats
from src.v2x.enodeb import extract_eNodeBs_and_create_ranges2
from src.v2x.mec import extract_mecs_with_ranges
from src.v2x.uct import UctCalc

logger = logging.getLogger(DEFAULT_LOGGER_NAME)


@print_execution_time
def read_config_and_execute_runs(car_time_location_raw: List[List], net_file: str, eNodeB_mec_config_file: str):
    output_json_file = 'output.json'
    sim_image_file = 'sim_image.png'

    with open(eNodeB_mec_config_file, 'r') as f:
        config_data = json.load(f)

    if DEFAULT_CONFIG_CONFIG_KEY not in config_data.keys() or type(config_data[DEFAULT_CONFIG_CONFIG_KEY]) is not list:
        logger.error('No default config dict in config file')
        raise ValueError('No default config dict in config file')

    eNodeBs = extract_eNodeBs_and_create_ranges2(net_file, config_data)

    global_stats = []
    uct_calc = UctCalc()

    if type(config_data[RUNS_CONFIG_KEY]) is list:
        logger.info('runs count: %d', len(config_data[RUNS_CONFIG_KEY]))

        for run in config_data[RUNS_CONFIG_KEY]:
            run_id = int(run[RUN_ID_CONFIG_KEY])

            logger.debug('run_id: %d', run_id)

            if RUN_CONFIG_CONFIG_KEY not in run.keys() or type(run[RUN_CONFIG_CONFIG_KEY]) is not list:
                logger.error('No run_config for run_id: %d', run_id)
                raise ValueError(f'No run_config for run_id: {run_id}')

            apply_run_config_to_eNodeBs(run[RUN_CONFIG_CONFIG_KEY], eNodeBs)
            uct_stats = execute_run(uct_calc, run_id, car_time_location_raw, eNodeBs)
            global_stats.append(uct_stats)

    else:
        uct_stats = execute_run(uct_calc, 0, car_time_location_raw, eNodeBs)
        global_stats.append(uct_stats)

    save_results_to_json_file(global_stats, output_json_file)
    logger.info('UCT stats saved to %s file', output_json_file)

    save_sim_image(uct_calc.xx, uct_calc.yy, eNodeBs, sim_image_file)
    logger.info('Simulation image saved to %s file', sim_image_file)


def apply_run_config_to_eNodeBs(run_config: List[dict], eNodeBs: List[eNodeB]):
    for enb in eNodeBs:
        mec_id = next(filter(lambda x: enb.Id in x[MEC_INCLUDED_eNodeB_IDS], run_config))[eNB_MEC_ID_CONFIG_KEY]
        enb.assigned_mec_id = mec_id


def execute_run(uct_calc: UctCalc, run_id: int, car_time_locations_raw: List[List], eNodeBs: List[eNodeB]) -> UctStats:
    mecs = extract_mecs_with_ranges(eNodeBs)
    uct_stats = uct_calc.retrieve_ucts_and_calculate_stats(car_time_locations_raw, eNodeBs, mecs)
    uct_stats.run_id = run_id
    return uct_stats


def save_results_to_json_file(global_stats: List[UctStats], file_name: str):
    jason = json.dumps([uct_stats.__dict__ for uct_stats in global_stats], indent=4)
    with open(file_name, 'w') as f:
        f.write(jason)
