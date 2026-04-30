-- Run these commands in your Supabase SQL Editor to fix registration and access issues.

-- Enable RLS on all tables
ALTER TABLE public.hospitals ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.tokens ENABLE ROW LEVEL SECURITY;

-- 1. HOSPITALS POLICIES
-- Anyone can view hospitals (for patient search)
DROP POLICY IF EXISTS "Public hospitals are viewable by everyone" ON public.hospitals;
CREATE POLICY "Public hospitals are viewable by everyone" 
ON public.hospitals FOR SELECT USING (true);

-- Authenticated users can create a hospital (Registration)
DROP POLICY IF EXISTS "Users can create their own hospital" ON public.hospitals;
CREATE POLICY "Users can create their own hospital" 
ON public.hospitals FOR INSERT 
TO authenticated 
WITH CHECK (auth.uid() = admin_id);

-- Only the admin can update their own hospital
DROP POLICY IF EXISTS "Admins can update their own hospital" ON public.hospitals;
CREATE POLICY "Admins can update their own hospital" 
ON public.hospitals FOR UPDATE 
TO authenticated 
USING (auth.uid() = admin_id);

-- 2. PROFILES (Doctors) POLICIES
-- Anyone can view doctor profiles (for patient search)
DROP POLICY IF EXISTS "Public profiles are viewable by everyone" ON public.profiles;
CREATE POLICY "Public profiles are viewable by everyone" 
ON public.profiles FOR SELECT USING (true);

-- Authenticated users can create their own profile (Doctor Registration)
DROP POLICY IF EXISTS "Users can create their own profile" ON public.profiles;
CREATE POLICY "Users can create their own profile" 
ON public.profiles FOR INSERT 
TO authenticated 
WITH CHECK (auth.uid() = id);

-- Users can update their own profile
DROP POLICY IF EXISTS "Users can update their own profile" ON public.profiles;
CREATE POLICY "Users can update their own profile" 
ON public.profiles FOR UPDATE 
TO authenticated 
USING (auth.uid() = id);

-- 3. TOKENS POLICIES
-- Anyone can insert a token (Patient booking)
DROP POLICY IF EXISTS "Anyone can book a token" ON public.tokens;
CREATE POLICY "Anyone can book a token" 
ON public.tokens FOR INSERT WITH CHECK (true);

-- Anyone can view tokens (to see current queue status)
DROP POLICY IF EXISTS "Public tokens are viewable by everyone" ON public.tokens;
CREATE POLICY "Public tokens are viewable by everyone" 
ON public.tokens FOR SELECT USING (true);

-- Doctors can update status of their tokens
DROP POLICY IF EXISTS "Doctors can update their token status" ON public.tokens;
CREATE POLICY "Doctors can update their token status" 
ON public.tokens FOR UPDATE 
TO authenticated 
USING (auth.uid() = doctor_id);
