CREATE TABLE factory (
    factory_id SERIAL,
    url VARCHAR(2048) NOT NULL,
    file_name VARCHAR(50) NOT NULL,
    file_size  BIGINT NOT NULL,
    work_size INTEGER NOT NULL,
    PRIMARY KEY (factory_id)
);

CREATE TABLE worker (
    worker_id SERIAL,
    factory_id INTEGER,
    PRIMARY KEY (worker_id),
    FOREIGN KEY (factory_id) REFERENCES factory (factory_id) ON DELETE CASCADE

);

CREATE TABLE work (
    work_id INTEGER,
    factory_id INTEGER,
    worker_id INTEGER,
    work_status varchar(10) DEFAULT 'unassigned',
    PRIMARY KEY (factory_id, work_id),
    FOREIGN KEY (factory_id) REFERENCES factory (factory_id) ON DELETE CASCADE,
    FOREIGN KEY (worker_id) REFERENCES worker (worker_id) ON DELETE CASCADE
);
