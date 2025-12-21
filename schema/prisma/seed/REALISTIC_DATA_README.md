# Realistic Company Data Generation

This document explains the improvements made to generate realistic company data for the InfoCompanies database.

## Overview

The `generateCompany()` function has been completely overhauled to produce realistic French company data with proper geographical consistency, industry-specific characteristics, and realistic financial patterns.

## Key Improvements

### 1. Geographical Consistency

**File**: `data/reference/cityDepartmentMapping.ts`

- Created accurate mapping of French cities to their departments and regions
- Added realistic postal code patterns for each location
- Ensures companies have geographically consistent addresses

**Features**:
- 50+ major French cities with proper department numbers
- Correct postal code patterns (e.g., 75xxx for Paris, 13xxx for Marseille)
- Consistent region-department-city relationships

### 2. Realistic Company Names

**File**: `data/utils/companyGenerator.ts`

- Industry-specific company name templates
- French business naming conventions
- Mix of generic and personal names (30% use personal surnames)

**Examples**:
- Construction: "Bâtiment Plus", "Travaux Martin"
- Commerce: "Boutique Central", "Magasin Express"
- Tech: "Digital Solutions", "Tech Innovation"

### 3. Employee Numbers by Industry

**File**: `data/utils/employee.ts`

- Industry-specific employee ranges based on real French business statistics
- 70% of companies near typical size, 30% at extremes for realism
- Proper company categorization (Micro-entreprise, PME, ETI, etc.)

**Industry Examples**:
- Agriculture: 1-50 employees (typical: 8)
- Manufacturing: 5-1000 employees (typical: 50)
- IT: 1-100 employees (typical: 15)
- Public Services: 50-1000 employees (typical: 200)

### 4. Legal Forms Based on Size

Automatically assigns appropriate legal forms based on employee count:
- 1 employee → EI (Entreprise Individuelle)
- 2-10 employees → Micro-entreprise
- 11-50 employees → EURL
- 51-250 employees → SARL
- 250+ employees → SA

### 5. Realistic Financial Data

**File**: `data/utils/financial.ts`

- Industry-specific revenue ranges
- COVID-19 impact modeling for 2020-2021
- Seasonal variations in quarterly data
- Proper turnover-to-revenue ratios

**Features**:
- Revenue ranges from €30k (small arts companies) to €100M (large industry)
- 2020 decline for affected sectors (-40% to -10%)
- 2021 recovery patterns
- Quarterly seasonal fluctuations

### 6. Enhanced Business Operations

**Industry-specific schedules**:
- Retail: Often open Saturdays, some Sundays
- Restaurants: 7am-22pm, extended weekends
- Healthcare: Saturday mornings only
- Public services: Standard office hours

**Realistic reviews**:
- Industry-appropriate rating distributions
- Review counts matching business type
- Restaurants: Higher review counts, wider rating spread
- Professional services: Fewer reviews, higher ratings

### 7. Proper French Business Codes

**File**: `data/reference/industries.ts`

- Expanded APE codes with proper French NAF format (e.g., "47.11A")
- Multiple relevant codes per industry sector
- Real French business classification system

### 8. Contact Information

- Realistic French phone number formats
- Industry-appropriate email addresses
- Business-specific domain generation

## Usage

```typescript
import { generateCompany } from './data/business/companies'

// Generate a single realistic company
const company = generateCompany()

// The company will have:
// - Geographically consistent location
// - Industry-appropriate name and characteristics
// - Realistic employee count and legal form
// - Proper French business codes
// - Industry-specific financial patterns
// - Realistic contact information
```

## File Structure

```
data/
├── business/
│   └── companies.ts          # Main generation function
├── reference/
│   ├── cityDepartmentMapping.ts    # Geographic data
│   ├── industries.ts              # Industry sectors and APE codes
│   ├── legalForms.ts              # French legal forms
│   ├── regions.ts                 # French regions
│   └── cities.ts                  # City names
└── utils/
    ├── companyGenerator.ts        # Name and contact generation
    ├── employee.ts               # Employee and size logic
    ├── financial.ts              # Financial and operational data
    └── random.ts                 # Geographic selection utilities
```

## Testing

A test file is provided to verify the realistic data generation:

```bash
# Run the test (from the seed directory)
npx ts-node test-realistic-data.ts
```

This will generate 5 sample companies showing the realistic data patterns.

## Benefits

1. **Data Quality**: Much more realistic data for testing and development
2. **Geographical Accuracy**: Proper French administrative divisions
3. **Industry Realism**: Sector-appropriate characteristics
4. **Business Logic**: Consistent relationships between size, legal form, and operations
5. **Regulatory Compliance**: Proper French business identifiers and codes
6. **Temporal Accuracy**: COVID impact and seasonal patterns reflected

The generated data now closely mimics real French business directory information, making it ideal for testing applications that work with French company data.
