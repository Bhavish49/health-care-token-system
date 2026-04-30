-- 1. Hospitals Table
-- Stores metadata about the medical facility
CREATE TABLE IF NOT EXISTS public.hospitals (
  id uuid DEFAULT gen_random_uuid() NOT NULL,
  name text NOT NULL,
  address text,
  admin_id uuid NOT NULL,
  hospital_email text,
  photo_url text,           -- For hospital banner
  description text,         -- For facility bio
  specialty text,           -- Main specialty
  staff_count integer,      -- Number of doctors
  onboarding_complete boolean DEFAULT false,
  created_at timestamp with time zone DEFAULT timezone('utc'::text, now()),
  CONSTRAINT hospitals_pkey PRIMARY KEY (id),
  CONSTRAINT hospitals_admin_id_fkey FOREIGN KEY (admin_id) REFERENCES auth.users(id) ON DELETE CASCADE
);

-- 2. Doctor Profiles Table
-- Stores metadata about medical professionals linked to a hospital
CREATE TABLE IF NOT EXISTS public.profiles (
  id uuid NOT NULL,
  name text,
  email text,
  specialization text,
  age integer,
  experience integer,
  diseases text,            -- Things they treat
  description text,         -- Professional bio
  photo_url text,           -- Profile picture
  hospital_id uuid,         -- LINK TO THE HOSPITAL
  category text,            -- e.g. Cardiology, General
  room_number text,
  qualification text,
  onboarding_complete boolean DEFAULT false,
  updated_at timestamp with time zone DEFAULT timezone('utc'::text, now()),
  CONSTRAINT profiles_pkey PRIMARY KEY (id),
  CONSTRAINT profiles_id_fkey FOREIGN KEY (id) REFERENCES auth.users(id) ON DELETE CASCADE,
  CONSTRAINT profiles_hospital_id_fkey FOREIGN KEY (hospital_id) REFERENCES public.hospitals(id) ON DELETE SET NULL
);

-- 3. Tokens Table
-- Manages the digital queue
CREATE TABLE IF NOT EXISTS public.tokens (
  id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  doctor_id uuid NOT NULL,
  num integer NOT NULL,
  patient_name text NOT NULL,
  patient_age integer,
  patient_phone text,
  status text DEFAULT 'pending'::text,
  created_at timestamp with time zone DEFAULT timezone('utc'::text, now()),
  CONSTRAINT tokens_pkey PRIMARY KEY (id),
  CONSTRAINT tokens_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES public.profiles(id) ON DELETE CASCADE
);
