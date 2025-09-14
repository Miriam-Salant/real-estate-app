Real Estate Platform (Django)🏡

📌 Project Description
A web application for buying and selling apartments.
The system allows users to register as buyers or sellers, publish properties for sale, search for relevant listings, and contact sellers directly.

🧩 Main Features

User registration & login – choose role: buyer or seller.

Homepage – describes the purpose of the website for unregistered users.

Property publishing (for sellers/agents):

Add property details: city, neighborhood, street, floor, number of rooms, property condition.

Upload multiple images.

Mark if the property is sold with or without an agent.

Search & filtering (for buyers): view only relevant properties based on chosen parameters.

Contact sellers – send inquiries directly from the website.

Property management (for sellers):

View listed properties.

Track received inquiries.

Update property status to "sold".

Broker commission calculation when a property is sold.

Automatic removal of sold properties from future searches.

🗂 Architecture (tables & relations)

User – user information and role (buyer/seller).

Property – property details, images, status, linked to the seller.

Inquiry – buyer inquiries linked to properties.

BrokerCommission – commission records for agents when properties are sold.

⚡ Technologies

Django (Python)

HTML / CSS / Bootstrap

SQLite (development)

📝 Installation & Setup

Clone the repository:

git clone https://github.com/USERNAME/real-estate-app.git


Create a virtual environment and install dependencies:

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt


Run migrations:

python manage.py migrate


Start the development server:

python manage.py runserver


Open in browser: http://127.0.0.1:8000/
