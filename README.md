# MoonPhases Scraper

This script is used to scrape moon phase data from the website [USNO Moon Phases](https://aa.usno.navy.mil/data/MoonPhases) using Playwright.

## Description

The MoonPhases Scraper script automates the process of extracting moon phase data from the USNO website. It uses the Playwright library to control a web browser, navigate to the moon phases page, and scrape the required data. The script can handle browser contexts with or without stored credentials and operates in full-screen kiosk mode for an immersive scraping experience.

## Prerequisites

- Python 3.7+
- Playwright
- Node.js (for Playwright installation)

## Installation

1. **Install Python packages**:
    ```sh
    pip install playwright
    ```

2. **Install Playwright browsers**:
    ```sh
    playwright install
    ```

## Usage

To run the script, you need to have the Playwright library installed and the necessary browsers set up. The script will launch a Firefox browser in full-screen kiosk mode and scrape the moon phase data.

### Arguments

- `playwright (Playwright)`: Playwright object containing the browser instances.

### Methods

#### `run_browser_and_scrape(playwright)`

This function is used to run the browser and scrape the data from the website [USNO Moon Phases](https://aa.usno.navy.mil/data/MoonPhases).

- **Args**:
  - `playwright (Playwright)`: Playwright object containing the browser instances.

- **Functionality**:
  - Launches a Firefox browser in full-screen kiosk mode.
  - Checks if a storage state file exists for credentials.
  - Creates a new browser context with or without the storage state.
  - Navigates to the moon phases page and scrapes the data.

### Final Output

The final output of the script is the scraped moon phase data, which can be stored in a file or processed further as needed. The exact format and storage mechanism depend on the implementation details of the scraping logic.

### Example

```python
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as playwright:
        # Your script logic here
        browser = await playwright.firefox.launch(headless=False,
                                                  ignore_default_args=["--no-startup-window"],
                                                  args=["--kiosk"])
        # Additional logic to handle browser context and scraping

# Run the main function
import asyncio
asyncio.run(main())