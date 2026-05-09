"""
Modified and tested on 04 May 2026
This script may fail if the structure of the website changes in the future
"""
import requests
from bs4 import BeautifulSoup
import re
import os
import time

print("Script has started!")

exclusionlist = [
    '/support/home', 
    '/support/solutions', 
    '/support/login', 
    '/support/tickets/new'
]

def download_faqs(url):
    try:
        print(f"Attempting to fetch the base URL: {url}")
        response = requests.get(url)
        response.raise_for_status()
        print(f"Successfully fetched the base URL: {url}")

        soup = BeautifulSoup(response.content, 'html.parser')

        category_links = []
        category_divs = soup.find_all('div', class_='col-md-4 col-xl-3 mb-8')
        print(f"Number of category divs found: {len(category_divs)}")
        for div in category_divs:
            link = div.find('a')
            if link and link.has_attr('href'):
                category_links.append(link['href'])
        print(f"Number of category links found: {len(category_links)}")

        all_faqs = []

        for category_link in category_links:
            full_category_url = "https://fitnesspassport.freshdesk.com" + category_link
            print(f"Processing category: {full_category_url}")

            try:
                category_response = requests.get(full_category_url)
                category_response.raise_for_status()
                category_soup = BeautifulSoup(category_response.content, 'html.parser')
                print(f"Successfully fetched category: {full_category_url}")
            except requests.exceptions.RequestException as e:
                print(f"Error fetching category {full_category_url}: {e}")
                continue

            article_links = []
            article_divs = category_soup.find_all('li')
            print(f"  Number of article divs found: {len(article_divs)}")

            for div in article_divs:
                link = div.find('a')
                if link and link.has_attr('href'):
                    if link['href'] not in exclusionlist:
                        article_links.append(link['href'])
            print(f"  Number of article links found: {len(article_links)}")

            for article_link in article_links:
                full_article_url = "https://fitnesspassport.freshdesk.com" + article_link
                print(f"  Processing article: {full_article_url}")
                try:
                    article_response = requests.get(full_article_url)
                    article_response.raise_for_status()
                    article_soup = BeautifulSoup(article_response.content, 'html.parser')
                    print(f"  Successfully fetched article: {full_article_url}")
                    time.sleep(1)
                except requests.exceptions.RequestException as e:
                    print(f"  Error fetching article {full_article_url}: {e}")
                    continue

                try:
                    question_element = article_soup.find('h1', class_='fw-page-title')
                    if question_element:
                        question = question_element.get_text(strip=True)
                    else:
                        print(f"    Warning: Could not find question for {full_article_url}")
                        continue
                except Exception as e:
                    print(
                        f"    Warning: Error while getting the question for {full_article_url}, error: {e}")
                    continue

                try:
                    answer_element = article_soup.find('div', 'fw-content')
                    if answer_element:
                        answer = answer_element.get_text(strip=True)

                        answer = re.sub(r'\s+', ' ', answer)
                        answer = re.sub(r'<[^>]+>', '', answer)
                    else:
                        print(f"    Warning: Could not find answer for {full_article_url}")
                        continue
                except Exception as e:
                    print(
                        f"    Warning: Error while getting the answer for {full_article_url}, error: {e}")
                    continue

                all_faqs.append({"question": question, "answer": answer})
                print(f"Successfully extracted Question and Answer from: {full_article_url}")

        print(f"Total FAQs extracted: {len(all_faqs)}")
        if len(all_faqs) == 0:
            return None
        else:
            return all_faqs

    except requests.exceptions.ConnectionError as e:
        print(f"Connection error occurred: {e}")
        return None
    except requests.exceptions.Timeout as e:
        print(f"Timeout error occurred: {e}")
        return None
    except requests.exceptions.TooManyRedirects as e:
        print(f"Too many redirects occurred: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"A requests error occurred: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def save_faqs_to_file(faqs, filename="faqs.txt"):
    if faqs:
        try:
            if not os.path.exists("output"):
                os.makedirs("output")
            with open(os.path.join("output", filename), 'w', encoding='utf-8') as f:
                for faq in faqs:
                    f.write(f"Question: {faq['question']}\n")
                    f.write(f"Answer: {faq['answer']}\n")
                    f.write("-" * 20 + "\n")
            print(f"Successfully saved FAQs to {filename}")
        except Exception as e:
            print(f"Error saving to file: {e}")
    else:
        print("No FAQs to save.")


def save_faqs_to_json(faqs, filename="faqs.json"):
    import json

    if faqs:
        try:
            if not os.path.exists("output"):
                os.makedirs("output")

            with open(os.path.join("output", filename), 'w', encoding='utf-8') as f:
                json.dump(faqs, f, indent=4, ensure_ascii=False)
            print(f"Successfully saved FAQs to {filename}")
        except Exception as e:
            print(f"Error saving to JSON file: {e}")
    else:
        print("No FAQs to save.")


if __name__ == "__main__":
    base_url = "https://fitnesspassport.freshdesk.com/support/home"
    extracted_faqs = download_faqs(base_url)
    if extracted_faqs:
        print("Saving  to file ....")
        save_faqs_to_file(extracted_faqs)
        print("Saving  to file .... done!")
        print("-----------------------------")
        print("Saving  to JSON ..........")
        save_faqs_to_json(extracted_faqs)
        print("Saving  to JSON .... done!")
    else:
        print("Nothing to save")
