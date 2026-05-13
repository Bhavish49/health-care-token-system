/**
 * EmailService — powered by EmailJS
 * Sends token notifications to patients via Email.
 * 
 * Free Tier: 200 emails / month.
 */

const EmailService = {
    // You will get these from emailjs.com
    SERVICE_ID: 'service_ljrek8r',
    TEMPLATE_ID: 'template_p35ueyn',
    PUBLIC_KEY: 'fURKTIgFAbApicLjY',

    init() {
        if (this.PUBLIC_KEY !== 'YOUR_PUBLIC_KEY') {
            emailjs.init(this.PUBLIC_KEY);
        }
    },

    /**
     * Send email notification
     */
    async sendEmail(toEmail, patientName, tokenNum, doctorName, hospName) {
        if (this.PUBLIC_KEY === 'YOUR_PUBLIC_KEY') {
            console.warn("EmailService: Please set your EmailJS credentials!");
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

// Initialize
EmailService.init();

// Expose globally as a drop-in replacement or addition
window.EmailService = EmailService;
// We also alias it to window.SMSService to avoid breaking existing code immediately
window.SMSService = {
    async notifyTokenBooked(email, name, nextNum, docName, hospName) {
        return EmailService.sendEmail(email, name, nextNum, docName, hospName);
    }
};
