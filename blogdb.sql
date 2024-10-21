--
-- PostgreSQL database dump
--

-- Dumped from database version 14.13 (Ubuntu 14.13-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.13 (Ubuntu 14.13-0ubuntu0.22.04.1)

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
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: blogs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.blogs (
    id uuid NOT NULL,
    title character varying(255) NOT NULL,
    content text NOT NULL,
    author character varying(100) NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    summary character varying(500),
    reading_time character varying(50),
    thumbnail_url character varying(255),
    tags character varying[]
);


ALTER TABLE public.blogs OWNER TO postgres;

--
-- Name: education; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.education (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    year character varying(255) NOT NULL,
    degree character varying(255) NOT NULL,
    university character varying(255) NOT NULL,
    cgpa character varying(255) NOT NULL
);


ALTER TABLE public.education OWNER TO postgres;

--
-- Name: experience; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.experience (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    year character varying(255) NOT NULL,
    "position" character varying(255) NOT NULL,
    company character varying(255) NOT NULL,
    work_details character varying[]
);


ALTER TABLE public.experience OWNER TO postgres;

--
-- Name: social_media_links; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.social_media_links (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    facebook character varying,
    linkedin character varying,
    instagram character varying,
    github character varying
);


ALTER TABLE public.social_media_links OWNER TO postgres;

--
-- Name: testimonials; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.testimonials (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    name character varying(255) NOT NULL,
    date timestamp without time zone NOT NULL,
    designation character varying(255) NOT NULL,
    company character varying(255) NOT NULL,
    content character varying NOT NULL,
    image_link character varying(255)
);


ALTER TABLE public.testimonials OWNER TO postgres;

--
-- Name: user_skills; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_skills (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    skill character varying(255) NOT NULL,
    icon_link character varying(255) NOT NULL
);


ALTER TABLE public.user_skills OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id uuid NOT NULL,
    username character varying(255) NOT NULL,
    full_name character varying(255) NOT NULL,
    designation character varying(255) NOT NULL,
    about character varying,
    cv_link character varying,
    profile_picture_link character varying
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
b7869912064f
\.


--
-- Data for Name: blogs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.blogs (id, title, content, author, created_at, updated_at, summary, reading_time, thumbnail_url, tags) FROM stdin;
f7a37e85-88cf-4432-8716-4413248bae56	Solving Synchronization Issues in Locust Tests	## The Problem\n\nIn my Locust setup, I was facing issues where some of my test cases failed because the created rules were not properly deleted. The core of the issue was ensuring that each creation of a rule was followed by its deletion, and that updates to rules (if needed) were synchronized correctly.\n\n## The Approach\n\nTo address this, I implemented a solution that involved careful handling of synchronization between tasks. Here’s how I approached solving the problem:\n\n### 1. Task Synchronization\n\nThe key to solving the synchronization issue was to ensure that rule creation, updating, and deletion were properly sequenced. I needed to make sure that each created rule was deleted, and any updates were applied before deletion.\n\n### 2. Using Locks\n\nTo avoid concurrent issues and ensure that rule creation and deletion do not overlap incorrectly, I used a thread lock. This helped in managing the critical section where a rule is created and then later deleted:\n\n```python\nfrom threading import Lock\n\nclass OTPTaskSet(TaskSet):\n    lock = Lock()\n    rule_id = None\n\n    @task\n    def create_and_delete_rule(self):\n        with self.lock:\n            # Create rule\n            response = self.client.post("/api/firewall/v1/otp/rules", json=data, headers=headers)\n            if response.status_code == 201:\n                self.rule_id = response.json().get("objectId")\n                # If rule created, update and delete it\n                self.update_rule()\n                self.delete_rule()\n            else:\n                print(f"Failed to create rule: {response.status_code} {response.text}")\n\n    def update_rule(self):\n        if self.rule_id:\n            # Update rule logic here\n            response = self.client.put(f"/api/firewall/v1/otp/rules/{self.rule_id}", json=update_data, headers=headers)\n            if response.status_code == 200:\n                print(f"Updated Rule with ID: {self.rule_id}")\n            else:\n                print(f"Failed to update rule: {response.status_code} {response.text}")\n\n    def delete_rule(self):\n        if self.rule_id:\n            response = self.client.delete(f"/api/firewall/v1/otp/rules/{self.rule_id}", headers=headers)\n            if response.status_code == 200:\n                print(f"Deleted Rule with ID: {self.rule_id}")\n                self.rule_id = None\n            else:\n                print(f"Failed to delete rule: {response.status_code} {response.text}")\n\n```\n\n### 3. Handling Update Operations\n\nFor updating rules, I added a step to handle updates between creation and deletion. The rules for updating were:\n\n- If `rule_type` is `pass`, it can only be updated to `block`.\n- If `status` is `False`, it can only be updated to `True`, and vice versa.\n\n```python\ndef update_rule(self):\n    if self.rule_id:\n        # Update rule logic here\n        response = self.client.put(f"/api/firewall/v1/otp/rules/{self.rule_id}", json=update_data, headers=headers)\n        if response.status_code == 200:\n            print(f"Updated Rule with ID: {self.rule_id}")\n        else:\n            print(f"Failed to update rule: {response.status_code} {response.text}")\n\n```\n\n### 4. Ensuring Data Consistency\n\nBy combining the use of locks and carefully sequencing tasks, I ensured that the data was consistent and that rules were properly managed. This approach also made sure that there were no overlaps or missed operations between create, update, and delete steps.\n\n## Conclusion\n\nBy implementing a locking mechanism and ensuring that tasks were properly sequenced, I was able to resolve the synchronization issues in my Locust tests. This solution ensures that every rule created is appropriately managed, updated if necessary, and eventually deleted, leading to a more reliable and accurate load testing process.\n	Md. Maruful Islam	2024-08-20 12:03:36.412069	2024-08-25 07:36:20.417659	When performing load testing with Locust, synchronization between different test operations can be crucial, especially when you need to create, update, and delete resources. In this blog, I’ll walk you through how I resolved synchronization issues in my Locust tests for managing OTP rules.	8	https://s3.brilliant.com.bd/rafin_storage/locust.png	{locust,lock,apis,synchronization}
\.


--
-- Data for Name: education; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.education (id, user_id, year, degree, university, cgpa) FROM stdin;
77f4600b-4ef4-4206-86e1-ce0b9a67894d	312b9d52-d0a2-476c-81be-88566b7b600b	2018 - 2023	Bachelor in Computer Science and Engineering	Chittagong University of Engineering and Technology	CGPA 3.28 / 4.00
1a2724b5-12af-45f0-b56b-f9008034fbbf	312b9d52-d0a2-476c-81be-88566b7b600b	2017 - 2018	Higher Secondary School Certificate	Notre Dame College, Dhaka	CGPA 5.00 / 5.00
\.


--
-- Data for Name: experience; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.experience (id, user_id, year, "position", company, work_details) FROM stdin;
038f17b0-5cd9-4bdc-87f6-ae90913b364b	312b9d52-d0a2-476c-81be-88566b7b600b	Feb 2024 - Present	Software Engineer - Cloud Software (Backend)	Intercloud Limited	{"Developed RESTful APIs using Flask","Led a team of junior developers","Implemented CI/CD pipelines"}
6663f0cf-4f06-4ee6-8991-e39d8508050a	312b9d52-d0a2-476c-81be-88566b7b600b	Apr 2023 - Dec 2023	Trainee Software Engineer	Diligite Limited	{"Developed RESTful APIs using Flask","Led a team of junior developers","Implemented CI/CD pipelines"}
\.


--
-- Data for Name: social_media_links; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.social_media_links (id, user_id, facebook, linkedin, instagram, github) FROM stdin;
cc8897c7-88d3-44fb-a3e2-3c431db76ad4	312b9d52-d0a2-476c-81be-88566b7b600b	https://www.facebook.com/maruful.islam.10	https://www.linkedin.com/in/marufulislam	https://www.instagram.com/_raafin	https://github.com/Rafin000
\.


--
-- Data for Name: testimonials; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.testimonials (id, user_id, name, date, designation, company, content, image_link) FROM stdin;
4fb6f93c-2f4b-4cd3-a654-b886cc7152c9	312b9d52-d0a2-476c-81be-88566b7b600b	Shahed Mahbub	2024-08-19 06:43:28.292122	DevOps Manager	NexGen Cloud	Rafin is dedicated to his work. Professionally, he is continuously seeking out opportunities to grow and try new approaches .	https://s3.brilliant.com.bd/rafin_storage/shahed.jpeg
7bb7ee80-a907-4c57-abdb-be23b1d9e6df	312b9d52-d0a2-476c-81be-88566b7b600b	Mahadi Hasan Shuvo	2024-08-25 11:57:39.868868	Software Engineer	NexGen Cloud	Rafin is dedicated to his work. Professionally, he is continuously seeking out opportunities to grow and try new approaches . fsdfdsfds adasd ewrfd  wetrf wef	https://s3.brilliant.com.bd/rafin_storage/shuvo.jpeg
586f098c-c1f3-4ba1-bb72-80294cb68394	312b9d52-d0a2-476c-81be-88566b7b600b	Simon Islam	2024-08-22 06:34:12.038578	Backend Software Developer	NexGen Cloud	I am really enjoying working with Rafin at Intercloud Limited. Whenever he can, he is willing to assist others. I give him a thumbs-up!	https://s3.brilliant.com.bd/rafin_storage/simon.jpeg
d3832fb7-ddf4-486d-914b-a86b88dd6647	312b9d52-d0a2-476c-81be-88566b7b600b	Arefin Ahmed	2024-08-25 06:54:15.388955	Software Engineer	Intercloud Limited	Professionally, he is continuously seeking out opportunities to grow and try new approaches 	https://s3.brilliant.com.bd/rafin_storage/arefin.jpeg
26be9a29-da61-4099-8c8b-670c654a178f	312b9d52-d0a2-476c-81be-88566b7b600b	Simon Islam	2024-10-20 09:17:51.06509	Software Engineer	NexGen Cloud	I am really enjoying working with Rafin at Intercloud Limited. Whenever he can, he is willing to assist others. I give him a thumbs-up	https://s3.brilliant.com.bd/rafin_storage/simon.jpeg
\.


--
-- Data for Name: user_skills; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_skills (id, user_id, skill, icon_link) FROM stdin;
c5379353-58bd-48f9-9aec-13a3664a6f84	312b9d52-d0a2-476c-81be-88566b7b600b	C++	https://s3.brilliant.com.bd/rafin_storage/c%2B%2B.png
fce5c5c3-68cf-47ee-b255-5420f5c01c1f	312b9d52-d0a2-476c-81be-88566b7b600b	Flask	https://s3.brilliant.com.bd/rafin_storage/flask.png
a1bc2ae8-718e-4a07-8c95-a976729380ac	312b9d52-d0a2-476c-81be-88566b7b600b	Javascript	https://s3.brilliant.com.bd/rafin_storage/javascript.png
bef720db-3ca9-48a6-ad80-e0d410092496	312b9d52-d0a2-476c-81be-88566b7b600b	Kubernetes	https://s3.brilliant.com.bd/rafin_storage/kubernetes.png
b0bd4844-ac77-4d9f-a132-02f49defd77a	312b9d52-d0a2-476c-81be-88566b7b600b	NodeJS	https://s3.brilliant.com.bd/rafin_storage/nodejs.png
0dbfc94e-d5ae-4cfc-9d03-d8c6c1354aa3	312b9d52-d0a2-476c-81be-88566b7b600b	Python	https://s3.brilliant.com.bd/rafin_storage/python.png
e50c2c57-6016-4712-9ecf-d8ec184af67a	312b9d52-d0a2-476c-81be-88566b7b600b	React	https://s3.brilliant.com.bd/rafin_storage/react.png
ca036f75-71b8-4622-925f-7e3527edd609	312b9d52-d0a2-476c-81be-88566b7b600b	Docker	https://s3.brilliant.com.bd/rafin_storage/docker.png
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, full_name, designation, about, cv_link, profile_picture_link) FROM stdin;
312b9d52-d0a2-476c-81be-88566b7b600b	rafin_98	Md. Maruful Islam	Software Engineer	I am a professional Software Engineer who dreams about being a successful person in every aspect of life. Currently, I have been working as a full time software engineer at Intercloud Limited which is located in Dhaka, Bangladesh. Besides, during my leisure time, you can find me playing FIFA, watching TV-Series, Movies or hanging out with my friends. Whenever I get a chance to do something, I usually do not stop until I finish it.	https://s3.brilliant.com.bd/rafin_storage/cv.pdf	https://s3.brilliant.com.bd/rafin_storage/profile-img01.png
\.


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: blogs blogs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.blogs
    ADD CONSTRAINT blogs_pkey PRIMARY KEY (id);


--
-- Name: education education_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.education
    ADD CONSTRAINT education_id_key UNIQUE (id);


--
-- Name: education education_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.education
    ADD CONSTRAINT education_pkey PRIMARY KEY (id);


--
-- Name: experience experience_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.experience
    ADD CONSTRAINT experience_id_key UNIQUE (id);


--
-- Name: experience experience_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.experience
    ADD CONSTRAINT experience_pkey PRIMARY KEY (id);


--
-- Name: social_media_links social_media_links_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.social_media_links
    ADD CONSTRAINT social_media_links_pkey PRIMARY KEY (id);


--
-- Name: testimonials testimonials_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.testimonials
    ADD CONSTRAINT testimonials_pkey PRIMARY KEY (id);


--
-- Name: user_skills user_skills_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_skills
    ADD CONSTRAINT user_skills_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: education education_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.education
    ADD CONSTRAINT education_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: experience experience_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.experience
    ADD CONSTRAINT experience_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: social_media_links social_media_links_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.social_media_links
    ADD CONSTRAINT social_media_links_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: testimonials testimonials_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.testimonials
    ADD CONSTRAINT testimonials_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: user_skills user_skills_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_skills
    ADD CONSTRAINT user_skills_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

