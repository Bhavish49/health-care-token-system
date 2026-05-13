-- WARNING: This schema is for context only and is not meant to be run.
-- Table order and constraints may not be valid for execution.

CREATE TABLE public.hospitals (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  name text NOT NULL,
  address text,
  admin_id uuid,
  hospital_email text,
  created_at timestamp with time zone DEFAULT timezone('utc'::text, now()),
  photo_url text,
  description text,
  specialty text,
  staff_count integer,
  onboarding_complete boolean DEFAULT false,
  tagline text,
  established_year integer,
  total_beds integer,
  patients_per_year text,
  hospital_type text DEFAULT 'Multi Speciality'::text,
  phone text,
  emergency_phone text,
  city text,
  state text,
  pin_code text,
  google_maps_location text,
  services text[] DEFAULT '{}'::text[],
  about_image text,
  infra_image text,
  equipment_image text,
  exterior_image text,
  equipment_list jsonb DEFAULT '[]'::jsonb,
  gallery_images text[] DEFAULT '{}'::text[],
  join_code text UNIQUE,
  CONSTRAINT hospitals_pkey PRIMARY KEY (id),
  CONSTRAINT hospitals_admin_id_fkey FOREIGN KEY (admin_id) REFERENCES auth.users(id)
);

CREATE TABLE public.profiles (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  name text,
  specialization text,
  age integer,
  experience integer,
  diseases text,
  description text,
  photo_url text,
  updated_at timestamp with time zone DEFAULT timezone('utc'::text, now()),
  hospital_id uuid,
  email text,
  category text,
  room_number text,
  qualification text,
  onboarding_complete boolean DEFAULT false,
  CONSTRAINT profiles_pkey PRIMARY KEY (id),
  CONSTRAINT profiles_hospital_id_fkey FOREIGN KEY (hospital_id) REFERENCES public.hospitals(id)
);

CREATE TABLE public.tokens (
  id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  doctor_id uuid NOT NULL,
  num integer NOT NULL,
  patient_name text NOT NULL,
  patient_age integer,
  patient_phone text,
  status text DEFAULT 'pending'::text,
  created_at timestamp with time zone DEFAULT timezone('utc'::text, now()),
  patient_id uuid,
  CONSTRAINT tokens_pkey PRIMARY KEY (id),
  CONSTRAINT tokens_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES public.profiles(id),
  CONSTRAINT tokens_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES auth.users(id)
);
