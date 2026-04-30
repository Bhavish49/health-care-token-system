// Global App Initialization
document.addEventListener('DOMContentLoaded', () => {
    console.log('MediQ initialized');
    
    // Check if Supabase is connected
    if (window.supabaseClient) {
        console.log('Supabase service connected');
    }
    
    // Add global interactions here
});
