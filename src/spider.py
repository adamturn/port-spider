"""
Python 3.7
Author: Adam Turner <turner.adch@gmail.com>
"""

# python package index
import requests
# standard library
import datetime


class Spider(object):

    def __init__(self):
        self.header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0"}
        self.s = requests.Session()

    def __current_date(self):
        return datetime.datetime.today()

    def __http_get(self, url):
        """Sends an HTTP GET request.

        Args:
            url: normal string url

        Returns:
            r: requests response object

        Raises:
            ValueError: when r yields a non-200 status code
        """
        r = self.s.get(url=url, headers=self.header)
        msg = f"GET response status code: {r.status_code}, url: {r.url}"
        if r.status_code == 200:
            print(msg)
            return r
        else:
            raise ValueError(msg)

    def crawl(self, data_dir, date='today'):
        """Crawls url and returns absolute str path to downloaded data.

        Args:
            data_dir: pathlib Path to the /data directory at the project root.
            date: datetime.date object, default behavior for 'today'

        Returns:
            file_path: str path to the downloaded file
        """
        if date == 'today':
            date = self.__current_date()
        date_str = date.strftime("%m-%d-%Y")
        file_name = f"Vessel-Arrival-Chart-{date_str}"
        extensions = [".pdf", ".xlsx"]
        for file_type in extensions:
            print(f"Requesting {file_name}{file_type}...")
            url = f"https://www.portofbrownsville.com/wp-content/uploads/{date.year}/{date.month}/{file_name}{file_type}"
            try:
                response = self.__http_get(url)
            except ValueError as e:
                print(e)                
                continue
            else:
                file_path = data_dir / str(file_name + file_type)
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                    return str(file_path)
