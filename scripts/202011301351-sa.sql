CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS "User_Statuses"
(
    id serial NOT NULL,
    const character varying(45) COLLATE pg_catalog."default" NOT NULL,
    description character varying(100) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "User_Statuses_pkey" PRIMARY KEY (id)
);

INSERT INTO "User_Statuses" (const, description) VALUES
('ACTIVE', 'An active user in the system'),
('DISABLED', 'A disabled user in the system'),
('DELETED', 'A deleted user in the system');

CREATE TABLE IF NOT EXISTS "User_SuperUsers"
(
    id serial NOT NULL,
    username character varying(100) COLLATE pg_catalog."default" NOT NULL,
    password character varying(255) COLLATE pg_catalog."default" NOT NULL,
    email character varying(100) COLLATE pg_catalog."default" NOT NULL,
    phone character varying(45) COLLATE pg_catalog."default",
    created_date date NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_status_id integer NOT NULL,
    first_name character varying(45) COLLATE pg_catalog."default",
    last_name character varying(45) COLLATE pg_catalog."default",
    uuid uuid NOT NULL DEFAULT uuid_generate_v4(),
    CONSTRAINT "User_SuperUsers_pkey" PRIMARY KEY (id),
    CONSTRAINT "unique_User_SuperUsers_username" UNIQUE (username),
    CONSTRAINT "unique_User_SuperUsers_uuid_" UNIQUE (uuid),
    CONSTRAINT "fk_User_SuperUsers_user_status_id" FOREIGN KEY (user_status_id)
        REFERENCES "User_Statuses" (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);
