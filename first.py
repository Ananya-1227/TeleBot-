import os
import random
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

TOKEN = "7592264448:AAFbnuPq-kxDDvqhOWJxL7D84fpcbQs3Yhk"
GROUP_WELCOMES = {}

# Structured categories with nested questions
QA_CATEGORIES = {
    "book1": {
        "name": "How to become a Hyper Achiever💪",
        "questions": [  #List of Dictionaries
            {
            "question": "How to Be in the Top 5% of Successful People in the World",
            "answer": "To reach the top 5% of successful people, individuals must:\n- Understand their strengths and weaknesses to maximize potential.\n- Leverage resources effectively, including knowledge, networks, and technology.\n- Develop lasting relationships with professionals in their industry.\n- Set SMART goals (Specific, Measurable, Achievable, Relevant, and Time-bound).\n- Adopt a growth mindset, continuously learning from failures and challenges."
            },
            {
            "question": "Biggest Challenges Hyper Achievers Face in Today’s Fast-Paced World",
            "answer": "- Balancing Personal and Professional Life – Many hyper achievers struggle to maintain relationships and personal well-being while pursuing success.\n- Handling Stress and Burnout – The pressure to constantly perform at high levels can lead to exhaustion.\n- Keeping Up with Rapid Changes – The evolving landscape of industries requires adaptability and continuous learning.\n- Managing Expectations – Societal and self-imposed expectations can become overwhelming.\n- Navigating Uncertainty – Economic and technological disruptions can create instability."
            },
            {
            "question": "Mindset Shifts Necessary to Thrive in the 21st Century (According to Charles Antony)",
            "answer": "- From Fixed to Growth Mindset – Embracing learning, adaptability, and resilience.\n- From Passive to Proactive Thinking – Taking initiative rather than waiting for opportunities.\n- From Short-Term to Long-Term Focus – Prioritizing sustained success over quick wins.\n- From Fear of Failure to Embracing Challenges – Viewing setbacks as learning experiences.\n- From Comfort Zone to Continuous Improvement – Always pushing boundaries."
            },
            {
            "question": "Role of Technology in Shaping Hyper Achievers",
            "answer": "- Enhances Productivity – Automation, AI, and digital tools streamline work.\n- Expands Learning Opportunities – Access to global knowledge at unprecedented speed.\n- Improves Networking – Social media and professional platforms help build strong connections.\n- Increases Efficiency – Data-driven decision-making optimizes performance.\n- Creates Competitive Edge – Those who leverage technology effectively outpace others."
            },
            {
            "question": "Key Differences Between Traditional Success Strategies and the Modern Hyper Achiever Mindset",
            "answer": "- Traditional: Focuses on linear growth, stability, and specialization.\n- Modern: Prioritizes adaptability, interdisciplinary skills, and leveraging digital advancements.\n- Traditional: Relies on structured career paths.\n- Modern: Encourages unconventional paths, entrepreneurship, and innovation."
            },
            {
            "question": "Trends Influencing High Achievers and How to Leverage Them",
            "answer": "- AI & Automation: Use AI-driven tools to optimize workflows.\n- Remote Work & Globalization: Expand professional networks beyond local boundaries.\n- Personal Branding: Build authority through social media and content creation.\n- Lifelong Learning: Stay ahead with continuous skill development."
            },
            {
            "question": "Definition of a Hyper Achiever (According to Charles Antony) & Difference from Average Success",
            "answer": "- Hyper Achievers: Individuals who consistently exceed expectations, dominate their industries, and continuously improve.\n- Key Differences:\n  - Extreme Focus & Discipline\n  - Rapid Adaptability\n  - High Risk-Taking Ability\n  - Innovative Thinking"
            },
            {
            "question": "Top Five Characteristics That Distinguish Hyper Achievers",
            "answer": "1. Ambition – Constantly striving for excellence.\n2. Resilience – Bouncing back from setbacks.\n3. Laser Focus – Eliminating distractions.\n4. Continuous Learning – Always upgrading skills.\n5. Networking Mastery – Building strong relationships."
            },
            {
            "question": "Mindset Shifts to Transition from Average to Hyper Achiever",
            "answer": "- From Comfort to Challenge-Seeking\n- From Doing More to Doing What Matters\n- From Fear of Failure to Learning from Failure\n- From Fixed Mindset to Experimentation & Innovation"
            },
            {
            "question": "Biggest Misconception About Hyper Achievers (According to Charles Antony)",
            "answer": "Many believe hyper achievers are just ‘naturally gifted,’ but in reality, they develop their skills through discipline, failure, and persistence."
            }
        ]
    },
    "book2": {
        "name": "Deal with Startups 😎🐱‍🏍",
        "questions": [#List of all the dictionaries
            {
            "question": "What makes a startup different from a traditional business?",
            "answer": "A startup is not just a smaller version of an established company. It is designed for rapid scaling, innovation, and industry disruption. Unlike a traditional business that grows incrementally, startups focus on exponential growth using technology, novel approaches, and scalable solutions. They take higher risks but have the potential for massive industry impact."
            },
            {
            "question": "What are the key characteristics of a successful startup?",
            "answer": "Successful startups share these traits:\n- Scalability – Growth is exponential, not linear.\n- Innovation – They introduce new solutions or business models.\n- Risk and Reward – Higher failure rates but significant industry impact.\n- Economic Contributions – Job creation, technology advancement, and ecosystem development."
            },
            {
            "question": "What critical factors determine a startup’s success?",
            "answer": "- Market Traction – Evidence that the idea resonates with customers through sales, user growth, or engagement metrics like Customer Acquisition Cost (CAC) and Lifetime Value (LTV).\n- Management Team – Experienced and adaptable leadership.\n- Organizational Efficiency – Lean structures for agility.\n- Exit Strategy – Plans for IPOs, acquisitions, or mergers."
            },
            {
            "question": "How can a startup validate its business idea before launching?",
            "answer": "Startups should validate their concept before significant investment.\n- Surveys & Interviews – Directly gather feedback from potential users.\n- Minimum Viable Product (MVP) – Launch a simplified version of the product to test market demand.\n- Market Fit Analysis – Ensure the product addresses a real problem."
            },
            {
            "question": "What are common funding options for startups?",
            "answer": "- Bootstrapping – Using personal savings or revenue.\n- Angel Investors – Wealthy individuals investing in early-stage startups.\n- Venture Capital (VC) – Funding from firms that back high-growth startups.\n- Crowdfunding – Raising money from multiple contributors online."
            },
            {
            "question": "What makes a great startup pitch?",
            "answer": "A strong pitch should:\n- Clearly define the problem the startup is solving.\n- Present a compelling solution with unique advantages.\n- Show traction and market validation (evidence of demand).\n- Specify funding needs and how the investment will be used.\n- Deliver with confidence and use visuals effectively."
            },
            {
            "question": "How should startups plan their financials?",
            "answer": "- Create revenue projections and track expenses.\n- Manage cash flow to ensure operational sustainability.\n- Set a budget and allocate resources wisely.\n- Implement financial controls to prevent mismanagement."
            },
            {
            "question": "What are the most effective growth strategies for startups?",
            "answer": "- Referral Programs – Encouraging customers to bring in new users.\n- Strategic Partnerships – Collaborating with other businesses to expand reach.\n- Content Marketing & SEO – Using blogs, videos, and search optimization.\n- Paid Advertising – Running targeted online campaigns."
            },
            {
            "question": "What is the Lean Startup methodology?",
            "answer": "The Lean methodology focuses on rapid iteration, customer feedback, and minimizing waste.\n- Build-Measure-Learn – Quickly develop, test, and refine products.\n- Minimum Viable Product (MVP) – Launch an early version to validate demand.\n- Data-Driven Decision Making – Prioritize user insights over assumptions."
            },
            {
            "question": "How should a startup choose its business model?",
            "answer": "- Subscription Model – Recurring revenue through monthly or yearly payments.\n- Marketplace Model – Connecting buyers and sellers (e.g., Airbnb, Uber).\n- Freemium Model – Offering free basic services with paid premium features.\n- Direct Sales Model – Selling products or services directly to customers."
            },
            {
            "question": "What is the importance of market research for startups?",
            "answer": "- Identifies customer needs and preferences.\n- Analyzes competition and industry trends.\n- Defines the Total Addressable Market (TAM) to assess potential revenue.\n- Helps refine pricing and marketing strategies."
            },
            {
            "question": "What are the key elements of a strong startup team?",
            "answer": "- Defined Roles – CEO, CTO, and key operational leads.\n- Cultural Fit – Employees who align with the startup’s vision.\n- Skill Balance – A mix of technical, marketing, and financial expertise.\n- Clear Leadership & Trust – Encouraging collaboration and decision-making."
            },
            {
            "question": "How do startups build a strong competitive advantage?",
            "answer": "- Innovation – Unique product features or technology.\n- Brand Positioning – A clear and compelling brand identity.\n- Customer Experience – Exceptional service and engagement.\n- Operational Efficiency – Cost advantages or superior logistics."
            },
            {
            "question": "What are common mistakes startups should avoid?",
            "answer": "- Lack of Market Fit – Launching a product no one needs.\n- Running Out of Cash – Poor financial planning and overspending.\n- Weak Business Model – Unclear revenue generation strategy.\n- Ignoring Customer Feedback – Not adapting to user needs."
            },
            {
            "question": "How do startups prepare for scaling?",
            "answer": "- Optimize operations – Automate and improve processes.\n- Expand market reach – Target new regions or demographics.\n- Develop a hiring strategy – Build a larger, more skilled team.\n- Secure additional funding – Plan capital requirements for growth."
            },
            {
            "question": "What are key strategies for attracting investors?",
            "answer": "- Demonstrate traction – Show strong customer interest and sales.\n- Have a solid business plan – Clearly outline strategy and revenue model.\n- Showcase a strong team – Highlight expertise and execution ability.\n- Be prepared for due diligence – Maintain accurate financial and legal records."
            },
            {
            "question": "How can startups maintain agility in a changing market?",
            "answer": "- Stay data-driven – Use analytics to adapt strategies.\n- Test and iterate quickly – Be willing to pivot if necessary.\n- Keep costs flexible – Avoid high fixed costs and commitments.\n- Encourage innovation – Foster a culture of continuous improvement."
            },
            {
            "question": "What role does customer feedback play in startup success?",
            "answer": "- Refines product features based on real user needs.\n- Enhances customer satisfaction by addressing pain points.\n- Increases loyalty and retention through responsive service.\n- Improves marketing strategies by understanding customer behavior."
            },
            {
            "question": "How do startups plan an exit strategy?",
            "answer": "- Initial Public Offering (IPO) – Selling shares to the public.\n- Acquisition/Merger – Selling the company to a larger firm.\n- Buyouts – Allowing investors or team members to take over.\n- Profitability & Independence – Growing without external exit pressure."
            }

        ]
    },
    "book3": {
        "name": "All-about Senior Corporate Leaders🤓",
        "questions":[#List of all the questions
            {
            "question": "What are the key hallmarks of next-generation leadership in the digital age?",
            "answer": "Next-generation leaders must develop digital fluency and technological foresight, allowing them to anticipate and adapt to technological disruptions. They also need adaptive decision-making capabilities to handle fast-evolving business landscapes while maintaining a balance between human-centered leadership and data-driven strategic execution."
            },
            {
            "question": "How can leaders effectively integrate corporate strategy with digital transformation?",
            "answer": "Leaders should focus on strategic technology integration to navigate disruptive environments. They must implement AI-enhanced decision frameworks while maintaining clarity in strategic vision. Using predictive analytics allows organizations to gain competitive intelligence and improve market positioning."
            },
            {
            "question": "Why is adaptive leadership important in today’s interconnected global market?",
            "answer": "Adaptive leadership enables corporate leaders to manage distributed digital workforces efficiently. It also helps in creating organizational structures that benefit from technological convergence, ensuring companies can innovate and respond to market changes swiftly."
            },
            {
            "question": "How can leaders drive market expansion through digital innovation?",
            "answer": "Leaders must evaluate technological partnership opportunities in emerging markets and develop platform strategies that enable rapid scaling. By creating digital-first value propositions, companies can establish a strong presence in global markets, surpassing geographical barriers."
            },
            {
            "question": "What role does AI-enhanced operational excellence play in modern organizations?",
            "answer": "AI plays a crucial role in improving operational efficiency by implementing intelligent automation, enhancing customer value delivery, and developing predictive maintenance systems to ensure operational resilience. End-to-end digital process optimization further streamlines workflow and enhances productivity."
            },
            {
            "question": "How can corporate leaders integrate startups into large enterprises?",
            "answer": "Entrepreneurial leadership requires establishing innovation ecosystems where corporations can collaborate with startups to leverage their agility. Leaders must implement rapid prototyping methodologies, powered by advanced analytics, and develop talent strategies that balance technical expertise with strategic vision."
            },
            {
            "question": "What strategies help leaders build future-ready organizational capabilities?",
            "answer": "Organizations need to foster digital intelligence through structured executive development. This includes implementing AI-enhanced analytical frameworks for strategic insights, developing responsible AI governance, and ensuring digital ethics frameworks that balance trust and innovation."
            },
            {
            "question": "How can organizations enhance data-driven decision-making?",
            "answer": "Leaders should use AI-enhanced analytical frameworks to extract meaningful insights from data. Establishing organizational capabilities for AI governance ensures ethical data usage. Digital ethics frameworks play a role in maintaining customer trust while enabling technological advancement."
            },
            {
            "question": "How should executives develop leadership skills for the digital economy?",
            "answer": "Executives need structured pathways for digital leadership development. Implementing reverse mentoring programs, where younger, tech-savvy employees mentor senior executives, enhances digital fluency. Creating cross-industry learning networks also helps in staying ahead of emerging technology trends."
            },
            {
            "question": "What is the importance of hyper-personalization in customer engagement?",
            "answer": "Hyper-personalization uses advanced analytics and predictive customer journey mapping to tailor experiences for individual users. Implementing real-time personalization engines across digital touchpoints ensures an enhanced customer experience and deeper engagement."
            },
            {
            "question": "How can organizations create seamless omnichannel experiences for customers?",
            "answer": "A cohesive omnichannel strategy requires the integration of data across multiple platforms. Companies should leverage real-time personalization engines to unify digital and physical touchpoints, ensuring a seamless transition between different customer engagement channels."
            },
            {
            "question": "What are the key components of strategic organizational reinvention?",
            "answer": "Organizations must conduct digital maturity assessments to evaluate their capabilities. Developing technology roadmaps aligned with strategic business objectives ensures structured digital transformation. Additionally, creating sustainable digital business models drives long-term value creation."
            },
            {
            "question": "How can AI be used for predictive analytics in decision-making?",
            "answer": "AI-driven predictive analytics allows businesses to anticipate market trends, understand customer behavior, and enhance competitive positioning. These insights support leaders in making data-backed, strategic decisions to drive business growth."
            },
            {
            "question": "What frameworks can organizations use for innovation in digital markets?",
            "answer": "Organizations can adopt innovation frameworks that harness emerging technologies by integrating cross-functional teams, leveraging AI-driven automation, and fostering digital-first strategies that prioritize scalability and user engagement."
            },
            {
            "question": "How do corporate leaders ensure responsible AI governance?",
            "answer": "Establishing clear AI governance policies ensures transparency and accountability in AI-driven decisions. Leaders must also implement digital ethics frameworks to balance innovation with ethical considerations, preventing biases and ensuring compliance with global regulations."
            },
            {
            "question": "How can companies leverage AI for operational efficiency?",
            "answer": "AI enhances operational efficiency through intelligent automation, predictive maintenance systems, and end-to-end process optimization. This reduces downtime, improves productivity, and streamlines business operations."
            },
            {
            "question": "What strategies help companies implement a data-driven corporate culture?",
            "answer": "Leaders must encourage AI-enhanced strategic insight generation and implement cross-industry learning networks to foster data-driven decision-making. A culture of continuous learning ensures long-term adaptation to technological advancements."
            },
            {
            "question": "How can organizations integrate digital transformation into their core business strategy?",
            "answer": "Digital transformation must be an integral part of corporate strategy rather than an isolated initiative. This involves aligning technology roadmaps with business objectives, developing data-driven decision frameworks, and maintaining agility in disruptive environments."
            },
            {
            "question": "What role does automation play in enhancing customer experiences?",
            "answer": "Automation streamlines customer interactions through AI-driven chatbots, personalized recommendations, and real-time analytics. This improves engagement and operational efficiency, ensuring customers receive tailored solutions faster."
            },
            {
            "question": "How do leaders balance human-centric leadership with AI-driven strategies?",
            "answer": "While AI provides data-driven efficiency, human-centric leadership ensures empathy, creativity, and emotional intelligence remain central to decision-making. Successful leaders merge AI-driven insights with human judgment, fostering trust and innovation simultaneously."
            }
        ]
        
    },
    "book4":{
        "name": "AI Future🤖",
        "questions": [#List of the questions
            {
            "question": "How is AI reshaping modern society?",
            "answer": "AI is transforming human society by automating processes, improving decision-making, and enhancing efficiency across industries. It is embedded in everyday technologies like smartphones, virtual assistants, and predictive analytics. However, AI also raises ethical concerns about bias, privacy, and human agency, requiring careful oversight."
            },
            {
            "question": "What is the significance of the human-AI partnership?",
            "answer": "AI is not replacing humans but augmenting their abilities. Doctors use AI for diagnosing diseases, teachers personalize learning through AI tools, and businesses gain deeper insights using data-driven AI models. The key is ensuring AI remains aligned with human values and ethics."
            },
            {
            "question": "How has AI evolved from its early days to today?",
            "answer": "AI began with simple rule-based systems but advanced through machine learning, deep learning, and reinforcement learning. Breakthroughs in neural networks and computing power have enabled AI to perform complex tasks like image recognition, language processing, and autonomous navigation."
            },
            {
            "question": "What role does AI play in business innovation?",
            "answer": "AI is driving business transformation by optimizing operations, automating decision-making, and enabling personalized customer experiences. It is revolutionizing industries such as finance, retail, and manufacturing by increasing efficiency and reducing costs."
            },
            {
            "question": "How is AI impacting the workforce?",
            "answer": "AI is replacing repetitive and manual tasks but also creating new opportunities in data science, AI development, and automation. Workers must upskill in AI-related fields, and businesses should foster lifelong learning to adapt to AI-driven changes."
            },
            {
            "question": "What are the ethical concerns surrounding AI?",
            "answer": "AI raises concerns about bias, privacy, surveillance, and accountability. AI systems may inherit biases from training data, leading to unfair decisions. Transparent AI governance, ethical frameworks, and regulations are crucial to mitigate risks."
            },
            {
            "question": "How is AI transforming education?",
            "answer": "AI is personalizing education by adapting learning materials to students' needs. Virtual tutors, interactive learning platforms, and AI-driven assessment tools help improve accessibility and engagement, although concerns about digital divide persist."
            },
            {
            "question": "How is AI influencing climate change solutions?",
            "answer": "AI enhances climate monitoring, renewable energy optimization, and disaster response. AI-powered models predict environmental trends, optimize energy consumption, and develop sustainable solutions to mitigate climate impact."
            }
        ]
    },
    "book5":{
        "name":"ELITE LEADERSHIP IN THE DIGITAL AGE🙌",
        "questions":[#List of the questions
            {
        "question": "What is the core theme of 'Elite Leadership in the Digital Age'?",
        "answer": "The document explores how leadership must evolve in the digital age, focusing on adaptability, innovation, and leveraging technology to drive organizational success."
    },
    {
        "question": "How has digital transformation affected leadership?",
        "answer": "Digital transformation has reshaped leadership by necessitating a shift toward agility, data-driven decision-making, and embracing emerging technologies to stay competitive."
    },
    {
        "question": "What are the key traits of elite leaders in the digital era?",
        "answer": "Key traits include adaptability, technological proficiency, data-driven decision-making, emotional intelligence, and an innovative mindset."
    },
    {
        "question": "Why is adaptability important for leaders today?",
        "answer": "Adaptability allows leaders to respond to rapid technological advancements, market shifts, and evolving customer expectations effectively."
    },
    {
        "question": "How does data-driven decision-making enhance leadership?",
        "answer": "It enables leaders to make informed choices based on analytics, improving efficiency, reducing risks, and enhancing strategic planning."
    },
    {
        "question": "What role does emotional intelligence play in digital leadership?",
        "answer": "Emotional intelligence helps leaders build strong teams, foster collaboration, and manage the human side of digital transformation."
    },
    {
        "question": "How can leaders foster innovation within their organizations?",
        "answer": "By encouraging a culture of experimentation, supporting creative problem-solving, and investing in research and development."
    },
    {
        "question": "What challenges do leaders face in digital transformation?",
        "answer": "Challenges include resistance to change, cybersecurity threats, skills gaps, and integrating new technologies effectively."
    },
    {
        "question": "How should leaders handle resistance to digital transformation?",
        "answer": "By fostering open communication, involving employees in the process, and providing training and incentives to ease the transition."
    },
    {
        "question": "What impact does cybersecurity have on leadership responsibilities?",
        "answer": "Leaders must prioritize data protection, implement robust security policies, and ensure compliance with regulations to safeguard their organizations."
    },
    {
        "question": "How can leaders develop a digital mindset?",
        "answer": "By staying informed about technological trends, embracing continuous learning, and promoting digital literacy within the organization."
    },
    {
        "question": "What strategies can leaders use to manage remote teams effectively?",
        "answer": "Strategies include leveraging digital collaboration tools, setting clear expectations, maintaining regular communication, and fostering team cohesion."
    },
    {
        "question": "Why is ethical leadership crucial in the digital era?",
        "answer": "Ethical leadership ensures responsible use of technology, data privacy, and fairness in digital decision-making processes."
    },
    {
        "question": "How can leaders leverage artificial intelligence for better decision-making?",
        "answer": "AI can provide insights from big data, automate routine tasks, and enhance predictive analytics, helping leaders make strategic decisions."
    },
    {
        "question": "What role does customer experience play in digital leadership?",
        "answer": "Customer experience is central to digital transformation, requiring leaders to prioritize user-centric innovations and seamless digital interactions."
    },
    {
        "question": "How can leaders build digital resilience within their organizations?",
        "answer": "By preparing for disruptions, investing in robust digital infrastructure, and fostering a culture of agility and continuous improvement."
    },
    {
        "question": "What are the best practices for leading in a hybrid work environment?",
        "answer": "Best practices include clear communication, promoting work-life balance, using digital collaboration tools, and ensuring team engagement."
    },
    {
        "question": "How does digital transformation influence organizational culture?",
        "answer": "It shifts culture towards innovation, continuous learning, agility, and a more data-driven, customer-focused approach."
    },
    {
        "question": "How can leaders measure the success of digital initiatives?",
        "answer": "By setting key performance indicators (KPIs), tracking digital adoption rates, and assessing the impact on business outcomes."
    },
    {
        "question": "What is the future outlook for leadership in the digital age?",
        "answer": "The future demands leaders who embrace continuous learning, leverage emerging technologies, and foster adaptability to thrive in an ever-evolving digital landscape."
    }]
    },
    "FAQ's":{
        "name": 'FAQS',
        "questions":[#List of the questions
            {
            "question": "Who is Charles Antony?",
            "answer": "Charles Antony is a distinguished technology leader with over 40 years of global experience across telecommunications, healthcare, and corporate leadership. He played a pivotal role in pioneering cellular wireless technology at Motorola USA and has led multiple business transformations."
            },
            {
            "question": "What were Charles Antony’s key contributions at Motorola?",
            "answer": "At Motorola, Charles Antony was a pioneer in introducing cellular wireless technology globally. He was a member of the prestigious 'Leaders Lab' program, led the global Y2K deployment team, and managed a Motorola-Cisco joint venture in the wireless segment while working with major telecom operators like Vodafone, Sprint, China Unicom, and Verizon."
            },
            {
            "question": "How did Charles Antony impact Tata Infotech?",
            "answer": "As COO and President of Tata Infotech, Charles Antony orchestrated a major turnaround, increasing revenue from $37M to $200M in 18 months. He achieved a 960% growth in profit after tax, led the company to SEI CMM Level 5 certification, and elevated Tata Infotech's EVA rating from 80th to 4th place in the Tata Group."
            },
            {
            "question": "What was his role at Tata Teleservices Limited?",
            "answer": "As CEO, MD, and Board Member of Tata Teleservices Limited, Charles Antony introduced India's first data card solution, achieved 75x growth in operating profit, and led the company to the #1 position in customer satisfaction. He also significantly reduced the cost per subscriber and achieved positive EBITDA for ten consecutive quarters."
            },
            {
            "question": "What entrepreneurial ventures has Charles Antony been involved in?",
            "answer": "Charles Antony co-founded LifeNet Limited, working closely with former President of India, Dr. Abdul Kalam. He developed the 108 Ambulance service, serving over 500 million people. He was also an advisor to Apollo Hospitals through HealthNet Global Limited, where he pioneered mobile telemedicine solutions for rural India."
            },
            {
            "question": "What are his contributions to healthcare technology?",
            "answer": "Charles Antony has been an innovator in healthcare IT, leading HealthNet Global Limited to win 'Company of the Year 2011' by Frost & Sullivan. He developed the first mobile-to-mobile telemedicine solution in India, helping rural communities access medical care."
            },
            {
            "question": "What leadership roles has Charles Antony held?",
            "answer": "Charles Antony has held leadership roles across multiple industries, including Chairman and Founder of CorpArete Consulting, Council Member at Gerson & Lehrman Group, Advisor to Guidepoint Global Advisors, and Startup Mentor & Advisor to T-Works, Telangana Government."
            },
            {
            "question": "What academic roles has Charles Antony held?",
            "answer": "Charles Antony has been a Visiting Professor at prestigious institutions such as the Indian School of Business (ISB), Woxsen School of Business, IBS, and Symbiosis. He contributes to leadership development and business strategy education."
            },
            {
            "question": "What are Charles Antony’s areas of expertise?",
            "answer": "His key areas of expertise include Operational Excellence, Business Turnaround Strategy, Leadership Development, Product Management, Go-to-Market Strategy, Corporate Strategy, Healthcare Technology, Telecommunications, and Startup Mentorship."
            },
            {
            "question": "What is Charles Antony’s current role?",
            "answer": "Charles Antony currently serves as a Council Member at Gerson & Lehrman Group, an Advisor at Guidepoint Global Advisors, and a mentor for startups. He also advises T-Works under the Telangana Government, supporting innovation and entrepreneurship."
            }


        ]
    }
}

# -------------------- Keyboard Generators --------------------
def generate_main_menu():
    keyboard = []
    for category_id, category in QA_CATEGORIES.items():
        keyboard.append(
            [InlineKeyboardButton(category["name"], callback_data=f"cat_{category_id}")]
        )
    keyboard.append([InlineKeyboardButton("❓ Help", callback_data="help")])
    return InlineKeyboardMarkup(keyboard)

def generate_category_menu(category_id):
    keyboard = []
    category = QA_CATEGORIES.get(category_id)
    
    if category:
        # Iterate through the LIST of questions using enumerate()
        for index, question in enumerate(category["questions"]):
            keyboard.append(
                [
                    InlineKeyboardButton(
                        question["question"], 
                        callback_data=f"q_{category_id}_{index}"  # Use index, not q_id
                    )
                ]
            )
        
        keyboard.append([InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")])
    
    return InlineKeyboardMarkup(keyboard)

# -------------------- Handlers --------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f"Welcome to the world of books {update.effective_user.first_name}! Choose a category:",
        reply_markup=generate_main_menu()
    )

async def send_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message to new group members"""
    for new_member in update.message.new_chat_members:
        # Ignore the bot itself
        if new_member.id == context.bot.id:
            continue
        
        group_id = update.effective_chat.id
        first_name = new_member.first_name
        
        # Get custom message or use default
        welcome_message = GROUP_WELCOMES.get(group_id, 
            f"👋 Welcome {first_name} to the group! 🎉\n"
            "Please read the rules and introduce yourself!"
        )

        await context.bot.send_message(
            chat_id=group_id,
            text=welcome_message,
            parse_mode="HTML"
        )

async def set_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Let admins set a temporary welcome message (not persisted)"""
    # Check if user is admin
    user = update.effective_user
    chat = update.effective_chat
    
    admins = await chat.get_administrators()
    if user.id not in [admin.user.id for admin in admins]:
        await update.message.reply_text("❌ Only admins can use this command!")
        return
    
    # Store message in memory (will reset on bot restart)
    welcome_message = " ".join(context.args)
    GROUP_WELCOMES[chat.id] = welcome_message
    
    await update.message.reply_text(
        "✅ Temporary welcome message set!\n"
        "Use placeholders: {first_name}, {group_name}\n"
        "Example: /setwelcome Welcome {first_name}!"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = """
    📖 Help Guide:
    
    - Use main menu categories to find topics
    - Click questions to see answers
    - Use 'Back' buttons to navigate
    - /start - Restart the menu
    - /help - Show this message
    """
    await update.message.reply_text(help_text)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "help":
        await help_command(update, context)
        await query.message.reply_text("Choose a category:", reply_markup=generate_main_menu())
    elif data == "main_menu":
        await query.edit_message_text("Main Menu:", reply_markup=generate_main_menu())
    elif data.startswith("cat_"):
        category_id = data.split("_")[1]
        await query.edit_message_text(
            text=f"Category: {QA_CATEGORIES[category_id]['name']}",
            reply_markup=generate_category_menu(category_id)
        )
    elif data.startswith("q_"):
        # Split into category ID and question INDEX (not q_id)
        _, category_id, q_index = data.split("_")
        q_index = int(q_index)  # Convert string to integer
        
        # Access the question from the LIST using the index
        question = QA_CATEGORIES[category_id]["questions"][q_index]
        
        answer_text = f"❓ {question['question']}\n\n📢 {question['answer']}"
        await query.edit_message_text(
            text=answer_text,
            reply_markup=generate_main_menu()
        )
    else:
        await query.edit_message_text(text="Invalid selection")

# -------------------- Main Setup --------------------
def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(
        filters.ChatType.GROUPS & filters.StatusUpdate.NEW_CHAT_MEMBERS,
        send_welcome
    ))
    application.add_handler(CommandHandler("setwelcome", set_welcome))

    application.run_polling()

if __name__ == '__main__':
    main()