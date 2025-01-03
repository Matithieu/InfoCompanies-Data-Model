# Adding Autocomplete Functionality

This guide explains how to implement an autocomplete feature based on company data stored in the database. The process involves extracting unique values, indexing them, and integrating the data into the API and frontend.

---

## Step 1: Export Data from the Database

To extract the required data for autocomplete:

1. **Export Unique Values to Populate the Database:**
    - Open the `db.sh` file.
    - Locate the `export_all_unique_values` function.
    - Add your line of code to extract distinct values for the fields you want to include in autocomplete.

    ```bash
    # Example: Extracting unique company names
    export_all_unique_values() {
        export_unique_values "SELECT DISTINCT region AS value FROM public.companies" "./InfoCompanies-Data-Model/region.csv"
    }
    ```

2. **Export Subsets for E2E Testing:**
    - In the same file, locate the `export_e2e_sub_data` function.
    - Add your line of code to extract a subset of data for end-to-end (E2E) tests.

    ```bash
    # Example: Exporting a subset of company names for testing
    export_e2e_sub_data() {
        export_unique_values "SELECT DISTINCT region AS value FROM public.companies" "$output_directory/e2e_region" "sql"
    }
    ```

---

## Step 2: Index the Data

To create an index for the autocomplete feature:

1. Navigate to the **Autocomplete Indexes** section of the `db.sh` script.
2. Add your index creation statement.

    ```bash
    # Example: Create index for company names
    create_indexes "region" "name"
    ```

---

## Step 3: Transfer the CSV to the Database

1. Locate the **Transfer Additional CSVs** section in the `db.sh` file.
2. Add your line to transfer the CSV file into the database.

    ```bash
    # Example: Load unique company names into the autocomplete table
    transfer_additional_csvs() {
        transfer_csv_to_database "region" "./InfoCompanies-Data-Model/region.csv" "name" ","
    }
    ```

---

## Step 4: Integrate into the API

1. **Model:**
    - Define a new entity or modify an existing one to support autocomplete data.

    ```java
    @Setter
    @Getter
    @Entity
    public class Region {

        @Id
        @GeneratedValue(strategy = GenerationType.IDENTITY)
        private Long id;

        private String name;
    }
    ```

2. **Repository:**
    - Add methods for querying autocomplete data.

    ```java
    public interface RegionRepository extends JpaRepository<Region, Long> {

        @Query("SELECT c FROM Region c " +
                "WHERE LOWER(c.name) " +
                "LIKE LOWER(CONCAT('%', :query, '%')) " +
                "ORDER BY c.name " +
                "ASC LIMIT 25")
        List<Region> findByNameContainingIgnoreCase(String query);
    }
    ```

3. **Service:**
    - Implement business logic for autocomplete.

    ```java
   @Service
    public class RegionService {

        @Autowired
        private RegionRepository regionRepository;

        public List<Region> searchRegions(String query) {
            return regionRepository.findByNameContainingIgnoreCase(query);
        }
    }
    ```

4. **Controller:**
    - Expose an API endpoint for the frontend to fetch autocomplete suggestions.

    ```java
    // Example: http://localhost:8080/api/v1/autocomplete/region?query=New
    @GetMapping("/region")
    public List<Region> autocompleteRegion(@RequestParam String query) {
        return regionService.searchRegions(query);
    }
    ```

---

## Step 5: Frontend Integration

Follow these steps to integrate the autocomplete API with the frontend:

### 1. Create or Update the Component
- Add functionality to call the autocomplete API.
- Ensure the component dynamically fetches suggestions based on user input.

### 2. Update Required Functions and Hooks

#### a. **`getFilterComponents`**
- Add your Autocomplete configuration or logic to this function.

#### b. **`useCompanyFilterStore`**
- Integrate your Autocomplete value into the store for state management.

#### c. **`fetchAutoComplete`**
- Add your API endpoint to the relevant type or case in this function.

#### d. **`constructURLWithFilter`**
- Implement the logic to handle Autocomplete values in this hook to construct API calls dynamically.

---

By following these steps, you will successfully implement an autocomplete feature that dynamically suggests values based on data stored in your database.

