-- ============================================
-- Run this in your Supabase SQL Editor
-- Adds all new hospital profile fields + storage bucket
-- ============================================

-- 1. Add new columns to hospitals table
ALTER TABLE public.hospitals ADD COLUMN IF NOT EXISTS tagline text;
ALTER TABLE public.hospitals ADD COLUMN IF NOT EXISTS established_year integer;
ALTER TABLE public.hospitals ADD COLUMN IF NOT EXISTS total_beds integer;
ALTER TABLE public.hospitals ADD COLUMN IF NOT EXISTS patients_per_year text;
ALTER TABLE public.hospitals ADD COLUMN IF NOT EXISTS hospital_type text DEFAULT 'Multi Speciality';
ALTER TABLE public.hospitals ADD COLUMN IF NOT EXISTS phone text;
ALTER TABLE public.hospitals ADD COLUMN IF NOT EXISTS emergency_phone text;
ALTER TABLE public.hospitals ADD COLUMN IF NOT EXISTS city text;
ALTER TABLE public.hospitals ADD COLUMN IF NOT EXISTS state text;
ALTER TABLE public.hospitals ADD COLUMN IF NOT EXISTS pin_code text;
ALTER TABLE public.hospitals ADD COLUMN IF NOT EXISTS google_maps_location text;
ALTER TABLE public.hospitals ADD COLUMN IF NOT EXISTS services text[] DEFAULT '{}';
ALTER TABLE public.hospitals ADD COLUMN IF NOT EXISTS gallery_images text[] DEFAULT '{}';
ALTER TABLE public.hospitals ADD COLUMN IF NOT EXISTS equipment_list jsonb DEFAULT '[]';

-- 2. Create storage bucket for hospital images
INSERT INTO storage.buckets (id, name, public) 
VALUES ('hospital-images', 'hospital-images', true)
ON CONFLICT (id) DO NOTHING;

-- 3. Storage Policies for hospital-images bucket
-- Drop existing policies to avoid errors on re-run
DROP POLICY IF EXISTS "Authenticated users can upload hospital images" ON storage.objects;
DROP POLICY IF EXISTS "Public can view hospital images" ON storage.objects;
DROP POLICY IF EXISTS "Authenticated users can update hospital images" ON storage.objects;
DROP POLICY IF EXISTS "Authenticated users can delete hospital images" ON storage.objects;

-- Re-create policies
CREATE POLICY "Authenticated users can upload hospital images"
ON storage.objects FOR INSERT
TO authenticated
WITH CHECK (bucket_id = 'hospital-images');

CREATE POLICY "Public can view hospital images"
ON storage.objects FOR SELECT
TO public
USING (bucket_id = 'hospital-images');

CREATE POLICY "Authenticated users can update hospital images"
ON storage.objects FOR UPDATE
TO authenticated
USING (bucket_id = 'hospital-images');

CREATE POLICY "Authenticated users can delete hospital images"
ON storage.objects FOR DELETE
TO authenticated
USING (bucket_id = 'hospital-images');
