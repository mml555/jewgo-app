#!/usr/bin/env node

/**
 * JewGo Test Data Seeding Script
 * Creates dummy data for testing and development
 */

const https = require('https');

// Sample restaurant data
const sampleRestaurants = [
  {
    business_id: 'test_restaurant_1',
    name: 'Kosher Delight',
    address: '123 Main St, New York, NY 10001',
    city: 'New York',
    state: 'NY',
    postal_code: '10001',
    latitude: 40.7505,
    longitude: -73.9934,
    stars: 4.5,
    review_count: 127,
    categories: 'Kosher,Delis,Jewish',
    hours: {
      Monday: '8:0-20:0',
      Tuesday: '8:0-20:0',
      Wednesday: '8:0-20:0',
      Thursday: '8:0-20:0',
      Friday: '8:0-18:0',
      Saturday: 'Closed',
      Sunday: '9:0-19:0'
    },
    attributes: {
      'BusinessAcceptsCreditCards': true,
      'RestaurantsDelivery': true,
      'RestaurantsTakeOut': true,
      'WheelchairAccessible': true
    }
  },
  {
    business_id: 'test_restaurant_2',
    name: 'Shalom Kitchen',
    address: '456 Oak Ave, Brooklyn, NY 11201',
    city: 'Brooklyn',
    state: 'NY',
    postal_code: '11201',
    latitude: 40.7021,
    longitude: -73.9872,
    stars: 4.2,
    review_count: 89,
    categories: 'Kosher,Restaurants,Jewish',
    hours: {
      Monday: '11:0-22:0',
      Tuesday: '11:0-22:0',
      Wednesday: '11:0-22:0',
      Thursday: '11:0-22:0',
      Friday: '11:0-17:0',
      Saturday: 'Closed',
      Sunday: '12:0-21:0'
    },
    attributes: {
      'BusinessAcceptsCreditCards': true,
      'RestaurantsDelivery': true,
      'RestaurantsTakeOut': true,
      'OutdoorSeating': true
    }
  },
  {
    business_id: 'test_restaurant_3',
    name: 'Mazel Tov Bistro',
    address: '789 Pine St, Queens, NY 11375',
    city: 'Queens',
    state: 'NY',
    postal_code: '11375',
    latitude: 40.7282,
    longitude: -73.7949,
    stars: 4.8,
    review_count: 203,
    categories: 'Kosher,Restaurants,Jewish,Mediterranean',
    hours: {
      Monday: '10:0-23:0',
      Tuesday: '10:0-23:0',
      Wednesday: '10:0-23:0',
      Thursday: '10:0-23:0',
      Friday: '10:0-16:0',
      Saturday: 'Closed',
      Sunday: '11:0-22:0'
    },
    attributes: {
      'BusinessAcceptsCreditCards': true,
      'RestaurantsDelivery': true,
      'RestaurantsTakeOut': true,
      'GoodForKids': true,
      'WiFi': 'free'
    }
  },
  {
    business_id: 'test_restaurant_4',
    name: 'Challah House',
    address: '321 Maple Dr, Bronx, NY 10451',
    city: 'Bronx',
    state: 'NY',
    postal_code: '10451',
    latitude: 40.8448,
    longitude: -73.8648,
    stars: 4.0,
    review_count: 67,
    categories: 'Kosher,Bakeries,Jewish',
    hours: {
      Monday: '6:0-19:0',
      Tuesday: '6:0-19:0',
      Wednesday: '6:0-19:0',
      Thursday: '6:0-19:0',
      Friday: '6:0-15:0',
      Saturday: 'Closed',
      Sunday: '7:0-18:0'
    },
    attributes: {
      'BusinessAcceptsCreditCards': true,
      'RestaurantsTakeOut': true,
      'GoodForKids': true
    }
  },
  {
    business_id: 'test_restaurant_5',
    name: 'Kiddush Corner',
    address: '654 Elm St, Staten Island, NY 10301',
    city: 'Staten Island',
    state: 'NY',
    postal_code: '10301',
    latitude: 40.5795,
    longitude: -74.1502,
    stars: 4.6,
    review_count: 145,
    categories: 'Kosher,Restaurants,Jewish,American',
    hours: {
      Monday: '11:0-21:0',
      Tuesday: '11:0-21:0',
      Wednesday: '11:0-21:0',
      Thursday: '11:0-21:0',
      Friday: '11:0-16:0',
      Saturday: 'Closed',
      Sunday: '12:0-20:0'
    },
    attributes: {
      'BusinessAcceptsCreditCards': true,
      'RestaurantsDelivery': true,
      'RestaurantsTakeOut': true,
      'OutdoorSeating': true,
      'WiFi': 'free'
    }
  }
];

// Sample review data
const sampleReviews = [
  {
    review_id: 'test_review_1',
    business_id: 'test_restaurant_1',
    user_id: 'test_user_1',
    stars: 5,
    useful: 12,
    funny: 3,
    cool: 8,
    text: 'Amazing kosher deli! The pastrami sandwich was incredible and the service was friendly. Highly recommend!',
    date: '2024-01-15'
  },
  {
    review_id: 'test_review_2',
    business_id: 'test_restaurant_1',
    user_id: 'test_user_2',
    stars: 4,
    useful: 8,
    funny: 1,
    cool: 5,
    text: 'Great food and atmosphere. The matzo ball soup was perfect for a cold day.',
    date: '2024-01-10'
  },
  {
    review_id: 'test_review_3',
    business_id: 'test_restaurant_2',
    user_id: 'test_user_3',
    stars: 4,
    useful: 15,
    funny: 2,
    cool: 10,
    text: 'Excellent kosher restaurant with authentic Jewish cuisine. The brisket was tender and flavorful.',
    date: '2024-01-12'
  },
  {
    review_id: 'test_review_4',
    business_id: 'test_restaurant_3',
    user_id: 'test_user_4',
    stars: 5,
    useful: 20,
    funny: 5,
    cool: 15,
    text: 'Best kosher restaurant in Queens! The falafel is amazing and the hummus is to die for.',
    date: '2024-01-08'
  },
  {
    review_id: 'test_review_5',
    business_id: 'test_restaurant_4',
    user_id: 'test_user_5',
    stars: 4,
    useful: 6,
    funny: 0,
    cool: 4,
    text: 'Fresh challah bread every day! The bakery items are delicious and reasonably priced.',
    date: '2024-01-14'
  }
];

// Function to make HTTP requests
function makeRequest(url, method = 'GET', data = null) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: new URL(url).hostname,
      port: 443,
      path: new URL(url).pathname,
      method: method,
      headers: {
        'Content-Type': 'application/json',
      }
    };

    if (data) {
      const postData = JSON.stringify(data);
      options.headers['Content-Length'] = Buffer.byteLength(postData);
    }

    const req = https.request(options, (res) => {
      let responseData = '';
      res.on('data', chunk => responseData += chunk);
      res.on('end', () => {
        try {
          const parsed = JSON.parse(responseData);
          resolve({ status: res.statusCode, data: parsed });
        } catch (e) {
          resolve({ status: res.statusCode, data: responseData });
        }
      });
    });

    req.on('error', reject);

    if (data) {
      req.write(JSON.stringify(data));
    }
    req.end();
  });
}

// Seed restaurants
async function seedRestaurants() {
  console.log('🌱 Seeding restaurants...');
  
  for (const restaurant of sampleRestaurants) {
    try {
      const response = await makeRequest(
        'https://jewgo.onrender.com/api/restaurants',
        'POST',
        restaurant
      );
      
      if (response.status === 201 || response.status === 200) {
        console.log(`✅ Added restaurant: ${restaurant.name}`);
      } else {
        console.log(`⚠️  Failed to add restaurant: ${restaurant.name} (Status: ${response.status})`);
      }
    } catch (error) {
      console.log(`❌ Error adding restaurant ${restaurant.name}:`, error.message);
    }
  }
}

// Seed reviews
async function seedReviews() {
  console.log('🌱 Seeding reviews...');
  
  for (const review of sampleReviews) {
    try {
      const response = await makeRequest(
        `https://jewgo.onrender.com/api/restaurants/${review.business_id}/reviews`,
        'POST',
        review
      );
      
      if (response.status === 201 || response.status === 200) {
        console.log(`✅ Added review for: ${review.business_id}`);
      } else {
        console.log(`⚠️  Failed to add review for: ${review.business_id} (Status: ${response.status})`);
      }
    } catch (error) {
      console.log(`❌ Error adding review for ${review.business_id}:`, error.message);
    }
  }
}

// Verify seeding
async function verifySeeding() {
  console.log('🔍 Verifying seeded data...');
  
  try {
    const response = await makeRequest('https://jewgo.onrender.com/api/restaurants');
    
    if (response.status === 200) {
      const restaurants = response.data;
      console.log(`✅ Found ${restaurants.length} restaurants in database`);
      
      // Check if our test restaurants are there
      const testRestaurants = restaurants.filter(r => r.business_id.startsWith('test_'));
      console.log(`✅ Found ${testRestaurants.length} test restaurants`);
      
      return testRestaurants.length > 0;
    } else {
      console.log(`⚠️  Could not verify data (Status: ${response.status})`);
      return false;
    }
  } catch (error) {
    console.log('❌ Error verifying data:', error.message);
    return false;
  }
}

// Main execution
async function main() {
  console.log('🚀 JewGo Test Data Seeding\n');
  
  try {
    // Seed restaurants first
    await seedRestaurants();
    
    // Wait a bit for restaurants to be processed
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Seed reviews
    await seedReviews();
    
    // Wait a bit for reviews to be processed
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Verify the seeding worked
    const success = await verifySeeding();
    
    if (success) {
      console.log('\n✅ Test data seeding completed successfully!');
      console.log('\nYou can now run tests with realistic data.');
    } else {
      console.log('\n⚠️  Seeding completed but verification failed.');
      console.log('Check your backend logs for any errors.');
    }
    
  } catch (error) {
    console.error('❌ Seeding failed:', error);
    process.exit(1);
  }
}

// Run seeding
main(); 