from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class Browser:
    """
    A class for fetching text from a web page using a browser. This ensures
    that any page rendering due to JavaScript is executed, and iframes
    are processed.
    """

    def __init__(self, headless=False):
        options = Options()
        if headless:
            options.add_argument("--headless=new")
        self.browser = webdriver.Chrome(options=options)

    def get(self, url) -> str:
        self.browser.get(url)
        return self._get_text()

    def _get_text(self):
        text = self.browser.find_element(By.TAG_NAME, "body").text

        # recursively get text from iframes (e.g. iframes within iframes)
        for iframe in self.browser.find_elements(By.TAG_NAME, "iframe"):
            self.browser.switch_to.frame(iframe)
            text += self._get_text()
            self.browser.switch_to.parent_frame()

        return text
