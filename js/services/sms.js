/**
 * SMSService — powered by Fast2SMS via Supabase pg_net
 * 
 * Token booking SMS: Handled AUTOMATICALLY by database trigger
 *   → When a token is inserted, the trigger calls Fast2SMS via pg_net
 *   → No frontend code needed for booking SMS!
 *
 * Queue update SMS: Called via Supabase RPC from doctor dashboard
 *   → Uses supabase.rpc('send_sms_rpc', { phone, message })
 */

const SMSService = {

    /**
     * Send SMS via Supabase RPC → pg_net → Fast2SMS
     * Used by doctor dashboard for queue updates.
     */
    async sendSMS(to, text) {
        let mobile = to.replace(/\D/g, '');
        if (mobile.length > 10) mobile = mobile.slice(-10);

        if (mobile.length !== 10) {
            console.warn("SMSService: Invalid mobile number →", to);
            return false;
        }

        console.log(`📤 Sending SMS to ${mobile} via Supabase RPC...`);

        try {
            const { data, error } = await window.supabaseClient
                .rpc('send_sms_rpc', {
                    phone: mobile,
                    message: text
                });

            if (error) {
                console.error("❌ SMS RPC error:", error.message);
                return false;
            }

            console.log("✅ SMS dispatched via RPC:", data);
            return true;

        } catch (err) {
            console.error("❌ SMS request error:", err.message);
            return false;
        }
    },

    // ─── Convenience wrappers ────────────────────────────────────────────────

    /**
     * Notify patient about their new token (on booking)
     * NOTE: This is now handled by the database trigger automatically.
     * This function is kept for backward compatibility but is a no-op.
     */
    async notifyTokenBooked(phone, patientName, tokenNum, doctorName, hospName) {
        console.log(`📨 Token booking SMS for ${patientName} (#${tokenNum}) — handled by database trigger`);
        return true; // Trigger handles it
    },

    /**
     * Notify the patient that it is NOW their turn
     */
    async notifyYourTurn(phone, patientName, tokenNum, doctorName) {
        const msg =
            `Hi ${patientName}, Token #${tokenNum} — it is YOUR TURN now! ` +
            `Please proceed to ${doctorName}'s cabin. - MediQ`;
        return this.sendSMS(phone, msg);
    },

    /**
     * Notify a waiting patient about updated queue position
     */
    async notifyQueueUpdate(phone, patientName, tokenNum, currentNum, ahead) {
        const msg =
            `Hi ${patientName} (Token #${tokenNum}), currently serving #${currentNum}. ` +
            `${ahead > 0 ? `Approx. ${ahead} patient(s) ahead of you.` : `You are next!`} - MediQ`;
        return this.sendSMS(phone, msg);
    },

    /**
     * Legacy-compatible wrapper (replaces WhatsAppService.sendMessage calls)
     */
    async sendMessage(templateName, to, variables = []) {
        let msg = "";
        if (templateName === "queue_status" && variables.length >= 4) {
            const [doctorName, currentNum, yourNum, ahead] = variables;
            if (ahead === 0) {
                msg = `Hi! Token #${yourNum} — it is YOUR TURN now! Please proceed to Dr. ${doctorName}'s cabin. - MediQ`;
            } else {
                msg = `Hi! (Token #${yourNum}) Currently serving #${currentNum}. ` +
                    `${ahead} patient(s) ahead of you. Dr. ${doctorName}. - MediQ`;
            }
        } else {
            msg = `MediQ: Your token update — ${variables.join(', ')}`;
        }
        return this.sendSMS(to, msg);
    }
};

// Expose globally
window.WhatsAppService = SMSService;
window.SMSService = SMSService;
