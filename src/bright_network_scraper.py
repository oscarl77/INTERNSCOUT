import requests
import time
from src.job_scraper import JobScraper
from bs4 import BeautifulSoup

class BrightNetworkScraper(JobScraper):

    def __init__(self):
        self.title_link_pairs = {}

    def scrape_jobs_page(self, number_of_pages):
        """Scrapes all internship positions from all given pages via
        html elements.

        Args:
            number_of_pages (int): the number of pages on an internship
            post site.

        Returns:
            dict: Dictionary has the following key:
              - 'job title' (str): job title
            and the following value:
              - 'job link' (str): url link corresponding to the job
        """
        for offset in range(number_of_pages):
            offset *= 10
            page = requests.get(f'https://www.brightnetwork.co.uk/search/?offset={offset}&content_types=jobs&career_path_sectors=Technology+%26+IT+Infrastructure&job_types=Internship')
            if page.status_code == 404:
                # page doesnt exist
                continue
            time.sleep(1)
            bright_network = BeautifulSoup(page.content, "html.parser")
            html_job_titles = bright_network.find_all('h6')
            html_job_links = bright_network.find_all(class_ = "result-link result-link-text js-ga-search-event card-link", href=True)
            self._parse_content(html_job_titles, html_job_links)
        return self.title_link_pairs

    def _parse_content(self, html_titles, html_links):
        """Converts raw job title and link html content into a dictionary
        of job title keys and url link values.

        Dictionary has the following key:
              - 'job title' (str): job title
            and the following value:
              - 'job link' (str): url link corresponding to the job

        Args:
            html_titles (str): titles corresponding to each job posting.
            html_links (str): html href links corresponding to each job posting.
        """
        titles_list = []
        links_list = []
        link_prefix = 'https://www.brightnetwork.co.uk'
        for job_title in html_titles:
            titles_list.append(job_title.get_text())
        for job_link in html_links:
            links_list.append(link_prefix + job_link['href'])
        self._convert_to_pairs(titles_list, links_list)
        
        
    def _convert_to_pairs(self, titles_list, links_list):
        """Given a list of job titles and a list of job links,
        converts the two lists into a single dictionary.

        Dictionary has the following key:
              - 'job title' (str): job title
            and the following value:
              - 'job link' (str): url link corresponding to the job

        Args:
            titles_list (list): list of str of job titles.
            links_list (list): list of str of href links for specific job page.
        """
        i = 0
        while i < min(len(titles_list), len(links_list)):
            self.title_link_pairs[titles_list[i]] = links_list[i]
            i += 1