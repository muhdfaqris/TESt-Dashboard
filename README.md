# TESt Dashboard

## Overview

TESt Dashboard is a comprehensive maintenance management and equipment tracking system designed for industrial operations. It provides real-time monitoring, analytics, and management of equipment maintenance activities, work orders, and staff performance to optimize operational efficiency and minimize downtime.

## Features

### 🏭 Core Functionality
- **Multi-page Dashboard Interface** with intuitive navigation between Overview, Data Records, Staff, and Settings
- **Real-time KPI Monitoring** including work order volumes, completion rates, MTTR, and activity durations
- **Interactive Data Visualizations** using Plotly charts for trends, distributions, and comparative analysis
- **Comprehensive Maintenance Tracking** with detailed work order lifecycle management
- **Equipment Performance Analytics** with station/machine-specific breakdown analysis
- **Staff Activity Monitoring** with vendor and personnel tracking
- **LOTO (Lock Out Tag Out) Compliance** tracking for safety procedures

### 📊 Analytics & Reporting
- **Key Performance Indicators**: Track completion rates, work order volumes, MTTR, and activity durations
- **Visual Analytics**: Interactive pie charts, bar charts, and trend analysis
- **Station/Machine Performance**: Top 10 analysis by work order volume
- **Time-based Trends**: Weekly and monthly trend analysis
- **Status Distribution**: Work order status breakdown by type
- **Comparative Analysis**: Period-over-period performance comparisons

### 🛠️ Technical Features
- **SQLite Database Integration** with comprehensive maintenance data schema (25+ fields)
- **Advanced Filtering System** for targeted data analysis and reporting
- **Automated Data Preprocessing** with validation and type conversion
- **Responsive UI Design** with modern Streamlit components and custom styling
- **Performance Optimization** using caching for database operations and calculations

## Technology Stack

- **Frontend Framework**: Streamlit (Python web application framework)
- **Database**: SQLite with structured maintenance data schema
- **Data Processing**: Pandas for data manipulation and analysis
- **Visualization**: Plotly for interactive charts and graphs
- **UI Components**: Streamlit-native components with custom styling

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd TESt-Dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run main.py
   ```

4. **Access the dashboard**
   Open your browser and navigate to `http://localhost:8501`

## Project Structure

```
TESt-Dashboard/
├── main.py                    # Application entry point and navigation
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── route/                     # Page-specific modules
│   ├── overview.py           # Main dashboard with analytics
│   ├── data_records.py       # Detailed data viewing interface
│   ├── staff.py              # Staff management interface
│   └── settings.py           # Configuration and settings
├── utils/                     # Utility modules
│   ├── db.py                 # Database operations and schema
│   ├── data.py               # Data preprocessing and validation
│   ├── calc.py               # KPI calculations and metrics
│   ├── filters.py            # Data filtering functionality
│   └── ui.py                 # UI helper functions
├── static/                   # Static assets (logos, images)
├── memory-bank/              # Project context and documentation
│   ├── productContext.md     # High-level project overview
│   ├── activeContext.md      # Current status and focus
│   ├── progress.md           # Progress tracking
│   ├── decisionLog.md        # Architectural decisions
│   └── systemPatterns.md     # System patterns and standards
└── database/                 # SQLite database files (auto-generated)
```

## Usage

### Dashboard Navigation

1. **Overview Page** (Default)
   - View key performance metrics and KPI cards
   - Analyze work order status distributions
   - Review weekly trends and patterns
   - Monitor top-performing stations/machines

2. **Data Records Page**
   - Browse detailed maintenance records
   - Filter and search through historical data
   - Export data for external analysis

3. **Staff Page**
   - Manage staff assignments and activities
   - Track vendor involvement and performance
   - Monitor activity completion by personnel

4. **Settings Page**
   - Configure application settings
   - Database management options
   - User preferences and customization

### Data Management

The system uses a SQLite database (`database/TESt_dashboard.db`) with the following key tables:

#### PM_data Table Schema
- **Work Order Tracking**: ID, Notification date, Work Order Status, Notification type
- **Equipment Information**: StationList, MachineList, EquipmentList, Equipment_Group
- **Maintenance Details**: Malfunction_Start_Date, Malfunction_Stop_Date, MTTR, Breakdown_Type
- **Activity Tracking**: Activity_Code, Activity, Activity_Start_Date, Activity_Stop_Date
- **Personnel**: Activity_by_1, Activity_by_Vendor, Creator_Email
- **Safety Compliance**: LOTO, LOTO_Date_Time_Start, LOTO_Date_Time_End
- **Planning**: Plan_Date_Time_Start, Plan_Date_Time_End

### Data Preprocessing

The system automatically processes incoming data with:
- **Date Format Standardization**: Convert various date formats to consistent datetime objects
- **Missing Value Handling**: Fill missing categorical data with 'Unknown'
- **Numeric Conversion**: Convert MTTR, Duration, and other metrics to numeric types
- **Data Validation**: Ensure data integrity and consistency

## API Reference

### Core Functions

#### Database Operations (`utils/db.py`)

```python
init_db() -> None
```
Initialize database and create tables if they don't exist.

**Purpose**: Set up the SQLite database schema and ensure all required tables are created.

---

```python
append_db(df: pandas.DataFrame) -> None
```
Append new data to the database, replacing existing data.

**Parameters**:
- `df` (pandas.DataFrame): DataFrame containing maintenance data to append

**Purpose**: Replace all existing data in the database with new data from the DataFrame.

---

```python
load_db() -> pandas.DataFrame
```
Load all data from the database.

**Returns**:
- `pandas.DataFrame`: DataFrame containing all maintenance records from database

**Purpose**: Retrieve all maintenance data for processing and analysis.

---

```python
total_record() -> int
```
Get total count of records in database.

**Returns**:
- `int`: Total number of maintenance records

**Purpose**: Provide quick record count for dashboard metrics.

#### Data Processing (`utils/data.py`)

```python
preprocess_data() -> pandas.DataFrame
```
Load and preprocess data from database with validation and type conversion.

**Returns**:
- `pandas.DataFrame`: Processed DataFrame ready for analysis

**Purpose**: Load raw data from database and apply necessary preprocessing steps including date conversion, missing value handling, and type standardization.

#### KPI Calculations (`utils/calc.py`)

```python
calculate_kpi(df: pandas.DataFrame) -> dict
```
Calculate key performance indicators from maintenance data.

**Parameters**:
- `df` (pandas.DataFrame): Filtered DataFrame for KPI calculation

**Returns**:
- `dict`: Dictionary containing calculated KPIs including total_orders, completion_rate, avg_mttr, avg_duration

**Purpose**: Compute essential maintenance metrics for dashboard display.

---

```python
calculate_delta(current_kpi: dict, previous_kpi: dict, as_percentage: bool = True) -> dict
```
Calculate period-over-period changes in KPIs.

**Parameters**:
- `current_kpi` (dict): Current period KPI values
- `previous_kpi` (dict): Previous period KPI values
- `as_percentage` (bool): Return results as percentage change

**Returns**:
- `dict`: Dictionary containing delta values for each KPI

**Purpose**: Provide trend analysis showing performance changes over time.

#### Filtering System (`utils/filters.py`)

```python
create_filters(df: pandas.DataFrame) -> dict
```
Create filter options based on DataFrame columns.

**Parameters**:
- `df` (pandas.DataFrame): Source DataFrame for filter creation

**Returns**:
- `dict`: Dictionary containing available filter options

**Purpose**: Generate filter interface components based on data characteristics.

---

```python
apply_filters(df: pandas.DataFrame, filters: dict) -> pandas.DataFrame
```
Apply selected filters to DataFrame.

**Parameters**:
- `df` (pandas.DataFrame): Source DataFrame to filter
- `filters` (dict): Selected filter criteria

**Returns**:
- `pandas.DataFrame`: Filtered DataFrame

**Purpose**: Reduce dataset based on user-selected criteria for focused analysis.

## Configuration

### Database Configuration
- Database file: `database/TESt_dashboard.db`
- Table name: `PM_data`
- Auto-created on first run

### Streamlit Configuration
- Page layout: Wide layout for optimal viewing
- Custom styling applied through `utils/ui.py`
- Session state management for data persistence

## Maintenance and Operations

### Data Backup
Regular backups of the `database/` directory are recommended:
```bash
cp -r database/ database_backup_$(date +%Y%m%d_%H%M%S)/
```

### Performance Monitoring
- Monitor memory usage with large datasets
- Consider data archiving for historical data older than 1 year
- Regular cleanup of temporary files and cache

### Troubleshooting

**Common Issues:**

1. **Database Connection Errors**
   - Check file permissions in `database/` directory
   - Verify SQLite installation
   - Restart the application

2. **Data Display Issues**
   - Clear Streamlit cache: `streamlit cache clear`
   - Restart the application
   - Check data format consistency

3. **Performance Issues**
   - Consider adding data indexing for large datasets
   - Implement data pagination for large result sets
   - Monitor memory usage with `@st.cache_data` decorators

## Contributing

When contributing to this project:

1. **Code Style**: Follow PEP 8 guidelines for Python code
2. **Documentation**: Update docstrings for all new functions
3. **Testing**: Add appropriate tests for new functionality
4. **Memory Bank**: Update relevant context files when making significant changes

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Review the Memory Bank files in `memory-bank/` for project context
- Check existing issues and discussions
- Create detailed bug reports with system information

---

**Last Updated**: 2025-09-28 15:19:20
**Version**: 1.0.0
**Status**: Active Development