import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, WebDriverException
import svgpathtools
from music21 import converter, stream

# Initialize the Microsoft Edge webdriver
driver = webdriver.Edge()

def get_score_links():
    links = []
    try:
        score_links = driver.find_elements(By.XPATH, '//a[contains(@href, "user") and contains(@href, "scores")]')
        for score_link in score_links:
            score_link_url = score_link.get_attribute("href")
            links.append(score_link_url)
    except (StaleElementReferenceException, NoSuchElementException, WebDriverException) as e:
        print(f"Error getting score links: {e}")
    return links

def download_svg(svg_url, save_path, num):
    try:
        response = requests.get(svg_url)
        if response.status_code == 200:
            os.makedirs(save_path, exist_ok=True)
            svg_file_path = os.path.join(save_path, f"svg_{num}.svg")
            with open(svg_file_path, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded SVG: {svg_file_path}")
            return svg_file_path
    except Exception as e:
        print(f"Error downloading SVG from {svg_url}: {e}")
    return None

def convert_svg_to_musicxml(svg_file_path, musicxml_file_path):
    try:
        # Example SVG parsing using svgpathtools (replace with actual parsing logic)
        paths, attributes = svgpathtools.svg2paths(svg_file_path)
        
        # Example construction of a music21 stream
        score_stream = stream.Score()
        for path in paths:
            # Example: Convert path to music21 notation (replace with actual logic)
            # For example purposes, let's add a single note to the stream
            # Replace this with actual logic to interpret musical elements from SVG
            note = stream.Note("C4", quarterLength=1.0)
            score_stream.append(note)
        
        # Write the constructed stream to MusicXML file
        score_stream.write("musicxml", fp=musicxml_file_path)
        
        print(f"Converted {svg_file_path} to MusicXML: {musicxml_file_path}")
        return True
    except Exception as e:
        print(f"Error converting {svg_file_path} to MusicXML: {e}")
    return False

# Define paths
save_path = r"C:\Users\tfls_\Desktop\music_svg"
midi_save_path = r"C:\Users\tfls_\Desktop\music_midi"

# Open the URL
url = "https://musescore.com/sheetmusic?complexity=1&genres=45&recording_type=public-domain"
driver.get(url)

# Get relevant score links
relevant_links = get_score_links()
final_links = set()

# Iterate over score links
num = 0
for relevant_link in relevant_links:
    driver.get(relevant_link)
    try:
        image = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//img[@class="KfFlO"]')))
        img_src = image.get_attribute("src")
        final_links.add(img_src)
    except Exception as e:
        print(f"Error getting image src for {relevant_link}: {e}")

# Process each SVG file
for final_link in final_links:
    svg_file_path = download_svg(final_link, save_path, num)
    if svg_file_path:
        musicxml_file_path = svg_file_path.replace('.svg', '.musicxml')
        if convert_svg_to_musicxml(svg_file_path, musicxml_file_path):
            # Convert MusicXML to MIDI (if needed)
            # Add your conversion logic here
            pass
    num += 1

# Close the webdriver
driver.quit()

