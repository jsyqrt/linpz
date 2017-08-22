
use songs_to_your_eyes;

CREATE TABLE tracks(
    id INT NOT NULL,
    name VARCHAR(500) NOT NULL,
    album VARCHAR(500) NOT NULL,
    artist VARCHAR(500) NOT NULL,

    publishers VARCHAR(500) NOT NULL,
    description VARCHAR(1000) NOT NULL,
    lenght VARCHAR(500) NOT NULL,
    cue_type VARCHAR(500) NOT NULL,
    label VARCHAR(500) NOT NULL,
    release_date VARCHAR(500) NOT NULL,
    catalog VARCHAR(500) NOT NULL,
    composer VARCHAR(500) NOT NULL,
    genre VARCHAR(500) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE sim_tracks(
    id INT NOT NULL,
    sim_to_id INT NOT NULL,
    sim_index INT NOT NULL,
    PRIMARY KEY (id, sim_to_id),
    FOREIGN KEY (id) REFERENCES tracks(id)
    FOREIGN KEY (sim_to_id) REFERENCES tracks(id)
);

