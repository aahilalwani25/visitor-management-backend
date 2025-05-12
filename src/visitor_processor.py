import re
from datetime import datetime
from difflib import SequenceMatcher


# Texts to explicitly exclude from name detection
EXCLUDED_TEXTS = {
    "PAKISTAN",
    "ISLAMIC REPUBLIC OF PAKISTAN",
    "ISLAMIC REPUBLIC",
    "ID CARD",
    "CNIC",
    "NATIONAL IDENTITY CARD",
    "IDENTITY CARD",
    "IDENTITY NUMBER",
    "ID NUMBER",
    "CARD NUMBER",
    "SIGNATURE",
    "VALID THRU",
    "DATE OF BIRTH",
    "DOB",
    "FATHER'S NAME",
    "Father Name",
    "FATHER NAME"
}

# def extract_visitor_info(ocr_response):
#     extracted_text = ocr_response.get("extracted_text", [])
#     print(extracted_text)
    
#     name = None
#     cnic = None
    
#     # 1. First find CNIC (strict format matching)
#     for item in extracted_text:
#         text = item["text"].strip()
#         # Pakistani CNIC format: 42201-1868522-3 (5-7-1 digits)
#         if re.fullmatch(r'\d{5}-\d{7}-\d{1}', text):
#             cnic = text
#             break
    
#     # 2. Find name by looking for the text after "Name" label
#     for i, item in enumerate(extracted_text):
#         current_text = item["text"].strip().upper()
        
#         # Look for "Name" label
#         if current_text == "NAME" and i + 1 < len(extracted_text):
#             next_item = extracted_text[i + 1]
#             candidate_name = next_item["text"].strip()
            
#             # Validate the candidate name
#             if (len(candidate_name) >= 3 and  # Name should be at least 3 characters
#                 candidate_name.upper() not in EXCLUDED_TEXTS and
#                 not any(char.isdigit() for char in candidate_name) and  # No digits
#                 ":" not in candidate_name and  # No colons
#                 candidate_name.upper() != "NAME" and  # Not another label
#                 next_item["confidence"] >= 0.85):  # High confidence
                
#                 name = candidate_name.title()  # Convert to title case
#                 break
    
#     # If name not found after "Name" label, try alternative approach
#     if not name:
#         # Look for text between "Name" and "Father Name" or other common labels
#         name_section_found = False
#         name_candidates = []
        
#         for item in extracted_text:
#             text = item["text"].strip()
            
#             # Skip low confidence items
#             if item["confidence"] < 0.85:
#                 continue
                
#             # Mark the start of name section
#             if text.upper() == "NAME":
#                 name_section_found = True
#                 continue
                
#             # Stop if we hit common following fields
#             if any(text.upper().endswith(x) for x in ["NAME", "FATHER", "DATE", "BIRTH", "IDENTITY"]):
#                 name_section_found = False
                
#             # Collect name candidates between "Name" and next label
#             if (name_section_found and 
#                 len(text) >= 3 and
#                 text.upper() not in EXCLUDED_TEXTS and
#                 not any(char.isdigit() for char in text)):
#                 name_candidates.append(text)
        
#         # Select the first valid name candidate
#         if name_candidates:
#             name = name_candidates[0].title()
    
#     return name, cnic

def is_similar_to_excluded(text, threshold=0.75):
    for word in EXCLUDED_TEXTS:
        similarity = SequenceMatcher(None, text.upper(), word.upper()).ratio()
        if similarity >= threshold:
            return True
    return False


def extract_name_candidates(text_blocks):
    name_candidates = []
    for item in text_blocks:
        text = item["text"].strip()
        conf = item["confidence"]
        upper_text = text.upper()
        # Apply filters
        if (3 <= len(text) <= 40 and
            conf >= 0.80 and
            not any(char.isdigit() for char in text) and
            not is_similar_to_excluded(upper_text)):
            # Heuristic score: prefer text with 2–4 words, mostly capitalized
            score = conf
            if len(text.split()) in (2, 3, 4):
                score += 0.1
            if sum(1 for w in text.split() if w.istitle()) >= 2:
                score += 0.1
            name_candidates.append((text, score))
    # Sort by highest score
    name_candidates.sort(key=lambda x: x[1], reverse=True)
    return name_candidates


def extract_visitor_info(ocr_response):
    extracted_text = ocr_response.get("extracted_text", [])
    name = None
    cnic = None
    # Find CNIC
    for item in extracted_text:
        text = item["text"].strip()
        if re.fullmatch(r'\d{5}-\d{7}-\d{1}', text):
            cnic = text
            break
    # Find best name candidate
    name_candidates = extract_name_candidates(extracted_text)
    if name_candidates:
        name = name_candidates[0][0].title()
    return name, cnic

def format_visitor_record(name, cnic):
    return {
        "full_name": name if name else "Unknown",
        "cnic": cnic if cnic else "",
        "check_in": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "check_out": "",
        "user_id": ""
    }