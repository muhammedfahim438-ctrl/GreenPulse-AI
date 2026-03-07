# ══════════════════════════════
# Email Alert Service
# ══════════════════════════════

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')


def send_email(to_email, subject, body):
    try:
        msg            = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From']    = EMAIL_ADDRESS
        msg['To']      = to_email

        html_body = f"""
        <html>
        <body style="
            font-family: Arial, sans-serif;
            background: #f4f7f5;
            padding: 20px;
        ">
            <div style="
                max-width: 600px;
                margin: 0 auto;
                background: white;
                border-radius: 16px;
                overflow: hidden;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            ">
                <div style="
                    background: #0d3320;
                    padding: 30px;
                    text-align: center;
                ">
                    <h1 style="color: #2ecc71; margin: 0;">
                        🌿 GreenPulse AI
                    </h1>
                    <p style="
                        color: rgba(255,255,255,0.6);
                        margin: 8px 0 0;
                        font-size: 14px;
                    ">
                        Smart Farming Alert System
                    </p>
                </div>

                <div style="padding: 30px;">
                    <h2 style="color: #0d3320;">
                        {subject}
                    </h2>
                    <p style="
                        color: #4a6558;
                        font-size: 15px;
                        line-height: 1.7;
                    ">
                        {body}
                    </p>
                </div>

                <div style="
                    background: #f4f7f5;
                    padding: 20px;
                    text-align: center;
                    font-size: 12px;
                    color: #888;
                ">
                    GreenPulse AI — Built for farmers 🌱
                </div>
            </div>
        </body>
        </html>
        """

        msg.attach(MIMEText(html_body, 'html'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())

        print(f'Email sent to {to_email}')
        return True

    except Exception as e:
        print(f'Email error: {e}')
        return False


def send_weather_alert(to_email, farmer_name, alert_type, details):

    subjects = {
        'high_temp':  '🌡️ High Temperature Alert — GreenPulse AI',
        'heavy_rain': '🌧️ Heavy Rain Warning — GreenPulse AI',
        'high_risk':  '⚠️ High Crop Risk Alert — GreenPulse AI',
        'disease':    '🦠 Disease Risk Warning — GreenPulse AI'
    }

    bodies = {
        'high_temp': f"""
            Dear {farmer_name},<br><br>
            High temperature detected on your farm.<br><br>
            <strong>Temperature:</strong>
            {details.get('temperature', 'N/A')}°C<br>
            <strong>Action:</strong>
            Increase irrigation immediately! 🌾
        """,
        'heavy_rain': f"""
            Dear {farmer_name},<br><br>
            Heavy rainfall forecast for your area.<br><br>
            <strong>Expected Rainfall:</strong>
            {details.get('rainfall', 'N/A')} mm<br>
            <strong>Action:</strong>
            Ensure proper drainage in your fields! 🌧️
        """,
        'high_risk': f"""
            Dear {farmer_name},<br><br>
            Your Crop Risk Score has reached high level.<br><br>
            <strong>Risk Score:</strong>
            {details.get('risk_score', 'N/A')}%<br>
            <strong>Action:</strong>
            Monitor your crops closely! ⚠️
        """,
        'disease': f"""
            Dear {farmer_name},<br><br>
            Disease detected in your crop image.<br><br>
            <strong>Disease:</strong>
            {details.get('disease', 'N/A')}<br>
            <strong>Confidence:</strong>
            {details.get('confidence', 'N/A')}%<br>
            <strong>Action:</strong>
            {details.get('treatment', 'Consult an expert.')} 🦠
        """
    }

    subject = subjects.get(alert_type, '🔔 Farm Alert — GreenPulse AI')
    body    = bodies.get(alert_type, '')

    return send_email(to_email, subject, body)