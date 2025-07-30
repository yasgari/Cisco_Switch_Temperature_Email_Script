from netmiko import ConnectHandler
import pandas as pd
import datetime
import time
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_pdf_report(text_content, pdf_filename):
    """
    Convert text content to PDF format using reportlab
    """
    try:
        logger.info(f"Creating PDF report: {pdf_filename}")
        
        # Create PDF document
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        # Get styles
        styles = getSampleStyleSheet()
        
        # Create custom style for preformatted text
        code_style = ParagraphStyle(
            'Code',
            parent=styles['Normal'],
            fontName='Courier',
            fontSize=8,
            spaceAfter=12,
            leftIndent=0,
            rightIndent=0
        )
        
        # Build story for PDF
        story = []
        
        # Add title
        title_style = styles['Title']
        title = Paragraph("Cisco Switch Temperature Monitoring Report", title_style)
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Split content into sections and add to PDF
        sections = text_content.split('\n --- Output of')
        
        for i, section in enumerate(sections):
            if i == 0:
                # First section contains the start time
                story.append(Paragraph(section.strip(), styles['Normal']))
                story.append(Spacer(1, 12))
            else:
                # Restore the split delimiter and format as code
                section_content = " --- Output of" + section
                # Split into lines and create preformatted text
                lines = section_content.split('\n')
                for line in lines:
                    if line.strip():
                        story.append(Preformatted(line, code_style))
                story.append(Spacer(1, 12))
        
        # Build PDF
        doc.build(story)
        logger.info(f"PDF report created successfully: {pdf_filename}")
        return True
        
    except Exception as e:
        logger.error(f"Error creating PDF report: {str(e)}")
        return False

def send_email_with_attachment(pdf_filename, text_filename, timestamp):
    """
    Send email with PDF attachment
    """
    try:
        # Email configuration from environment variables
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', '587'))
        sender_email = os.getenv('SENDER_EMAIL', 'sender@example.com')
        sender_password = os.getenv('SENDER_PASSWORD', 'password')
        recipient_email = os.getenv('RECIPIENT_EMAIL', 'recipient@example.com')
        
        logger.info(f"Preparing to send email to: {recipient_email}")
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = f"Cisco switch device temperature update {timestamp}"
        
        # Email body
        body = f"""
        Dear Network Administrator,
        
        Please find attached the Cisco switch temperature monitoring report generated on {timestamp}.
        
        This automated report contains temperature readings from all monitored network switches.
        
        Best regards,
        Network Monitoring System
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach PDF file
        if os.path.exists(pdf_filename):
            with open(pdf_filename, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {os.path.basename(pdf_filename)}'
                )
                msg.attach(part)
                logger.info(f"PDF attachment added: {pdf_filename}")
        
        # Attach text file as backup
        if os.path.exists(text_filename):
            with open(text_filename, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {os.path.basename(text_filename)}'
                )
                msg.attach(part)
                logger.info(f"Text backup attachment added: {text_filename}")
        
        # Send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        
        logger.info(f"Email sent successfully to {recipient_email}")
        return True
        
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        return False

def cleanup_files(files_to_remove):
    """
    Clean up temporary files after email sending
    """
    for file_path in files_to_remove:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Cleaned up file: {file_path}")
        except Exception as e:
            logger.warning(f"Could not remove file {file_path}: {str(e)}")

def main():
    """
    Main function to execute the enhanced temperature monitoring script
    """
    ts = time.time()
    
    # Specify the path to your Excel file
    excel_file_path = 'switchFile.xlsx'
    
    try:
        # Check if Excel file exists
        if not os.path.exists(excel_file_path):
            logger.error(f"Excel file not found: {excel_file_path}")
            return
        
        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(excel_file_path, engine='openpyxl')
        
        # Convert the DataFrame to a list of dictionaries
        list_of_switches = df.to_dict(orient='records')
        
        logger.info(f"Loaded {len(list_of_switches)} switches from Excel file")
        
        # Commands to execute
        commands = [
            'show env temp'
        ]
        
        time_str = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        timestamp_safe = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M%S')
        outputsVar = f'Start Script at Time: {time_str}\n'
        
        # Loop through all switches in the given excel spreadsheet
        for switch in list_of_switches:
            try:
                logger.info(f"Connecting to switch: {switch.get('host', 'Unknown')}")
                
                # Establish SSH connection
                net_connect = ConnectHandler(**switch)
                
                for command in commands:
                    logger.info(f"Executing '{command}' on {switch['host']}...")
                    output = net_connect.send_command(command)
                    hostname = net_connect.send_command('sh run | i host').split()[1]
                    outputsVar += f'\n --- Output of {command} on {hostname} \n{output}\n\n'
        
            except Exception as e:
                logger.error(f"Error processing switch {switch.get('host', 'Unknown')}: {str(e)}")
                outputsVar += f'\n --- Error connecting to {switch.get("host", "Unknown")}: {str(e)}\n\n'
        
            finally:
                # Disconnect from the switch
                if 'net_connect' in locals() and net_connect.is_alive():
                    net_connect.disconnect()
        
        # Generate output files
        text_filename = f'device_output_{timestamp_safe}.txt'
        pdf_filename = f'device_temperature_report_{timestamp_safe}.pdf'
        
        # Write text output
        logger.info(f"Writing text output to: {text_filename}")
        with open(text_filename, 'w') as f:
            f.write(outputsVar)
        
        # Create PDF report
        pdf_success = create_pdf_report(outputsVar, pdf_filename)
        
        if pdf_success:
            # Send email with attachments
            email_success = send_email_with_attachment(pdf_filename, text_filename, time_str)
            
            if email_success:
                logger.info("Temperature monitoring report sent successfully")
                
                # Clean up files if email was sent successfully (optional)
                cleanup_option = os.getenv('CLEANUP_FILES_AFTER_EMAIL', 'false').lower()
                if cleanup_option == 'true':
                    cleanup_files([pdf_filename, text_filename])
                else:
                    logger.info(f"Files preserved: {text_filename}, {pdf_filename}")
            else:
                logger.error("Failed to send email - files preserved for manual sending")
        else:
            logger.error("Failed to create PDF report")
            
            # Try to send just the text file if PDF creation failed
            email_success = send_email_with_attachment(None, text_filename, time_str)
            if email_success:
                logger.info("Text report sent successfully (PDF creation failed)")
    
    except Exception as e:
        logger.error(f"Critical error in main execution: {str(e)}")

if __name__ == "__main__":
    main()
