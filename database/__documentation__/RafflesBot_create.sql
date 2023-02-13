-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2023-02-12 15:25:19.141

-- tables
-- Table: admins
CREATE TABLE admins (
    user_id bigint  NOT NULL,
    CONSTRAINT admins_pk PRIMARY KEY (user_id)
);

-- Table: channels
CREATE TABLE channels (
    channel_id bigint  NOT NULL,
    title varchar(256)  NOT NULL,
    link varchar(64)  NOT NULL,
    CONSTRAINT channels_pk PRIMARY KEY (channel_id)
);

-- Table: participants
CREATE TABLE participants (
    user_id bigint  NOT NULL,
    raffle_id int  NOT NULL,
    CONSTRAINT participants_pk PRIMARY KEY (user_id,raffle_id)
);

-- Table: raffles
CREATE TABLE raffles (
    raffle_id int  NOT NULL GENERATED ALWAYS AS IDENTITY,
    start_datetime timestamp  NOT NULL,
    end_datetime timestamp  NOT NULL,
    number_of_winners int  NOT NULL,
    description varchar(1024)  NULL,
    image_url varchar(256)  NULL,
    CONSTRAINT raffles_pk PRIMARY KEY (raffle_id)
);

-- Table: raffles_channels
CREATE TABLE raffles_channels (
    raffle_id int  NOT NULL,
    channel_id bigint  NOT NULL,
    CONSTRAINT raffles_channels_pk PRIMARY KEY (raffle_id,channel_id)
);

-- Table: roles
CREATE TABLE roles (
    role_id int  NOT NULL GENERATED ALWAYS AS IDENTITY,
    title varchar(5)  NOT NULL,
    CONSTRAINT roles_pk PRIMARY KEY (role_id)
);

-- Table: users
CREATE TABLE users (
    user_id bigint  NOT NULL,
    first_name varchar(128)  NOT NULL,
    last_name varchar(128)  NULL,
    username varchar(32)  NULL,
    registration_datetime timestamp  NOT NULL,
    alive boolean  NOT NULL DEFAULT true,
    blocked boolean  NOT NULL DEFAULT false,
    role_id int  NOT NULL DEFAULT 1,
    CONSTRAINT users_pk PRIMARY KEY (user_id)
);

CREATE INDEX users_idx_1 on users USING btree (role_id ASC);

-- foreign keys
-- Reference: admins_users (table: admins)
ALTER TABLE admins ADD CONSTRAINT admins_users
    FOREIGN KEY (user_id)
    REFERENCES users (user_id)
    ON DELETE  CASCADE 
    ON UPDATE  CASCADE 
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: participants_raffles (table: participants)
ALTER TABLE participants ADD CONSTRAINT participants_raffles
    FOREIGN KEY (raffle_id)
    REFERENCES raffles (raffle_id)
    ON DELETE  CASCADE 
    ON UPDATE  CASCADE 
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: participants_users (table: participants)
ALTER TABLE participants ADD CONSTRAINT participants_users
    FOREIGN KEY (user_id)
    REFERENCES users (user_id)
    ON DELETE  CASCADE 
    ON UPDATE  CASCADE 
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: raffles_channels_channels (table: raffles_channels)
ALTER TABLE raffles_channels ADD CONSTRAINT raffles_channels_channels
    FOREIGN KEY (channel_id)
    REFERENCES channels (channel_id)
    ON DELETE  CASCADE 
    ON UPDATE  CASCADE 
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: raffles_raffles_channels (table: raffles_channels)
ALTER TABLE raffles_channels ADD CONSTRAINT raffles_raffles_channels
    FOREIGN KEY (raffle_id)
    REFERENCES raffles (raffle_id)
    ON DELETE  CASCADE 
    ON UPDATE  CASCADE 
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: users_roles (table: users)
ALTER TABLE users ADD CONSTRAINT users_roles
    FOREIGN KEY (role_id)
    REFERENCES roles (role_id)
    ON DELETE  CASCADE 
    ON UPDATE  CASCADE 
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- End of file.

