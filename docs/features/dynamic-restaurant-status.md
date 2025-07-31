# Dynamic Restaurant Status Implementation

## Overview

This document describes the implementation of dynamic restaurant status calculation for the JewGo application. The system calculates restaurant open/closed status in real-time based on business hours and current time, with proper timezone support.

## Key Features

### ✅ **Real-Time Status Calculation**
- Status is calculated dynamically, not stored in database
- Updates automatically based on current time
- Handles timezone differences correctly

### ✅ **Timezone Support**
- Automatic timezone detection based on restaurant location
- State-based timezone mapping for US locations
- Fallback to UTC for unknown locations

### ✅ **Flexible Hours Parsing**
- Supports multiple business hours formats
- Handles overnight hours (e.g., 6 PM - 2 AM)
- Parses 24-hour restaurants
- Graceful handling of invalid formats

### ✅ **Performance Optimized**
- Caching for repeated calculations
- Efficient regex-based parsing
- Minimal database impact

## Implementation Details

### Core Components

#### 1. RestaurantStatusCalculator Class
**Location**: `backend/utils/restaurant_status.py`

**Key Methods**:
- `get_restaurant_status()` - Main status calculation function
- `_get_timezone()` - Timezone determination
- `_parse_business_hours()` - Hours parsing
- `_check_if_open()` - Open/closed logic

#### 2. Database Integration
**Location**: `backend/database/database_manager_v3.py`

**Changes Made**:
- Updated `_restaurant_to_unified_dict()` method
- Integrated dynamic status calculation
- Added fallback to stored status if calculation fails

### Supported Hours Formats

#### 1. Standard Format
```
Monday: 9:00 AM - 10:00 PM
Tuesday: 9:00 AM - 10:00 PM
Wednesday: 9:00 AM - 10:00 PM
```

#### 2. Compact Format
```
Mon 9AM-10PM, Tue 9AM-10PM, Wed 9AM-10PM
```

#### 3. 24-Hour Format
```
Daily: 24 hours
24 hours
Open 24 hours
```

#### 4. Range Format
```
Mon-Fri 9AM-5PM
```

#### 5. Military Time
```
Monday 9:00-22:00
```

### Timezone Mapping

The system maps US states to their primary timezones:

| State | Timezone |
|-------|----------|
| NY, FL, PA, OH, GA, NC, MI, NJ, VA, IN, MA, MD, KY, CT, SC, WV, NH, ME, RI, DE, VT | America/New_York |
| CA, WA, OR, NV | America/Los_Angeles |
| TX, IL, TN, MO, MN, WI, LA, AL, IA, OK, AR, MS, KS, NE, SD, ND | America/Chicago |
| CO, AZ, UT, NM, ID, MT, WY | America/Denver |
| HI | Pacific/Honolulu |
| AK | America/Anchorage |

### Status Response Format

```json
{
  "is_open": true,
  "status": "open",
  "next_open_time": "2025-07-31T09:00:00-04:00",
  "current_time_local": "2025-07-31T01:43:10.421564-04:00",
  "timezone": "America/New_York",
  "hours_parsed": true,
  "status_reason": "Currently open"
}
```

**Fields**:
- `is_open`: Boolean indicating if restaurant is currently open
- `status`: String ("open", "closed", "unknown")
- `next_open_time`: ISO datetime of next opening (if closed)
- `current_time_local`: Current time in restaurant's timezone
- `timezone`: Restaurant's timezone
- `hours_parsed`: Whether business hours were successfully parsed
- `status_reason`: Human-readable explanation of status

## Usage Examples

### Basic Status Check
```python
from utils.restaurant_status import get_restaurant_status

restaurant_data = {
    'name': 'Test Restaurant',
    'hours_open': 'Monday: 9:00 AM - 10:00 PM',
    'city': 'New York',
    'state': 'NY'
}

status = get_restaurant_status(restaurant_data)
print(f"Restaurant is {'open' if status['is_open'] else 'closed'}")
```

### Database Integration
```python
# The database manager automatically calculates status
restaurants = db_manager.get_all_places()
for restaurant in restaurants:
    print(f"{restaurant['name']}: {restaurant['status']}")
```

## Testing

### Test Script
**Location**: `backend/test_status_calculation.py`

**Test Scenarios**:
1. Standard business hours
2. Compact format hours
3. 24-hour restaurants
4. Overnight hours
5. Weekdays only
6. Missing hours data
7. Invalid hours format

### Running Tests
```bash
cd backend
source ../venv311/bin/activate
python test_status_calculation.py
```

## Error Handling

### Graceful Degradation
- Falls back to stored status if calculation fails
- Returns "unknown" status for unparseable hours
- Logs errors for debugging
- Continues operation even with calculation errors

### Common Error Scenarios
1. **Invalid hours format**: Returns "unknown" status
2. **Missing timezone data**: Uses UTC as fallback
3. **Parsing errors**: Logs error and continues
4. **Import errors**: Uses fallback functions

## Performance Considerations

### Caching
- 5-minute cache TTL for repeated calculations
- Reduces computational overhead
- Maintains accuracy for reasonable time periods

### Database Impact
- No additional database queries
- Calculates status in memory
- Minimal impact on existing queries

### Memory Usage
- Lightweight calculation
- No persistent memory storage
- Efficient regex patterns

## Configuration

### Dependencies
Added to `requirements.txt`:
```
pytz==2023.3
python-dateutil==2.8.2
```

### Environment Variables
No additional environment variables required. Uses existing configuration.

## Migration Notes

### Database Changes
- No schema changes required
- Existing `status` field remains for fallback
- New fields added to response (not stored)

### Backward Compatibility
- Existing API responses remain compatible
- Fallback to stored status if calculation fails
- No breaking changes to existing functionality

## Future Enhancements

### Potential Improvements
1. **Geocoding Integration**: Use coordinates for precise timezone detection
2. **Holiday Support**: Account for holidays and special hours
3. **Seasonal Hours**: Handle seasonal business hour changes
4. **Real-time Updates**: WebSocket updates for status changes
5. **Advanced Parsing**: Support for more complex hours formats

### Performance Optimizations
1. **Redis Caching**: Distributed caching for high-traffic scenarios
2. **Background Calculation**: Pre-calculate status for popular restaurants
3. **Batch Processing**: Optimize for multiple restaurant queries

## Monitoring and Logging

### Log Levels
- **INFO**: Successful status calculations
- **WARNING**: Timezone detection issues
- **ERROR**: Parsing failures and calculation errors

### Key Metrics
- Status calculation success rate
- Hours parsing success rate
- Timezone detection accuracy
- Performance timing

## Troubleshooting

### Common Issues

#### 1. Status Always Shows "Unknown"
- Check if hours data is in supported format
- Verify timezone mapping for restaurant location
- Review error logs for parsing issues

#### 2. Incorrect Timezone
- Verify state abbreviation in restaurant data
- Check timezone mapping table
- Consider adding custom timezone logic

#### 3. Performance Issues
- Monitor cache hit rates
- Check for excessive regex processing
- Review calculation frequency

### Debug Mode
Enable detailed logging by setting log level to DEBUG in configuration.

## Conclusion

The dynamic restaurant status implementation provides a robust, timezone-aware solution for determining restaurant availability in real-time. The system is designed to be:

- **Reliable**: Graceful error handling and fallbacks
- **Performant**: Efficient calculation and caching
- **Flexible**: Support for various hours formats
- **Maintainable**: Clear code structure and documentation

This implementation satisfies the user requirement that restaurant status be calculated dynamically rather than stored in the database, while providing comprehensive timezone support and robust error handling. 