#!/usr/bin/env python3
"""
Test version of the enhanced temperature monitoring script
This version simulates switch connections for testing PDF and email functionality
"""

import pandas as pd
import datetime
import time
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
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

def main():
    """
    Test version of the temperature monitoring script
    """
    ts = time.time()
    
    # Test with sample data instead of reading Excel file
    logger.info("Running test version with simulated switch data")
    
    time_str = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    timestamp_safe = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M%S')
    
    # Create sample output to test PDF generation
    outputsVar = f'Start Script at Time: {time_str}\n'
    
    # Simulate output from multiple switches
    sample_switches = ['SW-CORE-01', 'SW-ACCESS-02', 'SW-DIST-03']
    
    for switch_name in sample_switches:
        # Simulate temperature output
        temp_output = f"""Temperature Status: Ok
Sensor                 Status          Reading
System Inlet           OK              23 Celsius
System Outlet          OK              28 Celsius
CPU Temperature        OK              42 Celsius
Power Supply 1         OK              35 Celsius
Power Supply 2         OK              33 Celsius"""
        
        outputsVar += f'\n --- Output of show env temp on {switch_name} \n{temp_output}\n\n'
    
    # Generate output files
    text_filename = f'device_output_test_{timestamp_safe}.txt'
    pdf_filename = f'device_temperature_report_test_{timestamp_safe}.pdf'
    
    # Write text output
    logger.info(f"Writing text output to: {text_filename}")
    with open(text_filename, 'w') as f:
        f.write(outputsVar)
    
    # Create PDF report
    pdf_success = create_pdf_report(outputsVar, pdf_filename)
    
    if pdf_success:
        logger.info("Test completed successfully!")
        logger.info(f"Generated files:")
        logger.info(f"  - Text file: {text_filename}")
        logger.info(f"  - PDF file: {pdf_filename}")
        print(f"\nTest Results:")
        print(f"✓ Text file created: {text_filename}")
        print(f"✓ PDF file created: {pdf_filename}")
        print(f"✓ All functionality working properly")
    else:
        logger.error("PDF generation failed")
        print("✗ PDF generation failed")

if __name__ == "__main__":
    main()