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

# Try to load .env file if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
    logger_config = logging.getLogger(__name__)
    logger_config.info("Loaded configuration from .env file")
except ImportError:
    # python-dotenv not installed, will use environment variables directly
    pass

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def analyze_output_for_alerts(text_content):
    """
    Analyze switch output for warning/critical conditions
    Returns categorized alerts with severity levels
    """
    warning_hosts = []
    critical_hosts = []
    warning_details = []
    critical_details = []
    
    sections = text_content.split('\n --- Output of')
    
    for section in sections[1:]:  # Skip first section (timestamp)
        lines = section.split('\n')
        hostname = "Unknown"
        has_warning = False
        has_critical = False
        
        # Extract hostname from first line
        if lines and 'on ' in lines[0]:
            hostname = lines[0].split(' on ')[-1].strip()
        
        # Check for warning/critical conditions
        for line in lines:
            line_lower = line.lower()
            if 'critical' in line_lower or 'catastrophic' in line_lower:
                has_critical = True
                critical_details.append(f"{hostname}: {line.strip()}")
            elif 'warning' in line_lower:
                has_warning = True
                warning_details.append(f"{hostname}: {line.strip()}")
        
        # Add to appropriate lists (critical takes precedence)
        if has_critical and hostname not in critical_hosts:
            critical_hosts.append(hostname)
        elif has_warning and hostname not in warning_hosts and hostname not in critical_hosts:
            warning_hosts.append(hostname)
    
    return warning_hosts, critical_hosts, warning_details, critical_details

def create_pdf_report(text_content, pdf_filename, warning_hosts=None, critical_hosts=None, warning_details=None, critical_details=None):
    """
    Convert text content to PDF format using reportlab with color-coded alerts
    """
    try:
        logger.info(f"Creating PDF report: {pdf_filename}")
        
        # Create PDF document
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        # Get styles
        styles = getSampleStyleSheet()
        
        # Create custom styles
        code_style = ParagraphStyle(
            'Code',
            parent=styles['Normal'],
            fontName='Courier',
            fontSize=8,
            spaceAfter=12,
            leftIndent=0,
            rightIndent=0
        )
        
        critical_header_style = ParagraphStyle(
            'CriticalHeader',
            parent=styles['Heading2'],
            textColor='red',
            fontSize=12,
            spaceAfter=6,
            spaceBefore=6
        )
        
        warning_header_style = ParagraphStyle(
            'WarningHeader',
            parent=styles['Heading2'],
            textColor='orange',
            fontSize=12,
            spaceAfter=6,
            spaceBefore=6
        )
        
        critical_detail_style = ParagraphStyle(
            'CriticalDetail',
            parent=styles['Normal'],
            textColor='red',
            fontSize=10,
            leftIndent=20,
            spaceAfter=3
        )
        
        warning_detail_style = ParagraphStyle(
            'WarningDetail',
            parent=styles['Normal'],
            textColor='orange',
            fontSize=10,
            leftIndent=20,
            spaceAfter=3
        )
        
        # Build story for PDF
        story = []
        
        # Add title
        title_style = styles['Title']
        title = Paragraph("Cisco Switch Temperature Monitoring Report", title_style)
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Add status message
        has_critical = critical_hosts and len(critical_hosts) > 0
        has_warnings = warning_hosts and len(warning_hosts) > 0
        
        # Always show "NO CRITICAL ALERTS AT THIS TIME" when there are no critical/catastrophic conditions
        if not has_critical:
            no_critical_style = ParagraphStyle(
                'NoCritical',
                parent=styles['Normal'],
                textColor='green',
                fontSize=14,
                alignment=1,  # Center alignment
                spaceBefore=6,
                spaceAfter=12,
                fontName='Helvetica-Bold'
            )
            story.append(Paragraph("✅ NO CRITICAL ALERTS AT THIS TIME", no_critical_style))
            story.append(Spacer(1, 12))
        
        # Add color-coded status based on conditions
        if not has_critical and not has_warnings:
            # All OK - green text already shown above
            pass
        elif has_warnings and not has_critical:
            # Show yellow/orange status when there are warnings but no critical alerts
            warning_status_style = ParagraphStyle(
                'WarningStatus',
                parent=styles['Normal'],
                textColor='orange',
                fontSize=14,
                alignment=1,  # Center alignment
                spaceBefore=6,
                spaceAfter=12,
                fontName='Helvetica-Bold'
            )
            story.append(Paragraph("⚠️ WARNING CONDITIONS DETECTED", warning_status_style))
            story.append(Spacer(1, 12))
        elif has_critical:
            # Show red status with switch names when there are critical alerts
            critical_status_style = ParagraphStyle(
                'CriticalStatus',
                parent=styles['Normal'],
                textColor='red',
                fontSize=14,
                alignment=1,  # Center alignment
                spaceBefore=6,
                spaceAfter=12,
                fontName='Helvetica-Bold'
            )
            critical_switches = ', '.join(critical_hosts)
            story.append(Paragraph(f"🚨 CRITICAL ALERTS: {critical_switches}", critical_status_style))
            story.append(Spacer(1, 12))
        
        # Add critical alerts first (if any)
        if has_critical:
            story.append(Paragraph("🚨 CRITICAL TEMPERATURE ALERTS", critical_header_style))
            story.append(Paragraph(f"Critical Switches: {', '.join(critical_hosts)}", critical_detail_style))
            story.append(Spacer(1, 6))
            
            if critical_details:
                story.append(Paragraph("Critical Alert Details:", styles['Heading3']))
                for detail in critical_details:
                    story.append(Paragraph(f"• {detail}", critical_detail_style))
            story.append(Spacer(1, 12))
        
        # Add warning alerts (if any)
        if has_warnings:
            story.append(Paragraph("⚠️ WARNING TEMPERATURE ALERTS", warning_header_style))
            story.append(Paragraph(f"Warning Switches: {', '.join(warning_hosts)}", warning_detail_style))
            story.append(Spacer(1, 6))
            
            if warning_details:
                story.append(Paragraph("Warning Alert Details:", styles['Heading3']))
                for detail in warning_details:
                    story.append(Paragraph(f"• {detail}", warning_detail_style))
            story.append(Spacer(1, 12))
        
        # Add separator if there were any alerts
        if has_critical or has_warnings:
            story.append(Spacer(1, 8))
            story.append(Paragraph("Detailed Temperature Report:", styles['Heading2']))
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
                        line_lower = line.lower()
                        # Color-code based on severity
                        if 'critical' in line_lower or 'catastrophic' in line_lower:
                            story.append(Paragraph(f"<font color='red'>{line}</font>", styles['Normal']))
                        elif 'warning' in line_lower:
                            story.append(Paragraph(f"<font color='orange'>{line}</font>", styles['Normal']))
                        else:
                            story.append(Preformatted(line, code_style))
                story.append(Spacer(1, 12))
        
        # Build PDF
        doc.build(story)
        logger.info(f"PDF report created successfully: {pdf_filename}")
        return True
        
    except Exception as e:
        logger.error(f"Error creating PDF report: {str(e)}")
        return False

def send_email_with_attachment(pdf_filename, text_filename, timestamp, warning_hosts=None, critical_hosts=None, warning_details=None, critical_details=None):
    """
    Send email with PDF attachment
    """
    try:
        # Email configuration from environment variables
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', '587'))
        sender_email = os.getenv('SENDER_EMAIL', 'sender@example.com')
        sender_password = os.getenv('SENDER_PASSWORD', 'password')
        recipient_emails_str = os.getenv('RECIPIENT_EMAIL', 'recipient@example.com')
        
        # Support multiple recipients - split by comma and clean up whitespace
        recipient_emails = [email.strip() for email in recipient_emails_str.split(',')]
        recipient_emails = [email for email in recipient_emails if email]  # Remove empty strings
        
        logger.info(f"Preparing to send email to: {', '.join(recipient_emails)}")
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = ', '.join(recipient_emails)
        
        # Modify subject based on alerts (critical takes precedence)
        all_alert_hosts = []
        if critical_hosts:
            all_alert_hosts.extend(critical_hosts)
        if warning_hosts:
            all_alert_hosts.extend(warning_hosts)
        
        if critical_hosts and len(critical_hosts) > 0:
            msg['Subject'] = f"🚨 CRITICAL ALERT: Cisco switch device temperature update {timestamp} - Critical issues on {', '.join(critical_hosts)}"
        elif warning_hosts and len(warning_hosts) > 0:
            msg['Subject'] = f"⚠️ WARNING: Cisco switch device temperature update {timestamp} - Warnings on {', '.join(warning_hosts)}"
        else:
            msg['Subject'] = f"Cisco switch device temperature update {timestamp}"
        
        # Email body with alert information
        if all_alert_hosts and len(all_alert_hosts) > 0:
            # Create alert summary
            alert_summary = ""
            if critical_details:
                alert_summary += "\n  CRITICAL ALERTS:\n"
                alert_summary += '\n'.join([f"    - {detail}" for detail in critical_details])
            if warning_details:
                alert_summary += "\n  WARNING ALERTS:\n"
                alert_summary += '\n'.join([f"    - {detail}" for detail in warning_details])
            
            urgency_level = "CRITICAL" if critical_hosts else "WARNING"
            body = f"""
        {'🚨 CRITICAL' if critical_hosts else '⚠️ WARNING'} TEMPERATURE ALERT DETECTED
        
        Dear Network Administrator,
        
        {urgency_level} ATTENTION REQUIRED: Temperature alerts have been detected on the following switches:
        Critical Issues: {', '.join(critical_hosts) if critical_hosts else 'None'}
        Warning Issues: {', '.join(warning_hosts) if warning_hosts else 'None'}
        
        Alert Details:
{alert_summary}
        
        Please investigate these temperature issues {'immediately' if critical_hosts else 'promptly'} to prevent potential equipment damage.
        
        Full temperature monitoring report generated on {timestamp} is attached.
        
        Best regards,
        Network Monitoring System
        """
        else:
            body = f"""
        Dear Network Administrator,
        
        Please find attached the Cisco switch temperature monitoring report generated on {timestamp}.
        
        All monitored network switches are operating within normal temperature ranges.
        
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
        server.sendmail(sender_email, recipient_emails, text)  # Use list of recipients
        server.quit()
        
        logger.info(f"Email sent successfully to {', '.join(recipient_emails)}")
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
        
        # Analyze output for temperature alerts
        warning_hosts, critical_hosts, warning_details, critical_details = analyze_output_for_alerts(outputsVar)
        
        if critical_hosts:
            logger.error(f"CRITICAL temperature alerts detected on switches: {', '.join(critical_hosts)}")
        if warning_hosts:
            logger.warning(f"WARNING temperature alerts detected on switches: {', '.join(warning_hosts)}")
        if not critical_hosts and not warning_hosts:
            logger.info("No temperature alerts detected - all switches operating normally")
        
        # Create PDF report with color-coded alert highlighting
        pdf_success = create_pdf_report(outputsVar, pdf_filename, warning_hosts, critical_hosts, warning_details, critical_details)
        
        if pdf_success:
            # Send email with attachments and alert information
            email_success = send_email_with_attachment(pdf_filename, text_filename, time_str, warning_hosts, critical_hosts, warning_details, critical_details)
            
            if email_success:
                if critical_hosts:
                    logger.info(f"CRITICAL ALERT EMAIL sent successfully for switches: {', '.join(critical_hosts)}")
                elif warning_hosts:
                    logger.info(f"WARNING ALERT EMAIL sent successfully for switches: {', '.join(warning_hosts)}")
                else:
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
            email_success = send_email_with_attachment(None, text_filename, time_str, warning_hosts, critical_hosts, warning_details, critical_details)
            if email_success:
                logger.info("Text report sent successfully (PDF creation failed)")
    
    except Exception as e:
        logger.error(f"Critical error in main execution: {str(e)}")

if __name__ == "__main__":
    main()
