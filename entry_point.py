import argparse
import sys
sys.path.append('./components/')
import er_events_collector as EEC
import mapper_json_ld as MJLD

import os

if __name__ == "__main__":

    # TOP-LEVEL PARSER
    parser = argparse.ArgumentParser()

    # add argument to choose the mode: only events donwload, only mapping, both
    parser.add_argument('-m','--mode', type=str, default='dm', 
        help="['d' download events | 'm' map events | 'dm' do both] (Default 'dm')")     

    args = parser.parse_args()

    if (args.mode == 'd') | (args.mode == 'dm'):
        os.system("py components/er_events_collector.py")
    
    if (args.mode == 'm') | (args.mode == 'dm'):
        os.system("py components/mapper_json_ld.py")