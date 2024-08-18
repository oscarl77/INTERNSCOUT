import requests
import time
from src.job_scraper import JobScraper
from bs4 import BeautifulSoup

class BrightNetworkScraper(JobScraper):

    def __init__(self):
        pass

    def scrape_jobs_page(self, url):
        page = requests.get(url)
        if page.status_code == 404:
            # page doesnt exist
            return
        soup = BeautifulSoup(page.content, "html.parser")

        time.sleep(5)

        html_job_titles = soup.find_all('h6')
        html_job_links = soup.find_all(class_ = "result-link result-link-text js-ga-search-event card-link", href=True)
        return self.parse_content(html_job_titles, html_job_links)

    def parse_content(self, html_titles, html_links):
        """Converts raw job title and link html content into organised
        format to be displayed.

        Args:
            html_titles (str): titles corresponding to each job posting.
            html_links (str): html href links corresponding to each job posting.
        """
        titles = []
        links = []
        link_prefix = 'https://www.brightnetwork.co.uk'
        for job_title in html_titles:
            titles.append(job_title.get_text())
        for job_link in html_links:
            links.append(link_prefix + job_link['href'])
        parsed_postings = self.convert_to_pairs(titles, links)
        return parsed_postings
        
    def convert_to_pairs(self, titles_list, links_list):
        """Given a list of job titles and a list of job title links,
        converts the two lists into a single dictionary.

        Args:
            titles_list (list): list of str of job titles.
            links_list (list): list of str of href links for specific job page.

        Returns:
            dict: dictionary has the following key:
              - 'job title' (str): job title
            and the following value:
              - 'job link' (str): url link corresponding to the job
        """
        title_link_pairs = {}
        i = 0
        while i < min(len(titles_list), len(links_list)):
            title_link_pairs[titles_list[i]] = links_list[i]
            i += 1
        return title_link_pairs