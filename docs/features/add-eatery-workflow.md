# Add Eatery Workflow - Complete Implementation

This document outlines the complete implementation of the enhanced "Add Eatery" workflow for the JewGo app.

## 🏗️ Architecture Overview

The Add Eatery workflow consists of:

1. **Frontend Form** (`/app/add-eatery/page.tsx`)
2. **Image Upload Component** (`/components/ImageUpload.tsx`)
3. **API Routes** (`/app/api/restaurants/`)
4. **Database Schema** (PostgreSQL)
5. **Admin Dashboard** (`/app/admin/restaurants/page.tsx`)

## 📋 Database Schema

### Required Database Changes

Run the migration script to add missing columns:

```sql
-- File: migrations/add_eatery_workflow.sql
-- Run this against your PostgreSQL database
```

### Key Tables

#### `restaurants` Table
```sql
-- Core fields (existing)
id, name, address, phone, website, kosher_category, certifying_agency

-- New fields for Add Eatery workflow
short_description TEXT,           -- Max 80 chars for mobile display
email TEXT,                       -- Contact email
google_listing_url TEXT,          -- Google Maps/GMB link
category TEXT DEFAULT 'restaurant',
status TEXT DEFAULT 'pending_approval',
is_cholov_yisroel BOOLEAN,        -- For dairy establishments
is_pas_yisroel BOOLEAN,           -- For meat/pareve establishments
hours_open TEXT,                  -- Business hours
price_range TEXT,                 -- $, $$, $$$, $$$$
image_url TEXT,                   -- Main restaurant image
```

#### `restaurant_owners` Table (Optional)
```sql
id SERIAL PRIMARY KEY,
restaurant_id INTEGER REFERENCES restaurants(id),
name TEXT NOT NULL,
email TEXT NOT NULL,
phone TEXT NOT NULL,
created_at TIMESTAMPTZ DEFAULT NOW(),
updated_at TIMESTAMPTZ DEFAULT NOW()
```

## 🎨 Frontend Implementation

### Form Features

1. **User Type Selection**
   - Owner submission (with additional contact info)
   - Community submission

2. **Image Upload**
   - Drag & drop interface
   - File validation (5MB max, image types only)
   - Preview functionality
   - Upload progress indicator

3. **Conditional Fields**
   - Dairy category → Chalav Yisrael/Chalav Stam options
   - Meat/Pareve category → Pas Yisroel options

4. **Validation**
   - Real-time field validation
   - Character count for short description
   - URL validation for links
   - Required field highlighting

### Key Components

#### ImageUpload Component
```typescript
// File: components/ImageUpload.tsx
interface ImageUploadProps {
  onImageUpload: (imageUrl: string) => void;
  currentImageUrl?: string;
  className?: string;
}
```

Features:
- File type validation
- Size validation (5MB max)
- Preview functionality
- Upload progress
- Error handling

## 🔌 API Implementation

### Main Restaurant API (`/api/restaurants`)

#### POST - Submit Restaurant
```typescript
// Endpoint: POST /api/restaurants
// Validates and stores restaurant submission

Request Body:
{
  name: string,
  short_description: string,      // Max 80 chars
  description?: string,
  certifying_agency: string,
  kosher_category: 'meat' | 'dairy' | 'pareve',
  is_cholov_yisroel?: boolean,   // Required for dairy
  is_pas_yisroel?: boolean,      // Required for meat/pareve
  phone: string,
  email?: string,
  address: string,
  website?: string,
  google_listing_url?: string,
  hours_open: string,
  price_range?: string,
  image_url: string,
  user_type: 'owner' | 'community',
  owner_info?: {
    name: string,
    email: string,
    phone: string
  }
}
```

#### GET - Fetch Restaurants
```typescript
// Endpoint: GET /api/restaurants?status=pending_approval
// Returns restaurants with optional filtering
```

### Approval/Rejection APIs

#### Approve Restaurant
```typescript
// Endpoint: PUT /api/restaurants/{id}/approve
// Approves a pending restaurant submission
```

#### Reject Restaurant
```typescript
// Endpoint: PUT /api/restaurants/{id}/reject
// Rejects a pending restaurant submission with reason
```

## 🛠️ Admin Dashboard

### Features

1. **Pending Submissions List**
   - Shows all restaurants with `status = 'pending_approval'`
   - Displays key information at a glance
   - Differentiates between owner and community submissions

2. **Submission Details Modal**
   - Full restaurant information
   - Owner contact details (if applicable)
   - Approve/Reject actions

3. **Statistics**
   - Total pending submissions
   - Owner vs community submission counts

### Access
- URL: `/admin/restaurants`
- Requires admin authentication (to be implemented)

## 🔄 Workflow Steps

### 1. User Submission
1. User navigates to `/add-eatery`
2. Selects user type (owner/community)
3. Fills out form with validation
4. Uploads restaurant image
5. Submits form
6. Receives confirmation message
7. Redirected to home page

### 2. Admin Review
1. Admin accesses `/admin/restaurants`
2. Views pending submissions
3. Clicks "View Details" for specific restaurant
4. Reviews all information
5. Approves or rejects with reason
6. Restaurant status updated in database

### 3. Post-Approval
1. Approved restaurants become visible in main app
2. Rejected restaurants remain hidden
3. Email notifications sent (to be implemented)

## 🎯 Validation Rules

### Required Fields
- Restaurant name
- Short description (max 80 chars)
- Certifying agency
- Kosher category
- Phone number
- Address
- Hours open
- Restaurant image

### Conditional Validation
- **Dairy category**: Must specify Chalav Yisrael or Chalav Stam
- **Meat/Pareve category**: Must specify Pas Yisroel status
- **Owner submission**: Must provide owner contact information

### URL Validation
- Website URL (optional)
- Google Maps URL (optional)
- Certification link URL (optional)

## 🚀 Deployment Checklist

### Database Setup
- [ ] Run migration script: `migrations/add_eatery_workflow.sql`
- [ ] Verify new columns exist
- [ ] Test database connections

### Frontend Deployment
- [ ] Deploy updated `/app/add-eatery/page.tsx`
- [ ] Deploy new `/components/ImageUpload.tsx`
- [ ] Deploy admin dashboard `/app/admin/restaurants/page.tsx`

### API Deployment
- [ ] Deploy `/app/api/restaurants/route.ts`
- [ ] Deploy `/app/api/restaurants/[id]/approve/route.ts`
- [ ] Deploy `/app/api/restaurants/[id]/reject/route.ts`

### Image Upload Setup
- [ ] Configure image upload service (S3, Supabase, Cloudinary)
- [ ] Update `ImageUpload.tsx` with actual upload logic
- [ ] Test image upload functionality

### Testing
- [ ] Test form validation
- [ ] Test image upload
- [ ] Test API endpoints
- [ ] Test admin approval workflow
- [ ] Test conditional field logic

## 🔧 Configuration

### Environment Variables
```bash
# Database
DATABASE_URL=postgresql://...

# Image Upload (choose one)
AWS_S3_BUCKET=your-bucket-name
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key

# Or Supabase
SUPABASE_URL=your-supabase-url
SUPABASE_ANON_KEY=your-anon-key

# Or Cloudinary
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

### Image Upload Configuration
Update the `ImageUpload.tsx` component to use your preferred service:

```typescript
// Example: S3 Upload
const uploadToS3 = async (file: File): Promise<string> => {
  // Implementation for S3 upload
  // Return the public URL
};

// Example: Supabase Upload
const uploadToSupabase = async (file: File): Promise<string> => {
  // Implementation for Supabase upload
  // Return the public URL
};
```

## 📱 Mobile Optimization

The form is optimized for mobile devices with:
- Responsive design
- Touch-friendly inputs
- Optimized image upload
- Character count for short descriptions
- Clear validation messages

## 🔒 Security Considerations

1. **Input Validation**: All inputs validated on both client and server
2. **File Upload Security**: File type and size validation
3. **Admin Access**: Admin routes should be protected (to be implemented)
4. **Rate Limiting**: Consider implementing rate limiting for submissions
5. **CSRF Protection**: Ensure CSRF tokens are used (Next.js handles this)

## 🚨 Error Handling

### Frontend Errors
- Form validation errors displayed inline
- Network errors with retry options
- Image upload errors with clear messages

### Backend Errors
- Validation errors returned with field-specific messages
- Database errors logged and handled gracefully
- 500 errors with user-friendly messages

## 📈 Future Enhancements

1. **Email Notifications**
   - Confirmation emails to submitters
   - Approval/rejection notifications
   - Admin notifications for new submissions

2. **Advanced Image Handling**
   - Multiple image uploads
   - Image cropping/editing
   - Automatic image optimization

3. **Enhanced Validation**
   - Address geocoding
   - Phone number formatting
   - Business hours validation

4. **Analytics**
   - Submission tracking
   - Approval rate metrics
   - User engagement data

## 📞 Support

For questions or issues with the Add Eatery workflow:
1. Check the validation rules above
2. Verify database schema matches requirements
3. Test API endpoints individually
4. Review browser console for JavaScript errors
5. Check server logs for backend errors 