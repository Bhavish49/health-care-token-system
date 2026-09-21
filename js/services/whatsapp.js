const WhatsAppService = {
    async sendMessage(templateName, to, variables = []) {
        let cleanTo = to.replace(/\D/g, '');
        if (cleanTo.length === 10) cleanTo = '91' + cleanTo;

        const phoneId = window.WHATSAPP_PHONE_ID || 'YOUR_PHONE_NUMBER_ID';
        const token = window.WHATSAPP_TOKEN || 'YOUR_META_ACCESS_TOKEN';

        if (token === 'YOUR_META_ACCESS_TOKEN' || phoneId === 'YOUR_PHONE_NUMBER_ID') {
            console.warn("WhatsAppService: Meta credentials missing!");
            return false;
        }

        const proxyUrl = "https://corsproxy.io/?";
        const targetUrl = `https://graph.facebook.com/v20.0/${phoneId}/messages`;
        const finalUrl = proxyUrl + encodeURIComponent(targetUrl);

        if (!Array.isArray(variables)) variables = [];
        const templateData = {
            name: templateName,
            language: { code: "en_US" }
        };

        if (variables.length > 0) {
            templateData.components = [{
                type: "body",
                parameters: variables.map(v => ({ type: "text", text: String(v) }))
            }];
        }

        try {
            const response = await fetch(finalUrl, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    messaging_product: "whatsapp",
                    to: cleanTo,
                    type: "template",
                    template: templateData
                })
            });

            const data = await response.json();
            if (response.ok) {
                console.log(`Template ${templateName} sent successfully.`);
                return true;
            } else {
                console.error("Meta API Error:", data);
                return false;
            }
        } catch (error) {
            console.error("Proxy Error:", error);
            return false;
        }
    }
};

window.WhatsAppService = WhatsAppService;
