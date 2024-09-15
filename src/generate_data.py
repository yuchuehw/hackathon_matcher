import sqlite3
import random
import string

first_names = [
    "Alex", "Jordan", "Taylor", "Morgan", "Riley", "Cameron", "Casey", "Jamie", "Avery", "Peyton",
    "Carter", "Drew", "Jesse", "Blake", "Charlie", "Quinn", "Dakota", "Rowan", "Skyler", "Reese"
]

last_names = [
    "Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor",
    "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson"
]

# List of hackathons
hackathons = [
    "TechTogether Online", "Hacks for Hackers", "HackBattle: React vs Angular", "Global Hack Week: Data",
    "HackRU", "HackUTA 2023", "The Golden Hack 5.0", "Data Hackfest", "HackGT X", "Hack the Valley",
    "Hackanile cal hacks", "Hacknc logo", "Datathon23", "Hackcbs 6.0 vector", "Hacknjit 2 mlh backsplash",
    "Gunnhacks 10.0", "Hackbi", "Hacktams", "Tamuhack", "InnovateHER Hackathon", "MorganHacks", "HackKU",
    "HogHacks", "Vihaan 007", "DragonHacks 2024", "KleinHacks", "RiverHacks 2024", "UTA Datathon",
    "Bitcamp 2024", "Hackathon Troyano 2024", "LA Hacks", "Web3Apps", "DragonHack", "HackDartmouth IX",
    "TribeHacks", "All In Open Source Hackathon", "HackDavis 2024", "GDSCHACKS Guelph", "HackUPC",
    "Hackathon Morelos"
]

# List of technologies
technologies = [
    "JavaScript", "Python", "React", "Node.js", "HTML", "CSS", "Java", "SQL", "Docker", "AWS",
    "Firebase", "Bootstrap", "Angular", "Vue.js", "Swift", "Kotlin", "Android Studio", "Xcode",
    "Jenkins", "Postman", "GraphQL", "MongoDB", "Redis", "TensorFlow", "PyTorch", "Jupyter Notebook",
    "OpenAI API", "ElasticSearch", "MySQL", "SQLite", "Apache Kafka", "Terraform", "Vagrant",
    "Apache Hadoop", "Kubernetes", "Nginx", "Apache", "C++", "C#", "Ruby on Rails", "Laravel",
    "WordPress", "Django", "Spring Boot", "Unity", "Unreal Engine", "GitHub", "GitLab", "Bitbucket"
]

# List of questions
questions = [
    "What is your favorite technology stack?",
    "What do you think is the most challenging part of hacking?",
    "How do you stay updated with the latest tech trends?",
    "What are your thoughts on open source contributions?",
    "What is the best hackathon project you have worked on?",
    "How do you approach debugging complex issues?",
    "What new technology are you most excited about?",
    "How do you manage your time during a hackathon?",
    "What resources do you use for learning new technologies?",
    "What is your strategy for collaborating with teammates remotely?"
]

def generate_username():
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    number = random.randint(1, 9999)
    return f"{first_name}{last_name}{number}"

def generate_data_entry():
    return {
        'username': generate_username(),
        'hackathon': random.choice(hackathons),
        'technology1': str(random.sample(technologies,random.randint(1,5))),
        'technology2': str(random.sample(technologies,random.randint(1,5))),
        'question1': random.choice(questions),
        'question2': random.choice(questions),
        'question3': random.choice(questions)
    }

def insert_dummy_data(num_entries):
    conn = sqlite3.connect('hackathon_matcher.db')  # Change 'example.db' to your database file name
    cursor = conn.cursor()

    # Insert data
    for _ in range(num_entries):
        data = generate_data_entry()
        try:
            cursor.execute('''
                INSERT INTO users (username, hackathon, technology1, technology2, question1, question2, question3)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (data['username'], data['hackathon'], data['technology1'], data['technology2'], data['question1'], data['question2'], data['question3']))
        except sqlite3.IntegrityError:
            # Username already exists, generate a new one
            continue

    conn.commit()
    conn.close()

# Insert 50 dummy data entries
insert_dummy_data(50)

