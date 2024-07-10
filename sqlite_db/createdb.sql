create table subscription(
    id integer primary key,
    title varchar(255),
    visible boolean DEFAULT 1,
    last_update DATETIME DEFAULT (datetime('now','localtime')),
    UNIQUE(title)
);