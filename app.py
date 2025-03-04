from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.output_parsers import PydanticOutputParser
import os
import streamlit as st
import requests

os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

def get_llm():
    return ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)

def company_brief(scrape):

    template3 = """
    Scrape: {scrape}
    Using the information scraped from the company websites, write a company brief that highlights key aspects of the business. 
    Rather than sticking to predefined categories, organize the brief into natural sections based on the content provided (e.g. problem statement, solution, features, target audience, mission and vision, differentiator). 
    Dynamically define the buckets(sub topics/sections) based on the information present in the scrape and not fancy headings.
    Use all the information, don't miss anything.

    Here are several possible buckets (sections) that can be used to create a company brief, depending on the information available:

    1. **Company Overview/Introduction**  
    - General description of the company, its mission, and its vision.

    2. **Founding and History**  
    - Founding year, founder(s), key milestones, and historical context.

    3. **Industry and Market**  
    - The industry in which the company operates, its market segment, and target audience.

    4. **Products and Services**  
    - Overview of the main products or services offered, including flagship offerings.

    5. **Unique Selling Proposition (USP)**  
    - What sets the company apart from its competitors (e.g., technology, service quality, pricing, innovation).

    6. **Mission and Values**  
    - Core principles and values driving the company’s operations and long-term vision.

    7. **Leadership and Team**  
    - Key leaders or management team, including their experience and background.

    8. **Clients and Customers**  
    - Key clients or the types of customers the company serves, testimonials, or notable partnerships.

    9. **Innovations and Technology**  
    - Any proprietary technology, patents, or innovative processes developed by the company.

    10. **Market Position and Competitors**  
    - The company’s position in the market, its primary competitors, and how it differentiates itself.

    11. **Financial Highlights**  
    - Revenue, profit margins, or any significant financial metrics (if available or publicly disclosed).

    12. **Achievements and Awards**  
    - Major accomplishments, industry recognition, certifications, or awards received.

    13. **Corporate Social Responsibility (CSR)**  
    - Contributions to sustainability, community service, or ethical practices.

    14. **Partnerships and Collaborations**  
    - Strategic alliances or collaborations with other organizations, businesses, or institutions.

    15. **Global Reach/Geographic Presence**  
    - Locations or regions where the company operates, including headquarters and global footprint.

    16. **Growth and Future Outlook**  
    - Recent growth trends, future goals, expansion plans, or new product launches.

    17. **Challenges and Solutions**  
    - Any key challenges the company faces and how they address them.

    18. **Customer Support and Experience**  
    - Details about customer service standards or user experience.

    19. **Company Culture**  
    - Overview of the internal culture, work environment, and employee engagement.

    20. **Social Media and Digital Presence**  
    - The company's online presence, including social media, blogs, and digital marketing strategies.

    21. **Investor Relations**  
    - Information for potential investors, financial backers, or shareholders.

    22. **Sustainability and Environmental Impact**  
    - Efforts toward sustainability, energy efficiency, and reducing environmental impact.

    23. **Legal and Compliance**  
    - Adherence to legal standards, industry regulations, or data protection (especially for highly regulated industries).

    24. **Recent News and Media**  
    - Mention of the latest media coverage, press releases, or newsworthy developments.

    Use these buckets to create the compay brief, don't have to use all instead use those for which you get information from the scrape.
    Focus on areas such as company history, industry focus, products or services, market position, core strengths, and anything that stands out (e.g., innovations, partnerships, or awards). 
    Adapt the structure to best represent the company's unique profile and strengths.
    Don't use 'This company...' or 'The company...', instead use the name of the company.
    The sub topics/sections name should be exactly as mentioned above and not anything else.

    """
    prompt3 = ChatPromptTemplate.from_template(template3)
    llm_google = get_llm()
    chain3 = prompt3 | llm_google

    res3 = chain3.invoke(scrape)
    return res3.content

def get_scrape(url):
    data = requests.get(f"https://r.jina.ai/{url}")
    data = data.text
    data = data.replace("Markdown Content:","")
    return data

# Streamlit app
st.title("Company Brief Generator")

# Input query
url = st.text_input("Enter wensite url")
det = st.text_input("Enter company details (optional)")

if st.button("Generate"):
    scrape = get_scrape(url)
    company_b = company_brief(f"Company details: \n\n {det} \n\n Company website scrape: \n\n {scrape}")
    st.header("COMPANY BRIEF")
    st.write(company_b)
    with st.expander("Click to view website scrape"):
        st.write(scrape)