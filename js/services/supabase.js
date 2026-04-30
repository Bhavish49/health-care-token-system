/**
 * Supabase Client Initialization
 * 
 * Replace the placeholders below with your project-specific credentials.
 * You can find these in your Supabase Project Settings > API.
 */

const SUPABASE_URL = 'https://tmebyxlflvljofdvptkr.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRtZWJ5eGxmbHZsam9mZHZwdGtyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY4OTM4MTQsImV4cCI6MjA5MjQ2OTgxNH0.gqW3c2ErgpOJB0rvFP4H7t2oa23DQ_yHCGUqAE3sMCo';

if (SUPABASE_URL.includes('YOUR_') || SUPABASE_ANON_KEY.includes('YOUR_')) {
    console.error('Supabase configuration missing! Please add your URL and Anon Key in js/services/supabase.js');
}

window.supabaseClient = supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
