import { serve } from "https://deno.land/std@0.168.0/http/server.ts"

// Replace with your actual Fast2SMS API Authorization key
const FAST2SMS_API_KEY = Deno.env.get("FAST2SMS_API_KEY") ?? "dNcMsuFAX7YIrvg6jopimEk3y5JLHlwbRBtVUqaZDfnh2QKSGCtv60GRpCiKWN4UXmAbkuJMjgxSIlqn";

const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST',
    'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};

serve(async (req) => {
    if (req.method === 'OPTIONS') {
        return new Response('ok', { headers: corsHeaders });
    }

    try {
        const { to, message } = await req.json();

        if (!to || !message) {
            return new Response(
                JSON.stringify({ error: "'to' and 'message' fields are required." }),
                { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 400 }
            );
        }

        // Sanitize phone: keep only digits, use last 10 digits
        const mobile = to.replace(/\D/g, '').slice(-10);

        if (mobile.length !== 10) {
            return new Response(
                JSON.stringify({ error: "Invalid Indian mobile number: " + to }),
                { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 400 }
            );
        }

        // Fast2SMS Bulk V2 API — Quick SMS route (no DLT needed for testing)
        const response = await fetch("https://www.fast2sms.com/dev/bulkV2", {
            method: "POST",
            headers: {
                "authorization": FAST2SMS_API_KEY,
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: new URLSearchParams({
                route:    "q",         // Quick SMS
                message:  message,
                language: "english",
                flash:    "0",
                numbers:  mobile,
            }).toString(),
        });

        const data = await response.json();

        return new Response(JSON.stringify(data), {
            headers: { ...corsHeaders, 'Content-Type': 'application/json' },
            status: data.return === true ? 200 : 400,
        });

    } catch (error) {
        return new Response(
            JSON.stringify({ error: error.message }),
            { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 500 }
        );
    }
});
