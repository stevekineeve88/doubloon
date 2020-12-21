CREATE TABLE "App_Apps"
(
    id serial NOT NULL,
    name character varying(20) COLLATE pg_catalog."default" NOT NULL,
    uuid uuid NOT NULL DEFAULT uuid_generate_v4(),
    api_key character varying(100) COLLATE pg_catalog."default" NOT NULL,
    created_date date DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "App_Apps_pkey" PRIMARY KEY (id),
    CONSTRAINT "unique_App_Apps_name" UNIQUE (name),
    CONSTRAINT "unique_App_Apps_uuid" UNIQUE (uuid)
)