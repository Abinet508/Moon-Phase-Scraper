
from playwright.async_api import Playwright, async_playwright
from playwright_stealth import stealth
import pandas as pd, os, asyncio, time, datetime,requests,datetime
from requests_html import HTML
from multiprocessing.pool import ThreadPool

class MoonPhases:
    """
    MoonPhases class is used to scrape the moon phases data from the website https://aa.usno.navy.mil/data/MoonPhases
    
    """
    def __init__(self) -> None:
        """
        This function is used to initialize the variables
        """
        # Get the current path of the file
        self.current_path = os.path.abspath(os.path.dirname(__file__))
        # Initialize the worksheet as an empty DataFrame
        self.worksheet = pd.DataFrame()
        self.directory = "MoonPhases"
        self.file_name = "MoonPhases_worksheet.xlsx"
        # Get the file path for the directory
        self.file_path = os.path.join(self.current_path,self.directory)
        self.current_url = "https://aa.usno.navy.mil/data/MoonPhases"
        # Create the directory if it does not exist
        os.makedirs(self.file_path, exist_ok=True)
        # Get the current year from the datetime module
        self.current_year = datetime.datetime.now().year
        # Initialize the cookies for the request
        self.cookies = {
    'session': ''}
        # Get the headers for the request
        self.headers = self.get_headers()
        
    def get_headers(self) -> None:
        """
        This function is used to get the headers for the request

        Returns:
            dict: headers for the request
        """
        return {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'accept-language': 'en-US,en;q=0.5',
            'priority': 'u=0, i',
            'referer': 'https://aa.usno.navy.mil/data/MoonPhases',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Brave";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'sec-gpc': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        }
    
    async def main(self) -> None:
        """
        This function is used to call the run function using the async_playwright context manager
    
        """
        # Create an async_playwright context manager
        async with async_playwright() as playwright:
            # Call the run function using the playwright context manager
            await self.run(playwright)
    
    def scrape_data(self, year: int) -> None:
        """
        This function is used to scrape the data from the website https://aa.usno.navy.mil/calculated/moon/phases

        Args:
            year (int): year for which the data needs to be scraped from the website
        
        Returns:
            list: list of dictionaries containing the scraped data
        """
        # Initialize the parameters for the request to the website
        params = {
    'date': f'{year}-01-01', # Start date of the year in the format YYYY-MM-DD
    'nump': '50', # Number of phases to display
    'format': 'p',
    'submit': 'Get Data',
}     
        while True:
            try:
                # Send a get request to the website and get the response
                response = requests.get('https://aa.usno.navy.mil/calculated/moon/phases', params=params, cookies=self.cookies, headers=self.headers,stream=True)
                # Get the content of the response
                content = response.content
                # Iterate over the content and get the chunks
                for chunk in response.iter_content(chunk_size=1024):
                    # Append the chunks to the content
                    content += chunk
                # Parse the content using the HTML parser
                html = HTML(html=content)
                # Get the table from the html
                table = html.find("table")[0]
                # Get the headers from the table
                headers = table.find("tr")[1].text.split("\n")
                # Initialize the final data and td_data
                td_data, final_data = [],[]
                # Iterate over the td in the table
                for td in table.find("td"):
                    # Get the text from the td
                    data = td.text
                    # Append the data to the td_data
                    td_data.append(data)
                    # Check if the length of the td_data is divisible by the length of the headers
                    if len(td_data) % len(headers) == 0:
                        # Append the data to the final_data
                        final_data.append(dict(zip(headers, td_data)))
                        # Clear the td_data
                        td_data = []
                # Return the final data
                return final_data
            
            except Exception as e:
                print("Error in scrape_data",e.__str__())
                time.sleep(5)
                continue
            
    async def run(self,playwright: Playwright) -> None:
       
        """
        This function is used to run the browser and scrape the data from the website https://aa.usno.navy.mil/data/MoonPhases
        
        Args:
            playwright (Playwright): Playwright object containing the browser instances
        """
        
        # Create a new browser context with stealth enabled and launch the browser in full screen mode with kiosk mode enabled
        browser = await playwright.firefox.launch(headless=False,
        ignore_default_args=[ "--no-startup-window"],
        args=["--kiosk"],)
        # Create a new context with no viewport and storage state if it exists
        if os.path.exists(os.path.join(self.current_path, "CREDENTIALS", "storage_state.json")):
            # Create a new context with storage state
            context = await browser.new_context(storage_state=os.path.join(self.current_path, "CREDENTIALS", "storage_state.json"),
        no_viewport=True)
        else:
            # Create a new context with no viewport
            context = await browser.new_context(
        no_viewport=True)
        # Create a new page in the context
        page = await context.new_page()
        # Enable stealth mode for the page
        await stealth.stealth_async(page)
        # Go to the current url and wait until fully loaded
        await page.goto(self.current_url,wait_until="load",timeout=3000000)
        # Get the current title of the page
        current_title = await page.title()
        # Wait until the title of the page is "Dates of Primary Phases of the Moon"
        while "Dates of Primary Phases of the Moon" not in current_title:
            time.sleep(5)
        cookies = await context.cookies()
        # Get the session cookie from the cookies
        for cookie in cookies:
           if cookie["name"] == "session":
                self.cookies["session"] = cookie["value"]
                break
        # Close the browser context
        await browser.close()
        
        # Scrape the data from the website using ThreadPool
        with ThreadPool(10) as pool:
            # Scrape the data for the years from 2000 to the current year
            results = pool.map(self.scrape_data, range(2000, self.current_year+1))
        for result in results:
            # Convert the scraped data into a DataFrame and save it to an excel file
            if self.worksheet.empty:
                # Create a new dataframe if the worksheet is empty
                self.worksheet = pd.DataFrame(result)
            else:
                # Concatenate the dataframes into a single dataframe
                self.worksheet = pd.concat([self.worksheet, pd.DataFrame(result)], ignore_index=True)
        
        # Save the dataframe to an excel file
        self.worksheet.to_excel(os.path.join(self.file_path, self.file_name), index=False)

if __name__ == "__main__":
    # Create an instance of the MoonPhases class
    moon_phase = MoonPhases()
    # Run the main function using the asyncio.run function
    asyncio.run(moon_phase.main())

