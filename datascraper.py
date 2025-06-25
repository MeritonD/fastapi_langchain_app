
import wikipedia
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# A diverse list of topics to create a broad knowledge base
topics_to_fetch = [
    "Artificial intelligence", "Machine learning", "Deep learning",
    "Natural language processing", "Computer vision", "Reinforcement learning",
    "Generative adversarial networks", "Transformer (machine learning model)",
    "Python (programming language)", "JavaScript", "React (JavaScript library)",
    "Node.js", "Docker (software)", "Kubernetes", "Cloud computing",
    "Amazon Web Services", "Microsoft Azure", "Google Cloud Platform",
    "History of science", "Physics", "Chemistry", "Biology", "Mathematics",
    "Philosophy", "Economics", "Political science", "Sociology", "Psychology",
    "World history", "Ancient history", "Medieval history", "Modern history",
    "The Renaissance", "The Industrial Revolution", "The Information Age",
    "Climate change", "Renewable energy", "Sustainable development",
    "Electric vehicle", "Quantum computing", "Blockchain", "Cryptocurrency",
    "Internet of Things", "5G", "Augmented reality", "Virtual reality"
]

def get_wikipedia_articles(topics, file_path):
    """
    Fetches content from Wikipedia articles and saves it to a file.

    Args:
        topics (list): A list of topics to search for on Wikipedia.
        file_path (str): The path to the file where the content will be saved.
    """
    all_content = ""
    for topic in topics:
        try:
            logging.info(f"Fetching content for topic: {topic}")
            # search for the topic and get the first result
            page_title = wikipedia.search(topic, results=1)[0]
            # get the page content
            page = wikipedia.page(page_title, auto_suggest=False)
            all_content += page.content + "\n\n"
        except wikipedia.exceptions.PageError:
            logging.warning(f"Page for topic '{topic}' not found. Skipping.")
        except wikipedia.exceptions.DisambiguationError as e:
            logging.warning(f"Disambiguation page found for topic '{topic}'. Skipping. Options: {e.options}")
        except Exception as e:
            logging.error(f"An unexpected error occurred for topic '{topic}': {e}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(all_content)
    logging.info(f"Successfully saved content to {file_path}")

if __name__ == "__main__":
    output_file_path = "knowledge_base.txt"
    get_wikipedia_articles(topics_to_fetch, output_file_path)
