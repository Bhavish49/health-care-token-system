-- Run these commands in your Supabase SQL Editor to update your existing tables

-- 1. Update Hospitals table
ALTER TABLE public.hospitals 
ADD COLUMN IF NOT EXISTS photo_url text,
ADD COLUMN IF NOT EXISTS description text,
ADD COLUMN IF NOT EXISTS specialty text,
ADD COLUMN IF NOT EXISTS staff_count integer,
ADD COLUMN IF NOT EXISTS onboarding_complete boolean DEFAULT false;

-- 2. Update Profiles table
ALTER TABLE public.profiles 
ADD COLUMN IF NOT EXISTS onboarding_complete boolean DEFAULT false;

-- 3. Note: Ensure your tokens table matches the logic
-- (The schema you provided already looks compatible with the token logic)
