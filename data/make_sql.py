# coding: utf-8

import json

def extract_sim_tracks_relation_from_json_to_sql(json_string):
    x = json_string
    sqls = []
    for sim_index, relation in enumerate(x['sim_tracks']):
        sql = '(%s)' % ', '.join(
                list(map(lambda x: str(x), 
                    [
                        x['id'],
                        relation['id'],
                        sim_index,
                    ]))
                    )
        sql = sql.encode('utf8', errors='ignore')
        sqls.append(sql)
    sql = ',\n'.join(sqls) + ',\n'
    return sql

def extract_track_detail_info_from_json_to_sql(json_string):
    x = json_string
    sql = str(x['id']) + ', ' + ', '.join(list(map(lambda x: '"%s"'%x.replace('"', '\\"'),
        [
            x['name'],
            x['album'],
            x['artist'],
            x['publishers'],
            x['description'],
            x['length'],
            x['cue_type'],
            x['label'],
            (lambda x: '-'.join(([x[-1]]+x[:-1] if len(x)==3 else [])))(x['date'].split('/')),
            x['catalog'],
            x['composer'],
            x['genre'],
        ]
        )))
    sql = '(%s),\n' % sql
    sql = sql.encode('utf8', errors='ignore')
    return sql

def extract_json_to_sql_and_insert_into_sql_file(line, sql_file_name, json_to_sql_func):
    x = json.loads(line.rstrip(',\n'))
    sql = json_to_sql_func(x)
    with open(sql_file_name, 'a') as f:
        f.write(sql)

def write_to_sql_header(sql_file_name, sql_header):
    with open(sql_file_name, 'w') as f:
        f.write(sql_header)

def start_write_to_sql_file(result_file_name, sql_file_name, json_to_sql_func, sql_header):
    print 'read from %s, write to %s...' %(result_file_name, sql_file_name)
    write_to_sql_header(sql_file_name, sql_header)
    with open(result_file_name, 'r') as ff:
        for line in ff:
            if line in ['[\n', ']']:
                continue
            extract_json_to_sql_and_insert_into_sql_file(line, sql_file_name, json_to_sql_func)
    with open(sql_file_name, 'r+') as f:
        f.seek(-2, 2)
        f.write(';\n')

if __name__ == '__main__':
    from_file = 'result.json'
    tracks_sql_file = 'tracks.sql'
    sim_tracks_file = 'sim_tracks.sql'

    sql_headers = ('use rainbow; \n insert into songs_to_your_eyes_tracks\nvalues\n', 'use rainbow; \n insert into songs_to_your_eyes_sim_tracks (sim_from_id, sim_to_id, sim_index) \nvalues\n')
    start_write_to_sql_file(from_file, tracks_sql_file, extract_track_detail_info_from_json_to_sql, sql_headers[0])
    start_write_to_sql_file(from_file, sim_tracks_file, extract_sim_tracks_relation_from_json_to_sql, sql_headers[1])
