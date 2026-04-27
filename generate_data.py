import json
import random

first_names = ["Aarav", "Aanya", "Vivaan", "Diya", "Aditya", "Ishita", "Vihaan", "Ananya", "Arjun", "Kavya", "Sai", "Priya", "Krishna", "Riya", "Rohan", "Sneha", "Rahul", "Nisha", "Amit", "Pooja", "Vikram", "Neha", "Sanjay", "Kiran", "Raj", "Anita", "Sunil", "Meera", "Anil", "Sita", "Ashok", "Gita", "Ramesh", "Nita", "Suresh", "Lata", "Ravi", "Mina", "Vijay", "Asha"]
last_names = ["Sharma", "Bhattarai", "Adhikari", "Thapa", "Gurung", "Tamang", "Rai", "Limbu", "Magar", "Shrestha", "Maharjan", "Joshi", "Karki", "Basnet", "Bhandari", "Poudel", "Gautam", "Lamsal", "Dahal", "Ghimire", "Nepal", "Baral", "Khatri", "Khadka", "Chhetri", "Malla", "Shah", "Singh", "Pradhan", "Amatya"]

options = {
  "1_How_often_do_you_visit_gover": [
    "Very Often", "Often", "Sometimes", "Rarely", "Never"
  ],
  "2_What_is_your_role": [
    "Student", "Job Seeker", "Working Professional", "Business Owner", "Other"
  ],
  "3_How_satisfied_are_you_with": [
    "1", "2", "3", "4", "5"
  ],
  "4_How_often_do_you_face_diffi": [
    "Very Often", "Often", "Sometimes", "Rarely", "Never"
  ],
  "5_Which_problem_do_you_face_m": [
    "Notices are scattered across many websites",
    "Difficult website navigation",
    "No proper search function",
    "Notices are only available in PDF/image form",
    "Delayed updates",
    "Other"
  ],
  "6_How_useful_would_a_single_p": [
    "Very Useful", "Useful", "Neutral", "Not Useful"
  ],
  "7_How_important_is_quick_acce": [
    "Very Important", "Important", "Neutral", "Not Important"
  ],
  "8_How_useful_would_AI_generat": [
    "Very Useful", "Useful", "Neutral", "Not Useful"
  ],
  "9_How_important_are_notificat": [
    "Very Important", "Important", "Neutral", "Not Important"
  ],
  "10_How_useful_would_category_b": [
    "Very Useful", "Useful", "Neutral", "Not Useful"
  ],
  "11_How_important_is_secure_lo": [
    "Very Important", "Important", "Neutral", "Not Important"
  ],
  "12_How_important_is_cloud_bas": [
    "Very Important", "Important", "Neutral", "Not Important"
  ],
  "13_How_useful_would_keyword_b": [
    "Very Useful", "Useful", "Neutral", "Not Useful", "Not Useful at All"
  ],
  "14_How_useful_would_document": [
    "Very Useful", "Useful", "Neutral", "Not Useful"
  ],
  "15_How_important_is_mobile_fr": [
    "Very Important", "Important", "Neutral", "Not Important"
  ],
  "16_Which_notice_category_do_y": [
    "Job Vacancies", "Exam Notices", "Tender Notices", "Policy Updates", "Scholarship Notices", "Other"
  ],
  "17_Which_features_would_you_p": [
    "Unified Search", "AI Summaries", "Keyword Alerts", "Category Filters", "Secure Login", "Cloud Storage", "Document Q&A", "Mobile Access"
  ],
  "18_Would_you_trust_AI_generat": [
    "Definitely Yes", "Probably Yes", "Not Sure", "Probably No", "Definitely No"
  ],
  "19_Would_you_use_an_AI_powere": [
    "Definitely Yes", "Probably Yes", "Not Sure", "Probably No", "Definitely No"
  ]
}

data = []

for i in range(70):
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    
    entry = {
        "Name": name,
        "1_How_often_do_you_visit_gover": random.choice(options["1_How_often_do_you_visit_gover"]),
        "2_What_is_your_role": random.choice(options["2_What_is_your_role"]),
        "3_How_satisfied_are_you_with": random.choices(options["3_How_satisfied_are_you_with"], weights=[0.1, 0.2, 0.4, 0.2, 0.1])[0],
        "4_How_often_do_you_face_diffi": random.choices(options["4_How_often_do_you_face_diffi"], weights=[0.2, 0.4, 0.3, 0.1, 0.0])[0],
        "5_Which_problem_do_you_face_m": random.choice(options["5_Which_problem_do_you_face_m"]),
        "6_How_useful_would_a_single_p": random.choices(options["6_How_useful_would_a_single_p"], weights=[0.6, 0.3, 0.1, 0.0])[0],
        "7_How_important_is_quick_acce": random.choices(options["7_How_important_is_quick_acce"], weights=[0.7, 0.2, 0.1, 0.0])[0],
        "8_How_useful_would_AI_generat": random.choices(options["8_How_useful_would_AI_generat"], weights=[0.5, 0.3, 0.1, 0.1])[0],
        "9_How_important_are_notificat": random.choices(options["9_How_important_are_notificat"], weights=[0.5, 0.4, 0.1, 0.0])[0],
        "10_How_useful_would_category_b": random.choices(options["10_How_useful_would_category_b"], weights=[0.6, 0.3, 0.1, 0.0])[0],
        "11_How_important_is_secure_lo": random.choices(options["11_How_important_is_secure_lo"], weights=[0.5, 0.3, 0.2, 0.0])[0],
        "12_How_important_is_cloud_bas": random.choices(options["12_How_important_is_cloud_bas"], weights=[0.4, 0.4, 0.2, 0.0])[0],
        "13_How_useful_would_keyword_b": random.choices(options["13_How_useful_would_keyword_b"], weights=[0.6, 0.3, 0.1, 0.0, 0.0])[0],
        "14_How_useful_would_document": random.choices(options["14_How_useful_would_document"], weights=[0.4, 0.4, 0.1, 0.1])[0],
        "15_How_important_is_mobile_fr": random.choices(options["15_How_important_is_mobile_fr"], weights=[0.8, 0.1, 0.1, 0.0])[0],
        "16_Which_notice_category_do_y": random.choice(options["16_Which_notice_category_do_y"]),
        # Question 17 is actually a radio button (multiple choice), so it only takes one value!
        "17_Which_features_would_you_p": random.choice(options["17_Which_features_would_you_p"]),
        "18_Would_you_trust_AI_generat": random.choices(options["18_Would_you_trust_AI_generat"], weights=[0.3, 0.4, 0.2, 0.1, 0.0])[0],
        "19_Would_you_use_an_AI_powere": random.choices(options["19_Would_you_use_an_AI_powere"], weights=[0.4, 0.4, 0.1, 0.1, 0.0])[0],
        "20_Additional_comments_or_sug": random.choices(["Great initiative", "Looking forward to this", "Keep it simple", "Please make it bilingual", "Mobile friendly design is a must", "I hope it launches soon", "N/A"], weights=[0.2, 0.2, 0.1, 0.1, 0.1, 0.1, 0.2])[0],
    }
    
    data.append(entry)

with open('generated_60_responses.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Generated generated_60_responses.json successfully!")
