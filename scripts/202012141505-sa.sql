CREATE TABLE "System_Roles"
(
    id serial NOT NULL,
    const character varying(45) NOT NULL,
    description character varying(100),
    CONSTRAINT "pk_System_Roles_id" PRIMARY KEY (id),
    CONSTRAINT "unique_System_Roles_const" UNIQUE (const)
);

INSERT INTO "System_Roles" (const, description) VALUES
('ADMIN', 'Administrator of users in an application'),
('USER', 'Users of an application able to access a token');

CREATE TABLE "User_AppUsers"
(
    id serial NOT NULL,
    user_status_id integer NOT NULL,
    system_role_id integer NOT NULL,
    username character varying(100) NOT NULL,
    uuid uuid NOT NULL DEFAULT uuid_generate_v4(),
    first_name character varying(100) NOT NULL,
    last_name character varying(100) NOT NULL,
    email character varying(100) NOT NULL,
    password character varying(255) NOT NULL,
    app_id integer NOT NULL,
    app_uuid character varying(255) NOT NULL,
    created_date date DEFAULT CURRENT_TIMESTAMP,
    phone character varying(45) NOT NULL,
    CONSTRAINT "pk_User_AppUsers_id" PRIMARY KEY (id, app_uuid),
    CONSTRAINT "unique_User_AppUsers_uuid" UNIQUE (uuid, app_uuid),
    CONSTRAINT "unique_User_AppUsers_username" UNIQUE (username, app_uuid),
    CONSTRAINT "fk_User_AppUsers_user_status_id" FOREIGN KEY (user_status_id)
        REFERENCES "User_Statuses" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT "fk_User_AppUsers_system_role_id" FOREIGN KEY (system_role_id)
        REFERENCES "System_Roles" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
) PARTITION BY LIST (app_uuid);