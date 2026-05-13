/**
 * WhatsApp Service (Production Mode)
 * Sends custom templates with variables (Doctor, Token, Status).
 */

const WhatsAppService = {
    async sendMessage(templateName, to, variables = []) {
        let cleanTo = to.replace(/\D/g, '');
        if (cleanTo.length === 10) cleanTo = '91' + cleanTo;

        const proxyUrl = "https://corsproxy.io/?";
        const targetUrl = "https://graph.facebook.com/v20.0/1074880385711833/messages";
        const finalUrl = proxyUrl + encodeURIComponent(targetUrl);
        const token = "EAALAGWdyDagBRUTSZAsAljKuZBlZCv6SetWCqKXEHnOAMHhbnl6dyVFxFJKHJsBbb4z9qxqxACNbvjDKCrvgA1dq0akrkZC0n1dd2TC5hXoLsrZB0mGWZBnZBLbhP03KsxmNTyXzmUn0sX6aQW6sHLgpF24P303L5NmUSoF6ZAcBcUMFKepQtZCq5TlTRPCgZAAYQoOFIvgP4PsWhXnWi8YLkJm8X7ZAe5LG2RcmpxYG1ugQ0IJeMx8kWVHCLHJ8O8DtdEaYFybwj0POMgwwzjB8W0t";

        // Map variables to Meta format
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
                console.log(`SUCCESS! Template ${templateName} sent.`);
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
