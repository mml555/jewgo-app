# ORB Web Scraping Process Documentation

## 🕷️ Overview

The ORB (Orthodox Union) web scraping system is a comprehensive data collection pipeline designed to extract kosher restaurant information from the ORB Kosher website. This document details the architecture, implementation, and maintenance procedures for the scraping system.

---

## 🏗️ System Architecture

### Technology Stack
- **Python 3.11**: Core scraping language
- **BeautifulSoup4**: HTML parsing and extraction
- **Selenium WebDriver**: Dynamic content handling
- **Requests**: HTTP client for static content
- **PostgreSQL**: Data storage and management
- **SQLAlchemy**: Database ORM
- **Logging**: Comprehensive error tracking

### Scraping Strategy
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Static HTML   │    │   JavaScript    │    │   API Calls     │
│   Scraping      │    │   Rendering     │    │   (Fallback)    │
│                 │    │                 │    │                 │
│ • BeautifulSoup │    │ • Selenium      │    │ • Direct API    │
│ • Fast parsing  │    │ • Full browser  │    │ • JSON data     │
│ • Basic data    │    │ • Dynamic content│   │ • Structured    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Data Pipeline │
                    │                 │
                    │ • Validation    │
                    │ • Cleaning      │
                    │ • Enrichment    │
                    │ • Storage       │
                    └─────────────────┘
```

---

## 🔧 Core Components

### Main Scraper (`orb_kosher_scraper.py`)

#### **Class Structure**
```python
class ORBKosherScraper:
    def __init__(self, base_url: str, db_manager: DatabaseManager):
        self.base_url = base_url
        self.db_manager = db_manager
        self.session = requests.Session()
        self.driver = None
        
    def scrape_all_categories(self) -> List[Dict[str, Any]]:
        """Scrape all restaurant categories"""
        
    def scrape_orb_category(self, category_url: str, category_name: str) -> List[Dict[str, Any]]:
        """Scrape restaurants from a specific category"""
        
    def extract_restaurant_data(self, element) -> Dict[str, Any]:
        """Extract restaurant data from HTML element"""
        
    def process_restaurant_page(self, detail_url: str) -> Dict[str, Any]:
        """Process individual restaurant detail page"""
```

#### **Key Methods**

**Category Discovery**
```python
def get_category_urls(self) -> List[Dict[str, str]]:
    """Discover all available restaurant categories"""
    categories = [
        {'name': 'Restaurants', 'url': f"{self.base_url}/category/restaurants/"},
        {'name': 'Bakeries', 'url': f"{self.base_url}/category/bakeries/"},
        {'name': 'Catering', 'url': f"{self.base_url}/category/catering/"},
        {'name': 'Markets', 'url': f"{self.base_url}/category/markets/"},
        # Additional categories...
    ]
    return categories
```

**Pagination Handling**
```python
def scrape_orb_category(self, category_url: str, category_name: str = "Restaurant") -> List[Dict[str, Any]]:
    """Scrape all restaurants from a category page with pagination"""
    all_data = []
    page_num = 1
    
    while True:
        page_url = f"{category_url}?page={page_num}"
        logger.info(f"Scraping page {page_num} of {category_name}")
        
        try:
            page_data = self.scrape_category_page(page_url)
            if not page_data:
                break
                
            all_data.extend(page_data)
            page_num += 1
            
            # Rate limiting
            time.sleep(2)
            
        except Exception as e:
            logger.error(f"Error scraping page {page_num}: {e}")
            break
    
    return all_data
```

**Data Extraction**
```python
def extract_restaurant_data(self, element) -> Dict[str, Any]:
    """Extract restaurant information from HTML element"""
    try:
        name = element.find('h3', class_='restaurant-name').text.strip()
        address = element.find('div', class_='address').text.strip()
        phone = element.find('div', class_='phone').text.strip()
        
        # Extract kosher information
        kosher_info = element.find('div', class_='kosher-info')
        certifying_agency = kosher_info.find('span', class_='agency').text.strip()
        kosher_type = kosher_info.find('span', class_='type').text.strip()
        
        return {
            'name': name,
            'address': address,
            'phone': phone,
            'certifying_agency': certifying_agency,
            'kosher_type': kosher_type,
            'detail_url': element.find('a')['href']
        }
    except Exception as e:
        logger.error(f"Error extracting restaurant data: {e}")
        return None
```

### Selenium Scraper (`selenium_orb_scraper.py`)

#### **Dynamic Content Handling**
```python
class SeleniumORBScraper:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        
    def setup_driver(self):
        """Initialize Chrome WebDriver"""
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.implicitly_wait(10)
        
    def scrape_with_selenium(self, url: str) -> List[Dict[str, Any]]:
        """Scrape content that requires JavaScript rendering"""
        try:
            self.driver.get(url)
            
            # Wait for dynamic content to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "restaurant-card"))
            )
            
            # Extract data from rendered page
            elements = self.driver.find_elements(By.CLASS_NAME, "restaurant-card")
            return [self.extract_data_from_element(element) for element in elements]
            
        except Exception as e:
            logger.error(f"Selenium scraping error: {e}")
            return []
```

### Data Processing Pipeline

#### **Data Validation**
```python
def validate_restaurant_data(data: Dict[str, Any]) -> bool:
    """Validate extracted restaurant data"""
    required_fields = ['name', 'address', 'certifying_agency']
    
    for field in required_fields:
        if not data.get(field):
            logger.warning(f"Missing required field: {field}")
            return False
    
    # Validate kosher category
    valid_categories = ['meat', 'dairy', 'pareve', 'fish', 'unknown']
    if data.get('kosher_category') and data['kosher_category'] not in valid_categories:
        logger.warning(f"Invalid kosher category: {data['kosher_category']}")
        data['kosher_category'] = 'unknown'
    
    return True
```

#### **Data Cleaning**
```python
def clean_restaurant_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Clean and standardize restaurant data"""
    cleaned = {}
    
    # Clean name
    cleaned['name'] = data.get('name', '').strip()
    
    # Parse and clean address
    address_parts = parse_address(data.get('address', ''))
    cleaned['address'] = address_parts.get('street', '')
    cleaned['city'] = address_parts.get('city', '')
    cleaned['state'] = address_parts.get('state', '')
    cleaned['zip_code'] = address_parts.get('zip', '')
    
    # Clean phone number
    cleaned['phone_number'] = format_phone_number(data.get('phone', ''))
    
    # Clean website URL
    cleaned['website'] = normalize_url(data.get('website', ''))
    
    # Standardize kosher information
    cleaned['certifying_agency'] = standardize_agency(data.get('certifying_agency', ''))
    cleaned['kosher_category'] = standardize_kosher_category(data.get('kosher_category', ''))
    
    return cleaned
```

#### **Data Enrichment**
```python
def enrich_restaurant_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Add additional information to restaurant data"""
    enriched = data.copy()
    
    # Add geolocation
    if data.get('address') and data.get('city') and data.get('state'):
        coords = geocode_address(f"{data['address']}, {data['city']}, {data['state']}")
        if coords:
            enriched['latitude'] = coords['lat']
            enriched['longitude'] = coords['lng']
    
    # Add Google listing URL
    google_url = find_google_listing(data['name'], data['address'], data['city'])
    if google_url:
        enriched['google_listing_url'] = google_url
    
    # Add Chalav Yisrael information
    if data.get('kosher_category') == 'dairy':
        enriched['is_cholov_yisroel'] = determine_chalav_yisrael(data.get('certifying_agency', ''))
    
    return enriched
```

---

## 📊 Data Extraction Patterns

### HTML Structure Analysis
```html
<!-- Restaurant Card Structure -->
<div class="restaurant-card">
    <h3 class="restaurant-name">Restaurant Name</h3>
    <div class="restaurant-info">
        <div class="address">123 Main St, City, State</div>
        <div class="phone">(555) 123-4567</div>
        <div class="website">
            <a href="http://restaurant.com">Visit Website</a>
        </div>
    </div>
    <div class="kosher-info">
        <span class="agency">ORB</span>
        <span class="type">Dairy</span>
        <span class="extra-info">Chalav Yisrael</span>
    </div>
</div>
```

### CSS Selectors
```python
SELECTORS = {
    'restaurant_cards': '.restaurant-card',
    'name': '.restaurant-name',
    'address': '.address',
    'phone': '.phone',
    'website': '.website a',
    'certifying_agency': '.kosher-info .agency',
    'kosher_type': '.kosher-info .type',
    'extra_kosher_info': '.kosher-info .extra-info',
    'pagination': '.pagination .next',
    'detail_link': '.restaurant-card a'
}
```

### Data Extraction Functions
```python
def extract_name(element) -> str:
    """Extract restaurant name"""
    name_elem = element.select_one(SELECTORS['name'])
    return name_elem.text.strip() if name_elem else ''

def extract_address(element) -> str:
    """Extract restaurant address"""
    addr_elem = element.select_one(SELECTORS['address'])
    return addr_elem.text.strip() if addr_elem else ''

def extract_phone(element) -> str:
    """Extract phone number"""
    phone_elem = element.select_one(SELECTORS['phone'])
    return phone_elem.text.strip() if phone_elem else ''

def extract_kosher_info(element) -> Dict[str, str]:
    """Extract kosher certification information"""
    kosher_elem = element.select_one('.kosher-info')
    if not kosher_elem:
        return {}
    
    agency_elem = kosher_elem.select_one('.agency')
    type_elem = kosher_elem.select_one('.type')
    extra_elem = kosher_elem.select_one('.extra-info')
    
    return {
        'certifying_agency': agency_elem.text.strip() if agency_elem else '',
        'kosher_type': type_elem.text.strip() if type_elem else '',
        'extra_kosher_info': extra_elem.text.strip() if extra_elem else ''
    }
```

---

## 🔄 Scraping Workflow

### Complete Scraping Process
```python
def run_complete_scrape():
    """Execute complete ORB scraping process"""
    logger.info("Starting ORB scraping process")
    
    # Initialize components
    scraper = ORBKosherScraper(BASE_URL, db_manager)
    selenium_scraper = SeleniumORBScraper()
    
    try:
        # 1. Discover categories
        categories = scraper.get_category_urls()
        logger.info(f"Found {len(categories)} categories")
        
        all_restaurants = []
        
        # 2. Scrape each category
        for category in categories:
            logger.info(f"Scraping category: {category['name']}")
            
            try:
                # Try static scraping first
                restaurants = scraper.scrape_orb_category(
                    category['url'], 
                    category['name']
                )
                
                # Fallback to Selenium if needed
                if not restaurants:
                    logger.info(f"Static scraping failed, trying Selenium for {category['name']}")
                    restaurants = selenium_scraper.scrape_with_selenium(category['url'])
                
                all_restaurants.extend(restaurants)
                
            except Exception as e:
                logger.error(f"Error scraping category {category['name']}: {e}")
                continue
        
        # 3. Process and validate data
        processed_restaurants = []
        for restaurant in all_restaurants:
            if validate_restaurant_data(restaurant):
                cleaned = clean_restaurant_data(restaurant)
                enriched = enrich_restaurant_data(cleaned)
                processed_restaurants.append(enriched)
        
        # 4. Store in database
        db_manager.batch_insert_restaurants(processed_restaurants)
        
        logger.info(f"Scraping completed. Processed {len(processed_restaurants)} restaurants")
        
    except Exception as e:
        logger.error(f"Scraping process failed: {e}")
        raise
    finally:
        # Cleanup
        if selenium_scraper.driver:
            selenium_scraper.driver.quit()
```

### Incremental Scraping
```python
def run_incremental_scrape():
    """Run incremental scraping to update existing data"""
    logger.info("Starting incremental ORB scraping")
    
    # Get last scrape timestamp
    last_scrape = db_manager.get_last_scrape_timestamp()
    
    # Get recently updated restaurants from ORB
    recent_restaurants = scraper.get_recently_updated(last_scrape)
    
    # Update existing records
    for restaurant in recent_restaurants:
        existing = db_manager.get_restaurant_by_name_and_address(
            restaurant['name'], 
            restaurant['address']
        )
        
        if existing:
            # Update existing record
            db_manager.update_restaurant(existing['id'], restaurant)
        else:
            # Insert new record
            db_manager.insert_restaurant(restaurant)
```

---

## 🛡️ Error Handling & Resilience

### Retry Mechanism
```python
def scrape_with_retry(url: str, max_retries: int = 3) -> Optional[BeautifulSoup]:
    """Scrape URL with retry mechanism"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
            
        except requests.RequestException as e:
            logger.warning(f"Attempt {attempt + 1} failed for {url}: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                logger.error(f"All attempts failed for {url}")
                return None
```

### Rate Limiting
```python
class RateLimiter:
    def __init__(self, requests_per_minute: int = 30):
        self.requests_per_minute = requests_per_minute
        self.requests = []
    
    def wait_if_needed(self):
        """Wait if rate limit would be exceeded"""
        now = time.time()
        
        # Remove requests older than 1 minute
        self.requests = [req_time for req_time in self.requests if now - req_time < 60]
        
        if len(self.requests) >= self.requests_per_minute:
            sleep_time = 60 - (now - self.requests[0])
            if sleep_time > 0:
                logger.info(f"Rate limit reached, waiting {sleep_time:.2f} seconds")
                time.sleep(sleep_time)
        
        self.requests.append(now)
```

### Data Validation
```python
def validate_scraped_data(data: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[str]]:
    """Validate scraped data and return valid records and errors"""
    valid_records = []
    errors = []
    
    for i, record in enumerate(data):
        try:
            # Required field validation
            if not record.get('name'):
                errors.append(f"Record {i}: Missing restaurant name")
                continue
            
            if not record.get('address'):
                errors.append(f"Record {i}: Missing address")
                continue
            
            # Data type validation
            if not isinstance(record.get('name'), str):
                errors.append(f"Record {i}: Invalid name type")
                continue
            
            # Business logic validation
            if record.get('kosher_category') not in ['meat', 'dairy', 'pareve', 'fish', 'unknown']:
                record['kosher_category'] = 'unknown'
            
            valid_records.append(record)
            
        except Exception as e:
            errors.append(f"Record {i}: Validation error - {e}")
    
    return valid_records, errors
```

---

## 📈 Monitoring & Analytics

### Scraping Metrics
```python
class ScrapingMetrics:
    def __init__(self):
        self.start_time = time.time()
        self.restaurants_scraped = 0
        self.errors_encountered = 0
        self.categories_processed = 0
        self.pages_processed = 0
    
    def log_restaurant_scraped(self):
        self.restaurants_scraped += 1
    
    def log_error(self):
        self.errors_encountered += 1
    
    def log_category_processed(self):
        self.categories_processed += 1
    
    def log_page_processed(self):
        self.pages_processed += 1
    
    def get_summary(self) -> Dict[str, Any]:
        duration = time.time() - self.start_time
        return {
            'duration_seconds': duration,
            'restaurants_scraped': self.restaurants_scraped,
            'errors_encountered': self.errors_encountered,
            'categories_processed': self.categories_processed,
            'pages_processed': self.pages_processed,
            'restaurants_per_minute': (self.restaurants_scraped / duration) * 60,
            'error_rate': self.errors_encountered / max(self.restaurants_scraped, 1)
        }
```

### Logging Configuration
```python
import logging
import logging.handlers

def setup_logging():
    """Configure comprehensive logging for scraping process"""
    logger = logging.getLogger('orb_scraper')
    logger.setLevel(logging.INFO)
    
    # File handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        'orb_scraper.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger
```

---

## 🔧 Maintenance & Updates

### Regular Maintenance Tasks
```python
def perform_maintenance():
    """Perform regular maintenance tasks"""
    logger.info("Starting maintenance tasks")
    
    # 1. Clean up old log files
    cleanup_old_logs()
    
    # 2. Update user agents
    update_user_agents()
    
    # 3. Validate database integrity
    validate_database_integrity()
    
    # 4. Update scraping patterns
    update_scraping_patterns()
    
    logger.info("Maintenance tasks completed")

def cleanup_old_logs():
    """Remove log files older than 30 days"""
    import os
    from datetime import datetime, timedelta
    
    log_dir = "logs"
    cutoff_date = datetime.now() - timedelta(days=30)
    
    for filename in os.listdir(log_dir):
        filepath = os.path.join(log_dir, filename)
        if os.path.isfile(filepath):
            file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
            if file_time < cutoff_date:
                os.remove(filepath)
                logger.info(f"Removed old log file: {filename}")
```

### Pattern Updates
```python
def update_scraping_patterns():
    """Update CSS selectors and patterns based on website changes"""
    # Test current selectors
    test_url = "https://www.orbkosher.com/category/restaurants/"
    
    try:
        soup = BeautifulSoup(requests.get(test_url).content, 'html.parser')
        
        # Test each selector
        selectors_to_test = [
            '.restaurant-card',
            '.restaurant-name',
            '.address',
            '.phone',
            '.kosher-info'
        ]
        
        for selector in selectors_to_test:
            elements = soup.select(selector)
            if not elements:
                logger.warning(f"Selector '{selector}' returned no elements")
            else:
                logger.info(f"Selector '{selector}' found {len(elements)} elements")
                
    except Exception as e:
        logger.error(f"Error testing selectors: {e}")
```

---

## 🚀 Performance Optimization

### Parallel Processing
```python
import concurrent.futures
from typing import List, Dict, Any

def scrape_categories_parallel(categories: List[Dict[str, str]], max_workers: int = 3) -> List[Dict[str, Any]]:
    """Scrape multiple categories in parallel"""
    all_restaurants = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit scraping tasks
        future_to_category = {
            executor.submit(scrape_single_category, category): category 
            for category in categories
        }
        
        # Collect results
        for future in concurrent.futures.as_completed(future_to_category):
            category = future_to_category[future]
            try:
                restaurants = future.result()
                all_restaurants.extend(restaurants)
                logger.info(f"Completed scraping {category['name']}: {len(restaurants)} restaurants")
            except Exception as e:
                logger.error(f"Error scraping {category['name']}: {e}")
    
    return all_restaurants
```

### Caching
```python
import hashlib
import pickle
import os

class ScrapingCache:
    def __init__(self, cache_dir: str = "cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def get_cache_key(self, url: str) -> str:
        """Generate cache key for URL"""
        return hashlib.md5(url.encode()).hexdigest()
    
    def get_cached_data(self, url: str) -> Optional[Dict[str, Any]]:
        """Retrieve cached data for URL"""
        cache_key = self.get_cache_key(url)
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.pkl")
        
        if os.path.exists(cache_file):
            # Check if cache is fresh (less than 1 hour old)
            if time.time() - os.path.getmtime(cache_file) < 3600:
                try:
                    with open(cache_file, 'rb') as f:
                        return pickle.load(f)
                except Exception as e:
                    logger.warning(f"Error loading cache: {e}")
        
        return None
    
    def cache_data(self, url: str, data: Dict[str, Any]):
        """Cache data for URL"""
        cache_key = self.get_cache_key(url)
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.pkl")
        
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(data, f)
        except Exception as e:
            logger.warning(f"Error caching data: {e}")
```

---

## 🔮 Future Enhancements

### Planned Improvements
- **Machine Learning**: Intelligent pattern recognition for website changes
- **Real-time Monitoring**: Live monitoring of scraping success rates
- **API Integration**: Direct API access when available
- **Distributed Scraping**: Multi-server scraping for better performance
- **Advanced Analytics**: Detailed scraping performance metrics

### Scalability Considerations
- **Load Balancing**: Distribute scraping across multiple servers
- **Database Optimization**: Optimize database operations for large datasets
- **Caching Strategy**: Implement Redis caching for frequently accessed data
- **Queue Management**: Use message queues for job distribution

---

*Last Updated: January 2025*
*Version: 2.0.0* 