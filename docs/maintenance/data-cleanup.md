# Data Cleanup & Management

## Overview

This guide covers data cleanup procedures, restaurant data updates, and data quality management for the JewGo application.

## 🧹 Data Cleanup Procedures

### Automated Cleanup Scripts
```bash
# Find data issues
python scripts/maintenance/find_data_issues.py

# Comprehensive database fix
python scripts/maintenance/comprehensive_database_fix.py

# Validate restaurant data
python scripts/maintenance/validate_restaurant_data.py
```

### Data Validation
- **Restaurant Data**: Verify all required fields are present
- **Kosher Information**: Validate kosher supervision details
- **Location Data**: Check coordinate accuracy
- **Contact Information**: Verify phone and website formats

## 🏪 Restaurant Data Updates

### Manual Update Procedures

#### Website Updates
```python
# Update restaurant website
def update_restaurant_website(restaurant_id, new_website_url):
    success = db_manager.update_restaurant_orb_data(
        restaurant_id=restaurant_id,
        website=new_website_url
    )
    return success

# Example usage
update_restaurant_website(207, 'https://barakehshawarma.com')
```

#### Hours Updates
```python
# Update restaurant hours
def update_restaurant_hours(restaurant_id, new_hours):
    success = db_manager.update_restaurant_orb_data(
        restaurant_id=restaurant_id,
        hours_open=new_hours
    )
    return success

# Example usage
update_restaurant_hours(45, 'Mon-Fri: 11AM-9PM, Sat: 12PM-10PM')
```

### Google Places Integration

#### Address Updates
```bash
# Update addresses using Google Places
python scripts/maintenance/google_places_address_updater.py
```

#### Hours Updates
```bash
# Update hours using Google Places
python scripts/maintenance/google_places_hours_updater.py
```

#### Description Updates
```bash
# Update descriptions using Google Places
python scripts/maintenance/google_places_description_updater.py
```

#### Image Updates
```bash
# Update images using Google Places
python scripts/maintenance/google_places_image_updater.py
```

## 📊 Data Quality Standards

### Required Fields
- **Name**: Restaurant name (required)
- **Address**: Complete address (required)
- **City**: City name (required)
- **State**: State abbreviation (required)
- **Kosher Type**: dairy, meat, pareve (required)
- **Certifying Agency**: ORB, KM, Star-K, etc. (required)

### Optional Fields
- **Phone**: Valid phone number format
- **Website**: Valid URL format
- **Email**: Valid email format
- **Hours**: Business hours format
- **Price Range**: $, $$, $$$, $$$$
- **Image URL**: Valid image URL

### Data Validation Rules
```python
# Validation examples
def validate_restaurant_data(data):
    errors = []
    
    # Required fields
    if not data.get('name'):
        errors.append('Restaurant name is required')
    
    if not data.get('address'):
        errors.append('Address is required')
    
    # Format validation
    if data.get('phone') and not is_valid_phone(data['phone']):
        errors.append('Invalid phone number format')
    
    if data.get('website') and not is_valid_url(data['website']):
        errors.append('Invalid website URL')
    
    return errors
```

## 🔄 Update Workflows

### New Restaurant Submission
1. **Data Collection**: Gather restaurant information
2. **Validation**: Check data quality and completeness
3. **Submission**: Submit to database
4. **Review**: Admin review and approval
5. **Publication**: Make restaurant visible to users

### Existing Restaurant Updates
1. **Data Verification**: Verify current data accuracy
2. **Update Collection**: Gather updated information
3. **Validation**: Validate new data
4. **Database Update**: Update restaurant record
5. **Verification**: Confirm update success

### Bulk Updates
```bash
# Update multiple restaurants
python scripts/maintenance/batch_update_remaining.py

# Update specific fields
python scripts/maintenance/perform_updates.py
```

## 📋 Data Quality Checklist

### Before Updates
- [ ] Verify data source accuracy
- [ ] Check data format compliance
- [ ] Validate required fields
- [ ] Test update procedures

### During Updates
- [ ] Monitor update progress
- [ ] Check for errors
- [ ] Verify data integrity
- [ ] Backup before major changes

### After Updates
- [ ] Verify update success
- [ ] Test data accessibility
- [ ] Check user experience
- [ ] Update documentation

## 🚨 Common Data Issues

### Missing Information
- **Hours**: 90 restaurants missing hours
- **Websites**: Some restaurants have invalid websites
- **Phone Numbers**: Missing or invalid phone numbers
- **Images**: Missing restaurant images

### Data Inconsistencies
- **Address Format**: Inconsistent address formatting
- **Phone Format**: Mixed phone number formats
- **Hours Format**: Inconsistent hours formatting
- **Kosher Information**: Missing kosher details

### Resolution Procedures
1. **Identify Issue**: Use data validation scripts
2. **Research Data**: Use Google Places API
3. **Update Database**: Use appropriate update scripts
4. **Verify Changes**: Test data accessibility
5. **Document Changes**: Update maintenance logs

## 🔧 Maintenance Scripts

### Data Validation Scripts
```bash
# Find data issues
python scripts/maintenance/find_data_issues.py

# Validate restaurant data
python scripts/maintenance/validate_restaurant_data.py

# Check data integrity
python scripts/maintenance/check_data_integrity.py
```

### Update Scripts
```bash
# Update restaurant information
python scripts/maintenance/update_restaurant_data.py

# Google Places integration
python scripts/maintenance/google_places_address_updater.py
python scripts/maintenance/google_places_hours_updater.py
python scripts/maintenance/google_places_description_updater.py
python scripts/maintenance/google_places_image_updater.py
```

### Cleanup Scripts
```bash
# Comprehensive cleanup
python scripts/maintenance/comprehensive_database_fix.py

# Data organization
python scripts/maintenance/comprehensive_final_report.py
```

## 📈 Data Quality Metrics

### Current Statistics
- **Total Restaurants**: 107
- **Complete Data**: 85%
- **Missing Hours**: 90 restaurants
- **Invalid Websites**: 1 restaurant
- **Missing Phone**: 15 restaurants

### Quality Targets
- **Data Completeness**: >95%
- **Data Accuracy**: >98%
- **Update Frequency**: Weekly
- **Validation Coverage**: 100%

## 🔐 Data Security

### Access Control
- **Admin Access**: Limited to authorized users
- **Update Logging**: All changes logged
- **Backup Procedures**: Regular data backups
- **Audit Trail**: Complete change history

### Data Protection
- **Encryption**: Sensitive data encrypted
- **Access Logs**: Monitor data access
- **Backup Security**: Secure backup storage
- **Compliance**: Follow data protection regulations

---

*For detailed update procedures, see the individual script documentation.* 