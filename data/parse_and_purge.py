# coding: utf-8

import json

def parse_a_line(line):
    l = line.rstrip('\n').rstrip(',')
    l = json.loads(l)

    tid = l['track_id']
    tdi = l['detail_info'].get('data', {}).get('content', [{}, {}])[1]
    tsl = l['sim_tracks_list']
    
    track_detail_info = dict(
            id = tid,

            name = tdi.get('title', ''),
            album = tdi.get('album', {}).get('name', ''),
            artist = tdi.get('artist', {}).get('name', '') # + ', ' + tdi.get('artist', {}).get('description', ''),

            composer = tdi.get('composer', {}).get('name', ''),
            catalog = tdi.get('catalog', {}).get('name', ''),
            label = tdi.get('label', {}).get('name', ''),
            publishers = ', '.join(list(map(lambda x: x.get('name', ''), tdi.get('publishers', [])))),
            genre = ', '.join(list(map(lambda x: x.get('name', ''), tdi.get('genre', [])))),
            cue_type = ', '.join(list(map(lambda x: x.get('name', ''), tdi.get('musicProviderCueTypes', [])))),
            description = tdi.get('description', ''),

            date = tdi.get('date', ''),
            lenght = tdi.get('length', ''),

            sim_tracks = get_sim_track_list(tsl)
            
            )
    return track_detail_info

def get_sim_track_list(tsl):
    sim_tracks = list(map(lambda x: x.get('data', {}).get('content', []), tsl))
    sim_tracks.sort(key = lambda x: x[0].get('page', -1))
    return list(
            map(
                lambda x: {
                    'id': x.get('id', -1),
                    'name': x.get('title', ''),
                    'album': x.get('album', {}).get('name', ''),
                    'artist': x.get('artist', {}).get('name', ''), # + ', ' + x.get('artist', {}).get('description', ''),
                    },
                reduce(lambda x, y: x[1:]+y[1:], sim_tracks)
                )
            )

def read_parse_and_save(from_file_name, to_file_name):
    with open(to_file_name, 'w') as tt:
        tt.write('[\n')
    with open(from_file_name, 'r') as ff:
        for line in ff:
            if line in ['[\n', ']']:
                continue
            with open(to_file_name, 'a') as tt:
                tdi = parse_a_line(line)
                tt.write(json.dumps(tdi)+',\n')
    with open(to_file_name, 'a') as tt:
        tt.write(']')

if __name__ == '__main__':
    from_file = 'sye.json'
    to_file   = 'result.json'
    read_parse_and_save(from_file, to_file)
