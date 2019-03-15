import argparse
import os

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    # add argument to choose the mode: only events donwload, only mapping, both
    parser.add_argument('-m','--mode', type=str, default='dm', 
        help="['d' download events | 'm' map events | 'dm' do both] (Default 'dm')")     

    args = parser.parse_args()

    if (args.mode == 'd') | (args.mode == 'dm'):
        os.system("py components/er_events_collector.py")
    
    if (args.mode == 'm') | (args.mode == 'dm'):
        os.system("py components/mapper_json_ld.py")
    
    # save event mapped in JSON-LD in ArangoDB
    os.system("py components/arangodb_connector.py")