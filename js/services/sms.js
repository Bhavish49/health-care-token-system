const SMSService = {
    async sendSMS(to, text) {
        let mobile = to.replace(/\D/g, '');
        if (mobile.length > 10) mobile = mobile.slice(-10);

        if (mobile.length !== 10) {
            console.warn("SMSService: Invalid mobile number →", to);
            return false;
        }

        console.log(`Sending SMS to ${mobile} via Supabase RPC...`);

        try {
            const { data, error } = await window.supabaseClient
                .rpc('send_sms_rpc', {
                    phone: mobile,
                    message: text
                });

            if (error) {
                console.error("SMS RPC error:", error.message);
                return false;
            }

            console.log("SMS dispatched via RPC:", data);
            return true;

        } catch (err) {
            console.error("SMS request error:", err.message);
            return false;
        }
    },

    async notifyTokenBooked(phone, patientName, tokenNum, doctorName, hospName) {
        return true;
    },

    async notifyYourTurn(phone, patientName, tokenNum, doctorName) {
        const msg =
            `Hi ${patientName}, Token #${tokenNum} — it is YOUR TURN now! ` +
            `Please proceed to ${doctorName}'s cabin. - MediQ`;
        return this.sendSMS(phone, msg);
    },

    async notifyQueueUpdate(phone, patientName, tokenNum, currentNum, ahead) {
        const msg =
            `Hi ${patientName} (Token #${tokenNum}), currently serving #${currentNum}. ` +
            `${ahead > 0 ? `Approx. ${ahead} patient(s) ahead of you.` : `You are next!`} - MediQ`;
        return this.sendSMS(phone, msg);
    },

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

window.WhatsAppService = SMSService;
window.SMSService = SMSService;
