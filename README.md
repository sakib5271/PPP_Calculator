# PPP Calculator

A desktop application for calculating Purchasing Power Parity (PPP) equivalents between countries using the latest IMF World Economic Outlook data.

## Features

- **Cross-Country Salary Comparison**: Easily compare your salary's purchasing power in different countries.
- **User-Friendly GUI**: Built with Tkinter for a clean, intuitive interface.
- **Flexible Input**: Supports both yearly and monthly salary inputs.
- **Real-Time Calculations**: Instant PPP equivalent calculations based on official IMF data.
- **Comprehensive Country Coverage**: Includes PPP data for over 50 countries worldwide.
- **Data Transparency**: All PPP factors are sourced from the IMF and stored in an easily updatable JSON file.

## Installation

### Prerequisites

- Python 3.6 or higher
- Tkinter (usually included with Python installations)

### Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/ppp-calculator.git
   cd ppp-calculator
   ```

2. **Ensure dependencies are installed**:
   Tkinter is typically included with Python. If not, install it via your package manager:
   - On Ubuntu/Debian: `sudo apt-get install python3-tk`
   - On macOS: `brew install python-tk`
   - On Windows: Tkinter comes with Python installer

3. **Run the application**:
   ```bash
   python ppp_calculator.py
   ```

## Usage

1. **Select Source Country**: Choose your current country from the dropdown.
2. **Enter Salary**: Input your annual or monthly salary in your local currency.
3. **Select Target Country**: Choose the country you want to compare against.
4. **Calculate**: Click the "Calculate PPP Equivalent" button.
5. **View Results**: See your salary's equivalent purchasing power in the target country.

### Example

If you earn $50,000 USD annually in the United States and want to know the equivalent in BD:
- Source: United States, Salary: 50000, Yearly
- Target: Bangladesh
- Result: Approximately 2,876,500 BDT (based on current PPP rates)

## Data Source

This application uses Purchasing Power Parity (PPP) conversion rates from the International Monetary Fund (IMF) World Economic Outlook database.

- **Source**: IMF World Economic Outlook, April 2025
- **Year**: 2024 estimates
- **Data File**: `data/ppp_data.json`

### Understanding PPP

PPP measures how much one currency needs to be converted to have the same purchasing power in different countries. For example, if the PPP factor for Country A is 2.0, then $1 USD has the same purchasing power as 2.0 units of Country A's currency.

## Updating Data

To update with the latest IMF data:

1. Visit the [IMF World Economic Outlook page](https://www.imf.org/en/Publications/WEO)
2. Download the latest dataset
3. Look for the "PPPPC" column (Implied PPP conversion rate)
4. Update the `ppp_factor` values in `data/ppp_data.json`
5. Alternatively, use World Bank data from [data.worldbank.org](https://data.worldbank.org/indicator/PA.NUS.PPP)

## Project Structure

```
ppp-calculator/
├── ppp_calculator.py    # Main application file
├── data/
│   └── ppp_data.json    # PPP data and metadata
└── README.md            # This file
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- International Monetary Fund for providing the PPP data
- Python and Tkinter communities for the excellent GUI framework

## Disclaimer

This tool is for informational purposes only. PPP calculations are estimates based on available data and should not be used for financial planning without professional advice. Always verify with current economic data.
