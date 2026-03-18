from typing import Dict, Any

class ResponseGenerator:
    def __init__(self):
        self.responses = self._load_all_responses()
    
    def _load_all_responses(self):
        """Load all service responses in both languages"""
        return {
            'en': self._get_english_responses(),
            'ml': self._get_malayalam_responses()
        }
    
    def _get_english_responses(self):
        """English responses for all services"""
        return {
            'greeting': "Welcome to Akshaya Digital Assistant. How can I help you today?",
            'farewell': "Thank you for using our services. Have a great day!",
            'unknown': "I understand you're asking about services. Please specify which service you need information about, or select a service from the sidebar.",
            'no_service': "Please specify which service you need information about. For example: 'ration card documents', 'passport application', or 'voter ID requirements'.",
            
            'ration_card': {
                'documents': """RATION CARD SERVICES - Required Documents:

NEW RATION CARD APPLICATION:
1. Identity Proof (Head of Family) - Aadhaar, Voter ID, Passport, Driving License, PAN Card, Government Photo ID
2. Address Proof - Aadhaar, Electricity/Water Bill (last 3 months), Landline/Broadband Bill, House Tax Receipt, Registered Rent Agreement, Passport (address page)
3. Proof of Family Members - Aadhaar of all members, Birth Certificate (children), School ID/Bonafide Certificate, Marriage Certificate, Self-declaration
4. Income Proof - Income Certificate (Govt./Tahsildar), Salary/Pension Certificate, Income Affidavit
5. Old Ration Card Surrender Proof (if any) - Cancellation Certificate, Old Ration Card Copy
6. Passport-size Photo of Head of Family
7. Filled Application Form & Self-Declaration

Kerala-specific (via Akshaya):
• Aadhaar linked mobile
• LSGD certificate (if required)
• Income certificate from e-District
• Online application slip

Processing Time: 15-30 days
Fee: No fee for Ration Card services""",
                
                'apply': """To apply for Ration Card:
1. Visit nearest Akshaya Center
2. Fill application form with all family details
3. Submit required documents
4. Get acknowledgment receipt
5. Ration card will be delivered to your address

You can also apply online through Civil Supplies Department portal.""",
                
                'general': """Ration Card Services Information:
• New Ration Card Application
• Addition/Deletion of Family Members
• Change of Address
• Correction in Ration Card
• Duplicate Ration Card
• Surrender of Ration Card

All services are free of cost."""
            },
            
            'marriage_registration': {
                'documents': """MARRIAGE REGISTRATION - Required Documents:

COMMON DOCUMENTS (All Religions):
1. Identity Proof (Bride & Groom) - Aadhaar, Voter ID, Passport, Driving License, PAN Card, Govt. Photo ID
2. Age Proof - Birth Certificate, SSLC/10th Certificate, Passport, School Leaving Certificate
3. Address Proof - Aadhaar, Voter ID, Passport, Utility Bill, Ration Card, Rent Agreement, House Tax Receipt
4. Marriage Proof - Marriage Certificate from Religious Authority, Marriage Invitation Card, Marriage Photo, Affidavit
5. Photographs - Passport-size photos of bride & groom
6. Witness Details - 2–3 Witnesses with Aadhaar, Address Proof, Photos
7. Marriage Registration Application Form
8. Marital Status Proof - Divorce Decree (if divorced), Death Certificate (if widowed)

SPECIAL MARRIAGE ACT (Inter-religion/Court Marriage):
1. Identity, Age & Address Proof (same as above)
2. 30 Days Residence Proof in jurisdiction
3. Notice of Intended Marriage Form
4. Marital Status Affidavit
5. Photographs
6. 3 Witnesses with Aadhaar, Address Proof, Photos
7. Affidavits (nationality, not in prohibited relationship, etc.)
8. Presence before Marriage Officer

Processing Time: 7-30 days
Fee: Varies based on Act and time period""",
                
                'apply': """Marriage Registration Process:
1. Apply at Local Registrar Office or Akshaya Center
2. Submit documents and application form
3. Pay prescribed fee
4. Receive acknowledgment
5. Certificate will be issued after verification

For Special Marriage Act, notice period is 30 days."""
            },
            
            'police_clearance': {
                'documents': """POLICE CLEARANCE CERTIFICATE (PCC) - Required Documents:

PCC VIA PASSPORT OFFICE (For Abroad):
1. Passport (Original + self-attested copies of first & last pages)
2. Address Proof - Aadhaar, Voter ID, Utility Bill, Bank Passbook, Rent Agreement, Ration Card
3. Online PCC Application (Passport Seva) + Receipt/ARN
4. Purpose Proof - Offer Letter, Visa Request, Embassy/University Letter
5. Passport-size Photographs
6. Fee Receipt
7. Police Verification (if required) - Address proof shown to police

DOMESTIC PCC (Employment/General):
1. Aadhaar Card
2. Address Proof
3. Passport-size Photo
4. Application Form
5. Employer/College/Rental Request Letter (if applicable)

Processing Time: 7-15 days for domestic, 15-30 days for passport PCC
Fee: ₹500 for passport PCC, varies for domestic""",
                
                'apply': """Apply for Police Clearance Certificate:
For Passport PCC:
1. Apply on Passport Seva Portal
2. Book appointment at PSK
3. Submit documents and biometrics
4. Police verification will be conducted
5. Collect PCC from PSK

For Domestic PCC:
1. Apply at District Police Headquarters
2. Submit application with documents
3. Police verification will be done
4. Collect certificate after clearance"""
            },
            
            'pan_card': {
                'documents': """PAN CARD SERVICES - Required Documents:

NEW PAN (Form 49A - Indian Citizen):
1. Identity Proof - Aadhaar, Voter ID, Passport, Driving License
2. Address Proof - Aadhaar, Voter ID, Passport, Utility Bill, Bank Passbook
3. Date of Birth Proof - Birth Certificate, SSLC, Passport, Aadhaar
4. Passport-size Photo, Signature, Mobile Number (OTP)

PAN CORRECTION/UPDATE:
1. Existing PAN Copy
2. Proof for Correction (Name/DOB/Address) - Aadhaar, Utility Bill, Birth Certificate, etc.
3. Photo, Signature

PAN-AADHAAR LINKING:
1. PAN Card
2. Aadhaar Card
3. Mobile linked with Aadhaar (OTP)

PAN FOR MINOR:
1. Minor's Birth Certificate
2. Minor's Aadhaar (if available)
3. Parent/Guardian PAN & Aadhaar
4. Photo of Minor

Processing Time: 15-20 days
Fee: ₹107 for new PAN (if not using Aadhaar)""",
                
                'apply': """Apply for PAN Card:
1. Apply online through NSDL or UTIITSL portal
2. Fill Form 49A with details
3. Upload documents and photo
4. Pay fee online
5. Submit signed copy if required
6. PAN card will be dispatched to address

For correction/update, use Form 49 for changes."""
            },
            
            'birth_certificate': {
                'documents': """BIRTH CERTIFICATE SERVICES - Required Documents:

NEW BIRTH REGISTRATION (within 21 days):
1. Hospital Birth Report / Discharge Summary
2. Parents' Aadhaar Cards
3. Marriage Certificate (if available)
4. Address Proof
5. Mobile Number

LATE BIRTH REGISTRATION (after 21 days):
1. Hospital Birth Proof / Affidavit
2. Parents' Aadhaar
3. Address Proof
4. Non-Availability Certificate (if applicable)
5. Application Form & Declaration

BIRTH CERTIFICATE CORRECTION:
1. Original Birth Certificate
2. Proof for Correction (Aadhaar, School Certificate, Hospital Record, etc.)
3. Application Form & Affidavit

DUPLICATE BIRTH CERTIFICATE:
1. Aadhaar Card
2. Birth Details (Name, DOB, Place)
3. Old Copy (if available)

Processing Time: 7-15 days for new registration
Fee: No fee for birth registration""",
                
                'apply': """Birth Certificate Registration:
1. Register at Hospital (if born in hospital) or Local Body Office
2. Submit documents within 21 days for easy registration
3. For late registration, additional affidavit required
4. Certificate will be issued after verification

Corrections require affidavit and supporting documents."""
            },
            
            'passport': {
                'documents': """PASSPORT SERVICES - Required Documents:

NEW PASSPORT (Fresh):
1. Aadhaar Card
2. Voter ID / Driving License / PAN Card
3. Birth Certificate / SSLC Certificate
4. Address Proof (Aadhaar, Utility Bill, Bank Passbook, Rent Agreement)
5. Passport-size Photos (if required)

PASSPORT RENEWAL:
1. Old Passport (Original + Copy)
2. Aadhaar Card
3. Address Proof (if changed)

CHANGE OF NAME (after Marriage/Gazette):
1. Old Passport
2. Aadhaar Card
3. Marriage Certificate / Gazette Notification
4. Address Proof

LOST/DAMAGED PASSPORT:
1. FIR Copy (for lost) / Damaged Passport
2. Old Passport Copy (if available)
3. Aadhaar Card
4. Address Proof

Processing Time: 30-45 days
Fee: Varies from ₹1500 to ₹3500 based on pages and validity""",
                
                'apply': """Passport Application Process:
1. Register on Passport Seva Portal
2. Fill online application form
3. Pay fee online
4. Book appointment at PSK
5. Visit PSK with documents
6. Police verification will be conducted
7. Passport will be delivered to address"""
            },
            
            'aadhaar': {
                'documents': """AADHAAR SERVICES - Required Documents:

NEW AADHAAR ENROLLMENT:
1. Proof of Identity - Aadhaar (if available), Passport, Voter ID, etc.
2. Proof of Address - Utility Bill, Bank Passbook, Rent Agreement, etc.
3. Proof of Date of Birth - Birth Certificate, SSLC, Passport

AADHAAR UPDATE (Name/DOB/Address):
1. Aadhaar Card
2. Supporting Document (for change) - SSLC, Birth Certificate, Utility Bill, etc.

AADHAAR MOBILE/EMAIL UPDATE:
1. Aadhaar Card

CHILD AADHAAR (Below 5 Years):
1. Birth Certificate
2. Parent's Aadhaar

Processing Time: 90 days for new enrollment, 30 days for updates
Fee: No fee for Aadhaar services""",
                
                'apply': """Aadhaar Enrollment/Update:
1. Visit nearest Aadhaar Enrollment Center (often at Akshaya Centers)
2. Fill enrollment/update form
3. Submit documents for verification
4. Provide biometrics (fingerprints, iris scan)
5. Get acknowledgment slip
6. Aadhaar card will be sent to address

For mobile/email update, visit Aadhaar Center or use online portal."""
            },
            
            'death_registration': {
                'documents': """DEATH REGISTRATION SERVICES - Required Documents:

NEW DEATH REGISTRATION:
1. Medical Certificate of Cause of Death (Form 4/4A)
2. Deceased Aadhaar Card
3. Informant Aadhaar Card
4. Hospital Discharge Summary / Burial-Cremation Certificate

LATE REGISTRATION (After 21 Days/1 Year):
1. Medical Certificate
2. Deceased & Informant Aadhaar
3. Affidavit
4. Local Body/Magistrate Approval (if very late)

DEATH CERTIFICATE CORRECTION/DUPLICATE:
1. Original Death Certificate
2. Proof for Correction (if applicable)
3. Informant Aadhaar
4. Application Form

Processing Time: 7-15 days
Fee: No fee for death registration""",
                
                'apply': """Death Registration Process:
1. Register death at Hospital (if died in hospital) or Local Body Office
2. Submit medical certificate and documents
3. Register within 21 days for normal process
4. For late registration, affidavit required
5. Certificate will be issued after verification"""
            },
            
            'ncl_certificate': {
                'documents': """NON-CREAMY LAYER (NCL) CERTIFICATE SERVICES - Required Documents:

NEW NCL CERTIFICATE:
1. Aadhaar Card
2. Caste Certificate
3. Ration Card
4. Latest Income Certificate
5. Residence Proof
6. Application Form & Self-Declaration

NCL RENEWAL/CORRECTION/DUPLICATE:
1. Previous NCL Certificate
2. Aadhaar Card
3. Updated Income Certificate
4. Proof for Correction (if applicable)

NCL FOR MINOR:
1. Child's Birth Certificate / Aadhaar
2. Parents' Aadhaar, Caste Certificate, Income Certificate
3. Ration Card

Processing Time: 15-30 days
Fee: No fee for NCL certificate""",
                
                'apply': """Apply for NCL Certificate:
1. Apply at Tahsildar Office or Revenue Department
2. Submit application with all documents
3. Verification will be conducted
4. Certificate will be issued after income verification

Income limit for NCL: ₹8 lakhs annual income"""
            },
            
            'voter_id': {
                'documents': """VOTER ID SERVICES - Required Documents:

NEW VOTER ID:
1. Proof of Identity - Aadhaar Card (preferred), PAN Card, Driving License, Passport
2. Proof of Address - Aadhaar Card, Electricity/Water bill (last 6 months), Bank Passbook, Rent Agreement
3. Proof of Date of Birth - Birth Certificate, SSLC Certificate, Passport
4. Two recent passport-size photographs
5. Mobile number (for OTP verification)

CORRECTION/UPDATE:
1. Existing Voter ID
2. Proof for Correction (Aadhaar, Utility Bill, etc.)
3. Application Form

DUPLICATE VOTER ID:
1. FIR (if lost) or Affidavit
2. Identity Proof
3. Address Proof

Processing Time: 15-30 days
Fee: No fee for Voter ID services""",
                
                'apply': """Apply for Voter ID:
1. Apply online through NVSP portal or visit Akshaya Center
2. Fill Form 6 for new registration
3. Submit documents
4. Booth Level Officer will verify details
5. Voter ID will be delivered to address"""
            },
            
            'income_certificate': {
                'documents': """INCOME CERTIFICATE - Required Documents:

NEW INCOME CERTIFICATE:
1. Aadhaar Card
2. Ration Card
3. Recent Salary Slips (last 6 months) or Income Proof
4. Bank Passbook/Statement (last 6 months)
5. Property Documents (if any)
6. Self-Declaration/Affidavit of Income
7. Application Form

RENEWAL/CORRECTION:
1. Previous Income Certificate
2. Updated Income Proof
3. Aadhaar Card
4. Proof for Correction (if applicable)

Processing Time: 15-30 days
Fee: No fee for Income Certificate""",
                
                'apply': """Apply for Income Certificate:
1. Apply at Tahsildar Office or Village Office
2. Submit application with documents
3. Verification will be conducted
4. Certificate will be issued after verification"""
            },
            
            'caste_certificate': {
                'documents': """CASTE CERTIFICATE - Required Documents:

NEW CASTE CERTIFICATE:
1. Aadhaar Card
2. Ration Card
3. Birth Certificate
4. Father's/Mother's Caste Certificate (if available)
5. School Certificate mentioning caste
6. Residence Proof
7. Application Form & Affidavit

RENEWAL/CORRECTION/DUPLICATE:
1. Previous Caste Certificate
2. Aadhaar Card
3. Proof for Correction (if applicable)
4. Application Form

Processing Time: 15-30 days
Fee: No fee for Caste Certificate""",
                
                'apply': """Apply for Caste Certificate:
1. Apply at Tahsildar Office or Revenue Department
2. Submit application with documents
3. Verification will be conducted
4. Certificate will be issued after community verification"""
            },
            
            'domicile_certificate': {
                'documents': """DOMICILE CERTIFICATE - Required Documents:

NEW DOMICILE CERTIFICATE:
1. Aadhaar Card
2. Birth Certificate
3. School Leaving Certificate
4. Ration Card/Voter ID
5. Residence Proof (minimum 15 years)
6. Father's/Mother's Domicile Certificate (if available)
7. Application Form & Affidavit

Processing Time: 15-30 days
Fee: No fee for Domicile Certificate""",
                
                'apply': """Apply for Domicile Certificate:
1. Apply at Tahsildar Office or Revenue Department
2. Submit application with residence proof
3. Verification will be conducted
4. Certificate will be issued after verification of residence period"""
            },
            
            'driving_license': {
                'documents': """DRIVING LICENSE - Required Documents:

LEARNER'S LICENSE:
1. Aadhaar Card
2. Age Proof (Birth Certificate/SSLC)
3. Address Proof
4. Passport-size Photos
5. Medical Certificate (Form 1A for commercial)
6. Application Form

PERMANENT LICENSE:
1. Learner's License
2. Age Proof
3. Address Proof
4. Training Certificate (if from school)
5. Application Form
6. Test Fee Receipt

RENEWAL:
1. Old Driving License
2. Aadhaar Card
3. Medical Certificate (if above 40/50 years)
4. Application Form

Processing Time: 30-45 days
Fee: Varies based on vehicle type""",
                
                'apply': """Apply for Driving License:
1. Apply online through Parivahan Sewa
2. Book slot for learner's test
3. Pass test and get learner's license
4. After 30 days, apply for permanent license
5. Pass driving test
6. License will be issued"""
            },
            
            'vehicle_registration': {
                'documents': """VEHICLE REGISTRATION - Required Documents:

NEW VEHICLE REGISTRATION:
1. Aadhaar Card
2. Address Proof
3. Sales Certificate (Form 21)
4. Road Worthiness Certificate (Form 22)
5. Insurance Certificate
6. Pollution Under Control Certificate
7. Invoice from Dealer
8. Temporary Registration (if any)
9. Application Form

TRANSFER OF OWNERSHIP:
1. Aadhaar of buyer and seller
2. Original RC Book
3. Form 29 & 30
4. Insurance Certificate
5. PUC Certificate
6. NOC (if from another state)

Processing Time: 7-15 days
Fee: Varies based on vehicle cost""",
                
                'apply': """Vehicle Registration Process:
1. Purchase vehicle from authorized dealer
2. Dealer will provide temporary registration
3. Apply for permanent registration at RTO
4. Submit all documents
5. Pay road tax and fees
6. Registration certificate will be issued"""
            }
        }
    
    def _get_malayalam_responses(self):
        """Malayalam responses for all services"""
        # Due to space constraints, showing structure
        # You would add the full Malayalam translations here
        return {
            'greeting': "അക്ഷയ ഡിജിറ്റൽ അസിസ്റ്റന്റിലേക്ക് സ്വാഗതം. ഇന്ന് എങ്ങനെ സഹായിക്കാം?",
            'farewell': "ഞങ്ങളുടെ സേവനങ്ങൾ ഉപയോഗിച്ചതിന് നന്ദി. ശുഭദിനം!",
            'unknown': "സേവനങ്ങളെക്കുറിച്ചാണ് ചോദിക്കുന്നതെന്ന് മനസ്സിലായി. ദയവായി ഏത് സേവനത്തെക്കുറിച്ചാണ് വിവരങ്ങൾ വേണ്ടതെന്ന് വ്യക്തമാക്കുക, അല്ലെങ്കിൽ സൈഡ്ബാറിൽ നിന്ന് ഒരു സേവനം തിരഞ്ഞെടുക്കുക.",
            'no_service': "ദയവായി ഏത് സേവനത്തെക്കുറിച്ചാണ് വിവരങ്ങൾ വേണ്ടതെന്ന് വ്യക്തമാക്കുക. ഉദാഹരണത്തിന്: 'റേഷൻ കാർഡ് ഡോക്യുമെന്റുകൾ', 'പാസ്പോർട്ട് അപേക്ഷ', അല്ലെങ്കിൽ 'വോട്ടർ ഐഡി ആവശ്യങ്ങൾ'.",
            
            'ration_card': {
                'documents': """റേഷൻ കാർഡ് സേവനങ്ങൾ - ആവശ്യമായ ഡോക്യുമെന്റുകൾ:

പുതിയ റേഷൻ കാർഡ് അപേക്ഷ:
1. തിരിച്ചറിയൽ തെളിവ് (കുടുംബ തലവൻ) - ആധാർ, വോട്ടർ ഐഡി, പാസ്പോർട്ട്, ഡ്രൈവിംഗ് ലൈസൻസ്, പാൻ കാർഡ്, സർക്കാർ ഫോട്ടോ ഐഡി
2. വിലാസ തെളിവ് - ആധാർ, വൈദ്യുതി/ജല ബിൽ (കഴിഞ്ഞ 3 മാസം), ലാൻഡ്‌ലൈൻ/ബ്രോഡ്ബാൻഡ് ബിൽ, വീട്ടുകര രസീത്, രജിസ്റ്റർ ചെയ്ത വാടക ഉടമ്പടി
3. കുടുംബ അംഗങ്ങളുടെ തെളിവ് - എല്ലാ അംഗങ്ങളുടെയും ആധാർ, ജനന സർട്ടിഫിക്കറ്റ് (കുട്ടികൾ), സ്കൂൾ ഐഡി/ബോണഫൈഡ് സർട്ടിഫിക്കറ്റ്, വിവാഹ സർട്ടിഫിക്കറ്റ്
4. വരുമാന തെളിവ് - വരുമാന സർട്ടിഫിക്കറ്റ്, ശമ്പള/പെൻഷൻ സർട്ടിഫിക്കറ്റ്, വരുമാന അഫിഡാവിത്ത്
5. പഴയ റേഷൻ കാർഡ് സർ‌റെൻഡർ തെളിവ് - റദ്ദാക്കൽ സർട്ടിഫിക്കറ്റ്, പഴയ റേഷൻ കാർഡ് കോപ്പി
6. കുടുംബ തലവന്റെ പാസ്പോർട്ട് സൈസ് ഫോട്ടോ
7. പൂരിപ്പിച്ച അപേക്ഷ ഫോം & സ്വയം പ്രഖ്യാപനം

കേരളം-നിർദ്ദിഷ്ട (അക്ഷയ വഴി):
• ആധാർ ലിങ്ക് ചെയ്ത മൊബൈൽ
• എൽ.എസ്.ജി.ഡി. സർട്ടിഫിക്കറ്റ്
• ഇ-ഡിസ്‌ട്രിക്റ്റിൽ നിന്നുള്ള വരുമാന സർട്ടിഫിക്കറ്റ്
• ഓൺലൈൻ അപ്ലിക്കേഷൻ സ്ലിപ്പ്

പ്രോസസ്സിംഗ് സമയം: 15-30 ദിവസം
ഫീസ്: റേഷൻ കാർഡ് സേവനങ്ങൾക്ക് ഫീസ് ഇല്ല""",
                
                'apply': """റേഷൻ കാർഡിന് അപേക്ഷിക്കാൻ:
1. സമീപത്തുള്ള അക്ഷയ സെന്റർ സന്ദർശിക്കുക
2. എല്ലാ കുടുംബ വിവരങ്ങളും ഉള്ള അപേക്ഷ ഫോം പൂരിപ്പിക്കുക
3. ആവശ്യമായ ഡോക്യുമെന്റുകൾ സമർപ്പിക്കുക
4. സ്വീകാര്യത രസീത് ലഭിക്കും
5. റേഷൻ കാർഡ് നിങ്ങളുടെ വിലാസത്തിലേക്ക് ഡെലിവർ ചെയ്യും

സിവിൽ സപ്ലൈസ് വകുപ്പ് പോർട്ടലിലൂടെ ഓൺലൈനിലും അപേക്ഷിക്കാം."""
            }
            # Add Malayalam for all other services...
        }
    
    def generate_response(self, processing_result: Dict[str, Any]) -> str:
        """
        Generate response based on processing result
        """
        language = processing_result['response_language']
        service = processing_result['service']
        intent = processing_result['intent']
        
        # Get responses for the language
        lang_responses = self.responses.get(language, self.responses['en'])
        
        # If no service detected
        if not service:
            if intent == 'greeting':
                return lang_responses['greeting']
            elif intent == 'farewell':
                return lang_responses['farewell']
            else:
                return lang_responses['no_service']
        
        # If service detected but not in responses
        if service not in lang_responses:
            if language == 'ml':
                return f"ക്ഷമിക്കണം, {service.replace('_', ' ')} സേവനത്തിനുള്ള വിവരങ്ങൾ ലഭ്യമല്ല. ദയവായി വീണ്ടും ശ്രമിക്കുക."
            else:
                return f"Sorry, information for {service.replace('_', ' ')} service is not available. Please try again."
        
        service_responses = lang_responses[service]
        
        # Check if we have response for the specific intent
        if intent in service_responses:
            return service_responses[intent]
        elif 'general' in service_responses:
            return service_responses['general']
        else:
            # Return first available response for the service
            first_key = next(iter(service_responses))
            return service_responses[first_key]
    
    def get_service_introduction(self, service: str, language: str = 'en') -> str:
        """
        Get introductory text for a service
        """
        lang_responses = self.responses.get(language, self.responses['en'])
        
        if service in lang_responses and 'general' in lang_responses[service]:
            return lang_responses[service]['general']
        
        if language == 'ml':
            return f"{service.replace('_', ' ')} സേവന വിവരങ്ങൾ. ഡോക്യുമെന്റുകൾ, അപേക്ഷ പ്രക്രിയ, ഫീസ്, സമയം എന്നിവയെക്കുറിച്ച് വിവരങ്ങൾ ലഭ്യമാണ്."
        else:
            return f"{service.replace('_', ' ')} service information. Details about documents, application process, fees, and time are available."