from abc import ABC, abstractmethod

class JobScraper(ABC):
    """Abstract class for scraping job postings from websites.

    This abstract class acts as a template for a website scraper, as 
    subclasses will be specific to each website due to differences in
    html content.
    """

    @abstractmethod
    def scrape_jobs_page(self, url):
        pass
