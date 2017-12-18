import dryscrape
import logging


class PcScraper(object):
    def __init__(self, url, credentials):
        logging.info("Configuring session")
        self.url = url
        self.credentials = credentials

        dryscrape.start_xvfb()

        self.session = dryscrape.Session()

        self.session.set_attribute(
            'local_content_can_access_remote_urls', True)
        self.session.set_attribute('local_storage_enabled', True)
        self.session.set_attribute('local_storage_database_enabled', True)
        self.session.set_attribute('local_content_can_access_file_urls', True)
        self.session.set_attribute('dns_prefetch_enabled', True)

        self.username_field_selector = ''
        self.password_field_selector = ''

        logging.info("Navigating to {}".format(url))
        self.session.visit(self.url)

    def enter_field(self, css_selector, value):
        username_field = self.session.at_css(css_selector)
        username_field.set(value)

    def login(self):
        self.enter_field(
            self.username_field_selector,
            self.credentials['username']
        )
        self.enter_field(
            self.password_field_selector,
            self.credentials['password']
        )
