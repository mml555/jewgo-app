# ORB Kosher Scraper

A comprehensive web scraper for extracting kosher business listings from ORB Kosher and storing them in a Neon PostgreSQL database.

## 🎯 Features

- **Web Scraping**: Uses Playwright and BeautifulSoup for robust scraping
- **Database Integration**: Direct insertion into Neon PostgreSQL
- **Pagination Support**: Automatically handles multiple pages
- **Error Resilience**: Robust error handling and retry logic
- **Data Extraction**: Extracts comprehensive business information
- **Python 3.11 Compatible**: Optimized for your system requirements

## 📋 Prerequisites

- Python 3.11
- Neon PostgreSQL database
- Internet connection for web scraping

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Run the setup script
python setup_orb_scraper.py
```

The setup script will:
- Check Python version compatibility
- Install required dependencies
- Install Playwright browsers
- Create .env template if needed
- Test database connection

### 2. Configure Environment Variables

Create a `.env` file with your database credentials:

```env
# Neon PostgreSQL Database URL
DATABASE_URL=postgresql://username:password@ep-something.neon.tech/dbname?sslmode=require

# Optional: Logging level
LOG_LEVEL=INFO
```

### 3. Run the Scraper

```bash
# Run the scraper (default: 5 pages)
python orb_scraper.py
```

## 📊 Data Fields Extracted

| Field | Description |
|-------|-------------|
| `name` | Business name |
| `detail_url` | ORB detail page URL |
| `category` | Business category (Restaurant) |
| `photo` | Image URL from detail page |
| `address` | Street address |
| `phone` | Phone number |
| `website` | Business website URL |
| `kosher_cert_link` | Kosher certification link |
| `kosher_type` | General kosher type (Meat, Dairy, Parve) |
| `extra_kosher_info` | Special kosher requirements |

## 🗃️ Database Schema

The scraper creates a `kosher_places` table with the following structure:

```sql
CREATE TABLE kosher_places (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    detail_url TEXT UNIQUE,
    category TEXT,
    photo TEXT,
    address TEXT,
    phone TEXT,
    website TEXT,
    kosher_cert_link TEXT,
    kosher_type TEXT,
    extra_kosher_info TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

## 🔧 Configuration Options

### Scraper Settings

You can modify the scraper behavior by editing `orb_scraper.py`:

```python
# Change max pages to scrape
await scraper.run(max_pages=10)

# Adjust delays between requests
await asyncio.sleep(2)  # Page load delay
await asyncio.sleep(1)  # Between listings
await asyncio.sleep(3)  # Between pages
```

### Target Categories

To scrape different categories, modify the category URL:

```python
# For restaurants (default)
self.category_url = f"{self.base_url}/category/restaurants/"

# For other categories
self.category_url = f"{self.base_url}/category/bakeries/"
self.category_url = f"{self.base_url}/category/caterers/"
```

## 📁 File Structure

```
├── orb_scraper.py              # Main scraper script
├── setup_orb_scraper.py        # Setup and installation script
├── schema.sql                  # Database schema
├── orb_scraper_requirements.txt # Python dependencies
├── .env                        # Environment variables (create this)
├── .env.template               # Environment template
└── ORB_SCRAPER_README.md       # This file
```

## 🛠️ Troubleshooting

### Common Issues

1. **Python Version Error**
   ```
   Error: Python 3.11 required
   ```
   Solution: Ensure you're using Python 3.11

2. **Database Connection Failed**
   ```
   Error: connection to server failed
   ```
   Solution: Check your DATABASE_URL in .env file

3. **Playwright Installation Failed**
   ```
   Error: playwright install failed
   ```
   Solution: Run `playwright install chromium` manually

4. **No Data Found**
   ```
   Warning: No businesses found on page
   ```
   Solution: The website structure may have changed. Check the selectors in the scraper.

### Logs

The scraper creates detailed logs in `orb_scraper.log`. Check this file for debugging information.

## 🔒 Legal and Ethical Considerations

- **Rate Limiting**: The scraper includes delays to be respectful to the target website
- **Terms of Service**: Ensure you comply with ORB Kosher's terms of service
- **Data Usage**: Use scraped data responsibly and in accordance with applicable laws
- **Attribution**: Consider providing attribution to ORB Kosher for the data source

## 📈 Performance Tips

1. **Start Small**: Begin with 1-2 pages to test the setup
2. **Monitor Logs**: Watch the log file for any issues
3. **Database Indexes**: The schema includes indexes for better query performance
4. **Error Handling**: The scraper continues even if individual listings fail

## 🤝 Contributing

To improve the scraper:

1. Test with different categories
2. Improve data extraction patterns
3. Add support for additional fields
4. Optimize performance and error handling

## 📞 Support

If you encounter issues:

1. Check the logs in `orb_scraper.log`
2. Verify your database connection
3. Ensure all dependencies are installed
4. Check that the target website is accessible

## 📄 License

This scraper is provided as-is for educational and development purposes. Please ensure compliance with all applicable laws and terms of service. 