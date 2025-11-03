# This file stores all the step-by-step guides for the INEC CVR Portal.

# Base URL for the official INEC CVR Portal
INEC_PORTAL_URL = "https://cvr.inecnigeria.org/Public/getStarted"
INEC_SIGN_IN_URL = "https://cvr.inecnigeria.org/pvc"

# Universal steps that apply to ALL services
UNIVERSAL_STEPS = {
    "signup": {
        "title": "Portal Access & Account Setup",
        "description": "Every user must create an account or sign in to access INEC CVR services.",
        "steps": [
            {
                "number": 1,
                "instruction": "First, let's access the INEC CVR Portal. Open Google Chrome and type the address: **{}**".format(INEC_PORTAL_URL),
                "question": "Have you opened the portal? (type 'yes' when ready)"
            },
            {
                "number": 2, 
                "instruction": "Great! Now Select your desired application.",
                "question": "Can you see the sign up form?' (Type 'yes' to proceed)"
            },
            {
                "number": 3,
                "instruction": "**Create Account/Sign In:** \n• Sign up to create a new account or sign in to an existing account.",
                "question": "Have you created an account? (Type 'yes' once done)"
            },
            {
                "number": 4,
                "instruction": "**Verify Email (New Users Only):** Check your email inbox for a verification link from INEC, click the link to activate your account. Skip this step if you're an existing user.",
                "question": "Have you successfully verified your email? (type 'yes' to continue)"
            },
            {
                "number": 5,
                "instruction": "Now, sign in to your account, you'll see the various voter registration services.",
                "question": "Can you see the services available on the portal? (Type 'yes' to proceed)"
            }
        ]
    }
}

GUIDES = {
    # --- 0. UNIVERSAL SIGN-UP (Applies to everyone) ---
    "universal-signup": UNIVERSAL_STEPS["signup"],
    
    # --- 1. NEW VOTER REGISTRATION ---
    "new-registration": {
        "title": "New Voter Pre-Registration Guide",
        "description": "This is for citizens who have never registered before, between 2011 and 2022. Remember: Online Pre-Registration must be followed by physical Biometric Capture.",
        "prerequisites": ["universal-signup"],
        "steps": [
            {
                "number": 1,
                "instruction": "**Select Service:** From your dashboard, select **'New Voter Pre-Registration'** and click on **'Start Registration'**.",
                "question": "Have you selected 'New Voter Pre-Registration'? (type 'yes' to continue)"
            },
            {
                "number": 2,
                "instruction": "**Fill Application Form:** Carefully complete all sections with your personal data. Ensure all information matches your official documents.",
                "question": "Are you done filling the form? (type 'yes' when done)"
            },
            {
                "number": 3,
                "instruction": "Next, take two photos (normal and smiling) of yourself.",
                "question": "Have you successfully uploaded your passport photo? (type 'yes' to proceed)"
            },
            {
                "number": 4,
                "instruction": "Now, Schedule an appointment or copy your Application ID (PRE) for your physical biometric capture.",
                "question": "Have you booked your appointment? (Type 'yes' to continue)"
            },
            {
                "number": 5,
                "instruction": "Finally, Visit any INEC centre with your Application ID for biometric capture.",
                "question": "Have you saved or copied your pre-registration number? (type 'yes' to complete)"
            }
        ],
        "required_documents": [
            "Pre-registration number for physical capture"
        ],
        "completion_note": "NEXT STEP: Visit any INEC office for biometric capture."
    },

    # --- 2. TRANSFER OF POLLING UNIT ---
    "transfer": {
        "title": "Transfer of Polling Unit Guide",
        "description": "For already registered voters who have RELOCATED to a new area and need to change their Polling Unit to their new residence.",
        "prerequisites": ["universal-signup", "revalidation"],
        "steps": [
            {
                "number": 1,
                "instruction": "**Select Service:** From the dashboard, click on the *'Transfers'* option.",
                "question": "Have you selected the 'Transfers' service? (type 'yes' to continue)"
            },
            {
                "number": 2,
                "instruction": "**Identity Verification:** You'll be prompted to take two real-time pictures of yourself for verification against your existing voter record.",
                "question": "Have you completed the photo verification? (type 'yes' to proceed)"
            },
            {
                "number": 3,
                "instruction": "**Select New Location:** Enter your new residential address and select the new State, LGA, Registration Area (Ward), and desired Polling Unit (PU).",
                "question": "Have you selected your new polling unit location? (type 'yes' to continue)"
            },
            {
                "number": 4,
                "instruction": "**Submit Request:** Review all information and submit your transfer request.",
                "question": "Have you submitted your transfer application? (type 'yes' to complete)"
            }
        ],
        "required_documents": [
            "Your existing PVC or Voter's Identification Number (VIN)",
            "Evidence of new residency (utility bill, tenancy agreement)"
        ],
        "completion_note": "Your transfer request will be reviewed by the Electoral Officer. You'll receive updates via email. Once approved, collect your new PVC at your new Polling Unit."
    },

    # --- 3. VOTER INFORMATION UPDATE ---
    "update": {
        "title": "Voter Information Update Guide",
        "description": "For correcting errors like **misspelt names, date of birth, gender, or wrong address** on your existing voter record.",
        "prerequisites": ["universal-signup", "revalidation"],
        "steps": [
            {
                "number": 1,
                "instruction": "**Select Service:** From your dashboard, click on the **'Information Update'** option.",
                "question": "Have you selected 'Information Update'? (type 'yes' to continue)"
            },
            {
                "number": 2,
                "instruction": "**Search Your Record:** Find your voter record using your **Surname** or the last **6 digits of your VIN** (Voter ID Number).",
                "question": "Have you successfully found your voter record? (type 'yes' to proceed)"
            },
            {
                "number": 3,
                "instruction": "**Make Corrections:** Edit the specific field(s) that need correction (name, date of birth, address, etc.).",
                "question": "Have you made the necessary corrections? (type 'yes' to continue)"
            },
            {
                "number": 4,
                "instruction": "**Upload Supporting Documents (CRITICAL):** Upload clear photos/scans of legal documents that justify the changes (affidavit, birth certificate, marriage certificate, court order).",
                "question": "Have you uploaded the required supporting documents? (type 'yes' to complete)"
            }
        ],
        "required_documents": [
            "Existing PVC or VIN",
            "Supporting legal documents for the correction requested",
            "Affidavit for name changes or corrections"
        ],
        "completion_note": "Your update request will be processed by INEC. You may be required to visit a CVR center for verification if major changes are requested."
    },

    # --- 4. LOST OR DAMAGED PVC ---
    "lost-pvc": {
        "title": "Lost or Damaged PVC Replacement Guide",
        "description": "For requesting a replacement for a Permanent Voter's Card (PVC) that is missing or unusable.",
        "prerequisites": ["universal-signup", "revalidation"],
        "steps": [
            {
                "number": 1,
                "instruction": "**Select Service:** From your dashboard, click on **'Lost or Damaged PVC'**.",
                "question": "Have you selected the PVC replacement service? (type 'yes' to continue)"
            },
            {
                "number": 2,
                "instruction": "**Retrieve Your Record:** Provide required details to retrieve your existing voter record.",
                "question": "Have you found your voter record? (type 'yes' to proceed)"
            },
            {
                "number": 3,
                "instruction": "**State Reason:** Choose the reason for replacement: **Lost Card** or **Physically Damaged Card**.",
                "question": "Have you selected the appropriate reason? (type 'yes' to continue)"
            },
            {
                "number": 4,
                "instruction": "**Verification:** Take two pictures of yourself for identity verification against the INEC database.",
                "question": "Have you completed the identity verification? (type 'yes' to complete)"
            }
        ],
        "required_documents": [
            "Your voter information (VIN or personal details)",
            "Image of the damaged card (if applicable)"
        ],
        "completion_note": "Your replacement request has been submitted. Wait for INEC's public announcement for PVC collection and pick up your new card in person with valid ID."
    },

    # --- 5. VOTER REVIEW / REVALIDATION ---
    "revalidation": {
        "title": "Voter Information Review/Revalidation Guide",
        "description": "Required for all existing voters before making changes to their record. This verifies your identity and updates your voter information.",
        "prerequisites": ["universal-signup"],
        "steps": [
            {
                "number": 1,
                "instruction": "**Select Service:** From your dashboard, click on **'Review'** and input your PVC info to retrieve your Record.",
                "question": "Have you successfully retrieved your voter record? (type 'yes' to continue)"
            },
            {
                "number": 2,
                "instruction": "**Start Review:** Click 'Continue' and fill the form with your current information.",
                "question": "Are you done updating your information? (type 'yes' to proceed)"
            },
            {
                "number": 3,
                "instruction": "**Save & Update Photo:** Take two clear photos (normal and smiling) for identity verification.",
                "question": "Have you completed the photo verification? (type 'yes' to complete)"
            }
        ],
        "required_documents": [
            "Existing voter details (VIN or Surname)"
        ],
        "completion_note": "Your revalidation is complete! Your voter record is now verified and up-to-date."
    }
}