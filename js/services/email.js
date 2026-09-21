const EmailService = {
    SERVICE_ID: 'service_ljrek8r',
    TEMPLATE_ID: 'template_p35ueyn',
    PUBLIC_KEY: 'fURKTIgFAbApicLjY',

    init() {
        if (this.PUBLIC_KEY) {
            emailjs.init(this.PUBLIC_KEY);
        }
    },

    async sendEmail(toEmail, patientName, tokenNum, doctorName, hospName) {
        if (!this.PUBLIC_KEY) {
            console.warn("EmailService: Credentials missing!");
            return false;
        }

        const templateParams = {
            to_email: toEmail,
            patient_name: patientName,
            token_number: tokenNum,
            doctor_name: doctorName,
            hospital_name: hospName,
            reply_to: 'support@mediq.com'
        };

        try {
            const response = await emailjs.send(this.SERVICE_ID, this.TEMPLATE_ID, templateParams);
            console.log('✅ Email sent successfully!', response.status, response.text);
            return true;
        } catch (error) {
            console.error('❌ Email failed to send:', error);
            return false;
        }
    }
};

EmailService.init();

window.EmailService = EmailService;
window.SMSService = {
    async notifyTokenBooked(email, name, nextNum, docName, hospName) {
        return EmailService.sendEmail(email, name, nextNum, docName, hospName);
    }
};
