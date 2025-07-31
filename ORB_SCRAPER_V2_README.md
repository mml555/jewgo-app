# ORB Kosher Scraper V2

A comprehensive web scraper for extracting kosher business listings from ORB Kosher and storing them directly in the current database schema with proper Chalav Yisroel and Pas Yisroel categorization.

## 🎯 Features

- **Direct Database Integration**: Maps ORB data directly to current `restaurants` table schema
- **Kosher Supervision Categorization**: Automatically sets Chalav Yisroel/Stam and Pas Yisroel status
- **Web Scraping**: Uses Playwright for robust scraping of ORB Kosher website
- **Address Parsing**: Extracts city, state, and zip code from addresses
- **Duplicate Prevention**: Checks for existing restaurants to prevent duplicates
- **Error Resilience**: Robust error handling and logging
- **Python 3.11 Compatible**: Optimized for your system requirements

## 📋 Prerequisites

- Python 3.11
- Neon PostgreSQL database with current schema
- Internet connection for web scraping
- `DATABASE_URL` environment variable set

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install Playwright and browsers
pip install playwright
playwright install chromium
```

### 2. Set Environment Variables

Ensure your `.env` file contains:

```env
DATABASE_URL=postgresql://username:password@ep-something.neon.tech/dbname?sslmode=require
```

### 3. Run the Scraper

```bash
python orb_scraper_v2.py
```

## 📊 Data Mapping

The scraper maps ORB data to your current database schema:

| ORB Field | Database Field | Description |
|-----------|----------------|-------------|
| `name` | `name` | Business name |
| `address` | `address` | Street address |
| `phone` | `phone_number` | Phone number |
| `website` | `website` | Business website |
| `photo` | `image_url` | Business image |
| `kosher_type` | `kosher_category` | dairy, pareve, etc. |
| `kosher_cert_link` | `kosher_cert_link` | Kosher certificate PDF |
| - | `certifying_agency` | Set to 'ORB' |
| - | `is_cholov_yisroel` | Calculated from restaurant list |
| - | `is_pas_yisroel` | Calculated from restaurant list |

## 🥛 Chalav Yisroel/Stam Categorization

The scraper automatically categorizes dairy restaurants:

### Chalav Stam (3 restaurants only):
- Cafe 95 at JARC
- Hollywood Deli
- Sobol Boynton Beach

### Chalav Yisroel (all other dairy restaurants):
All other dairy restaurants are automatically set to Chalav Yisroel.

## 🍞 Pas Yisroel Categorization

The scraper sets Pas Yisroel status for specific restaurants:

### Pas Yisroel Restaurants (22 restaurants):
- Grand Cafe Hollywood
- Yum Berry Cafe & Sushi Bar
- Pita Xpress
- Mizrachi's Pizza in Hollywood
- Boca Grill
- Shalom Haifa
- Chill & Grill Pita Boca
- Hummus Achla Hallandale
- Jon's Place
- Levy's Shawarma
- Holy Smokes BBQ and Grill (Food Truck)
- Friendship Cafe & Catering
- Tagine by Alma Grill
- Lox N Bagel (Bagel Factory Cafe)
- Kosher Bagel Cove
- Cafe Noir
- Grill Xpress
- PX Grill Mediterranean Cuisine
- Carmela's Boca
- Ariel's Delicious Pizza
- Oak and Ember
- Rave Pizza & Sushi
- Burnt Smokehouse and Bar
- Vish Hummus Hollywood

### Regular Pas (all other meat/pareve restaurants):
All other meat/pareve restaurants are set to not Pas Yisroel.

## 🗃️ Database Schema Compatibility

The scraper is designed to work with your current `restaurants` table schema:

```sql
-- Key fields populated by the scraper
name VARCHAR(255) NOT NULL
address VARCHAR(500)
city VARCHAR(100)
state VARCHAR(50)
zip_code VARCHAR(20)
phone_number VARCHAR(50)
website VARCHAR(500)
certifying_agency VARCHAR(100) -- Set to 'ORB'
kosher_category VARCHAR(100) -- dairy, pareve, etc.
is_kosher BOOLEAN -- Set to TRUE
is_cholov_yisroel BOOLEAN -- Calculated
is_pas_yisroel BOOLEAN -- Calculated
kosher_cert_link VARCHAR(500)
image_url VARCHAR(500)
short_description TEXT
status VARCHAR(50) -- Set to 'active'
```

## 🔧 Configuration

### Chalav Stam Restaurants

To modify the Chalav Stam list, edit the `chalav_stam_restaurants` list in the scraper:

```python
self.chalav_stam_restaurants = [
    "Cafe 95 at JARC",
    "Hollywood Deli", 
    "Sobol Boynton Beach"
]
```

### Pas Yisroel Restaurants

To modify the Pas Yisroel list, edit the `pas_yisroel_restaurants` list in the scraper:

```python
self.pas_yisroel_restaurants = [
    "Grand Cafe Hollywood",
    "Yum Berry Cafe & Sushi Bar",
    # ... add more restaurants
]
```

## 📁 File Structure

```
├── orb_scraper_v2.py              # Main scraper script
├── database_manager_v3.py         # Database manager (required)
├── ORB_SCRAPER_V2_README.md       # This documentation
└── .env                           # Environment variables
```

## 🛠️ Troubleshooting

### Common Issues

1. **Database Connection Failed**
   ```
   Error: DATABASE_URL environment variable is required
   ```
   Solution: Ensure DATABASE_URL is set in your .env file

2. **Playwright Installation Failed**
   ```
   Error: playwright install failed
   ```
   Solution: Run `playwright install chromium` manually

3. **No Data Found**
   ```
   Warning: No businesses found on page
   ```
   Solution: Check if ORB website structure has changed

### Logs

The scraper provides detailed logging output showing:
- Number of restaurants scraped
- Kosher type statistics
- Chalav Yisroel/Stam statistics
- Pas Yisroel statistics
- Sample scraped businesses

## 📈 Expected Results

After running the scraper, you should see:

```
📊 Total businesses scraped: 107
🥛 Dairy restaurants: 99
🥬 Pareve restaurants: 8

🥛 Chalav Yisroel: 104
🥛 Chalav Stam: 3
🍞 Pas Yisroel: 22
```

## 🔒 Legal and Ethical Considerations

- **Rate Limiting**: Includes delays to be respectful to ORB Kosher
- **Terms of Service**: Ensure compliance with ORB Kosher's terms
- **Data Usage**: Use scraped data responsibly
- **Attribution**: Consider providing attribution to ORB Kosher

## 🚀 Deployment

The scraper is ready for production use and will:
1. Connect to your database
2. Scrape ORB Kosher website
3. Map data to your schema
4. Set proper kosher supervision status
5. Save all restaurants to database

## 📞 Support

If you encounter issues:
1. Check the console output for error messages
2. Verify your database connection
3. Ensure all dependencies are installed
4. Check that the ORB website is accessible

## 📄 License

This scraper is provided as-is for educational and development purposes. Please ensure compliance with all applicable laws and terms of service. 