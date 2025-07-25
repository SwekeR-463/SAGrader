from main import grade_essay

topic = "The Impact of Artificial Intelligence on Modern Society"

sample_essay = """
    Artificial Intelligence (AI) has become an integral part of our daily lives, 
    revolutionizing various sectors including healthcare, finance, and transportation. 
    This essay explores the profound effects of AI on modern society, discussing both 
    its benefits and potential challenges.

    One of the most significant impacts of AI is in the healthcare industry. 
    AI-powered diagnostic tools can analyze medical images with high accuracy, 
    often surpassing human capabilities. This leads to earlier detection of diseases 
    and more effective treatment plans. Moreover, AI algorithms can process vast 
    amounts of medical data to identify patterns and insights that might escape 
    human observation, potentially leading to breakthroughs in drug discovery and 
    personalized medicine.

    In the financial sector, AI has transformed the way transactions are processed 
    and monitored. Machine learning algorithms can detect fraudulent activities in 
    real-time, enhancing security for consumers and institutions alike. Robo-advisors 
    use AI to provide personalized investment advice, democratizing access to 
    financial planning services.

    The transportation industry is another area where AI is making significant strides. 
    Self-driving cars, powered by complex AI systems, promise to reduce accidents 
    caused by human error and provide mobility solutions for those unable to drive. 
    In logistics, AI optimizes routing and inventory management, leading to more 
    efficient supply chains and reduced environmental impact.

    However, the rapid advancement of AI also presents challenges. There are concerns 
    about job displacement as AI systems become capable of performing tasks 
    traditionally done by humans. This raises questions about the need for retraining 
    and reskilling the workforce to adapt to an AI-driven economy.

    Privacy and ethical concerns also arise with the increasing use of AI. The vast 
    amount of data required to train AI systems raises questions about data privacy 
    and consent. Additionally, there are ongoing debates about the potential biases 
    in AI algorithms and the need for transparent and accountable AI systems.

    In conclusion, while AI offers tremendous benefits and has the potential to solve 
    some of humanity's most pressing challenges, it also requires careful consideration 
    of its societal implications. As we continue to integrate AI into various aspects 
    of our lives, it is crucial to strike a balance between technological advancement 
    and ethical considerations, ensuring that the benefits of AI are distributed 
    equitably across society.
    """
    

# grade the sample essay
result = grade_essay(topic, sample_essay)

# display the results
print(f"Final Essay Score: {result['final_score']:.2f}\n")
print(f"Relevance Score: {result['relevance_score']:.2f}")
print(f"Grammar Score: {result['grammar_score']:.2f}")
print(f"Structure Score: {result['structure_score']:.2f}")
print(f"Depth Score: {result['depth_score']:.2f}")