--
-- PostgreSQL database dump
--

\restrict HfqCDUeeXiQQVBBo8FFYYAUJdQE4lbFfFLgBxULHfoUhbnD6aY2xuIbPbddWCBa

-- Dumped from database version 16.15
-- Dumped by pg_dump version 16.15

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: records; Type: TABLE; Schema: public; Owner: barq_app
--

CREATE TABLE public.records (
    id bigint NOT NULL,
    title character varying(200) NOT NULL,
    CONSTRAINT records_title_check CHECK ((length(TRIM(BOTH FROM title)) > 0))
);


ALTER TABLE public.records OWNER TO barq_app;

--
-- Name: records_id_seq; Type: SEQUENCE; Schema: public; Owner: barq_app
--

ALTER TABLE public.records ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.records_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Data for Name: records; Type: TABLE DATA; Schema: public; Owner: barq_app
--

COPY public.records (id, title) FROM stdin;
1	Review service readiness
2	Document the operating procedure
3	persistence_test_record
\.


--
-- Name: records_id_seq; Type: SEQUENCE SET; Schema: public; Owner: barq_app
--

SELECT pg_catalog.setval('public.records_id_seq', 3, true);


--
-- Name: records records_pkey; Type: CONSTRAINT; Schema: public; Owner: barq_app
--

ALTER TABLE ONLY public.records
    ADD CONSTRAINT records_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

\unrestrict HfqCDUeeXiQQVBBo8FFYYAUJdQE4lbFfFLgBxULHfoUhbnD6aY2xuIbPbddWCBa

