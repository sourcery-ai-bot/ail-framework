#!/usr/bin/env python3
# -*-coding:UTF-8 -*

import os
import re
import sys
import time
import redis
import datetime

sys.path.append(os.path.join(os.environ['AIL_BIN'], 'lib/'))
import ConfigLoader
import Tracker

def update_update_stats():
    nb_updated = int(r_serv_db.get('update:nb_elem_converted'))
    progress = int((nb_updated * 100) / nb_elem_to_update)
    print('{}/{}    updated    {}%'.format(nb_updated, nb_elem_to_update, progress))
    r_serv_db.set('ail:current_background_script_stat', progress)

if __name__ == '__main__':

    start_deb = time.time()

    config_loader = ConfigLoader.ConfigLoader()
    r_serv_db = config_loader.get_redis_conn("ARDB_DB")
    config_loader = None

    r_serv_db.set('ail:current_background_script', 'trackers update')

    nb_elem_to_update = r_serv_db.get('update:nb_elem_to_convert')
    if not nb_elem_to_update:
        nb_elem_to_update = 1
    else:
        nb_elem_to_update = int(nb_elem_to_update)

    while True:
        tracker_uuid = r_serv_onion.spop('trackers_update_v3.7')
        if tracker_uuid is not None:
            print(tracker_uuid)
            # FIX STATS
            Tracker.fix_tracker_stats_per_day(tracker_uuid)
            # MAP TRACKER - ITEM_ID
            Tracker.fix_tracker_item_link(tracker_uuid)


            r_serv_db.incr('update:nb_elem_converted')
            update_update_stats()

        else:
            r_serv_db.set('ail:current_background_script_stat', 100)
            sys.exit(0)
