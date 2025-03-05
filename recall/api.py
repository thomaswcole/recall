import requests
from datetime import datetime

class NHTSA:
    BASE_URL = "https://api.nhtsa.gov"

    def __init__(self):
        self.results = []

    def fetch_data(self, campaign_number=None, make=None, model=None, year=None):
        if campaign_number:
            endpoint = "recalls/campaignNumber"
            params = {'campaignNumber': campaign_number}
        else:
            endpoint = "recalls/recallsByVehicle"
            params = {}
            if make:
                params['make'] = make
            if model:
                params['model'] = model
            if year:
                params['modelYear'] = year
            
            if not params:
                raise ValueError("At least one of 'make', 'model', or 'year' must be provided.")
        
        url = f"{self.BASE_URL}/{endpoint}"
        self.results = self._make_request(url, params)

    def _make_request(self, url, params):
        try:
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json().get("results", [])
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return []
        except Exception as err:
            print(f"An error occurred: {err}")
            return []
    
    def get_unique_field_values(self, field):
        """
        Retrieve a list of unique values for the given field from the API results.
        """
        return list({entry.get(field) for entry in self.results if entry.get(field)})
    
    def get_model_years(self):
        return self.get_unique_field_values("ModelYear")
    
    def get_models(self):
        return self.get_unique_field_values("Model")
    
    def get_makes(self):
        return self.get_unique_field_values("Make")
    
    def get_manufacturers(self):
        return self.get_unique_field_values("Manufacturer")
    
    def get_affected_units(self):
        return self.get_unique_field_values("PotentialNumberofUnitsAffected")

    def get_report_dates(self):
        """
        Get unique report dates from the API results, parsed as datetime objects.
        """
        date_list = []
        for entry in self.results:
            date_str = entry.get("ReportReceivedDate")
            if date_str:
                try:
                    date_obj = datetime.strptime(date_str, "%d/%m/%Y").date()
                    date_list.append(date_obj)
                except ValueError:
                    print(f"Date format error in entry: {entry}")
        return list(set(date_list))
    
    def get_all_model_years(self):
        """Fetch all model years available in the NHTSA database."""
        url = f"{self.BASE_URL}/products/vehicle/modelYears?issueType=r"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return [year["modelYear"] for year in response.json().get("results", [])]
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return []
        except Exception as err:
            print(f"An error occurred: {err}")
            return []

    def get_all_makes(self, model_year):
        """Fetch all makes for a specific model year."""
        url = f"{self.BASE_URL}/products/vehicle/makes?modelYear={model_year}&issueType=r"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return [make["make"] for make in response.json().get("results", [])]
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return []
        except Exception as err:
            print(f"An error occurred: {err}")
            return []

    def get_all_models(self, model_year, make):
        """Fetch all models for a specific model year and make."""
        url = f"{self.BASE_URL}/products/vehicle/models?modelYear={model_year}&make={make}&issueType=r"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return [model["model"] for model in response.json().get("results", [])]
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return []
        except Exception as err:
            print(f"An error occurred: {err}")
            return []
    def __str__(self):
        """
        String representation of the recall data, showing relevant fields.
        """
        if not self.results:
            return "No data available."

        summary = (
            f"Units Affected: {', '.join(self.get_affected_units())}\n"
            f"Manufacturers: {', '.join(self.get_manufacturers())}\n"
            f"Models: {', '.join(self.get_models())}\n"
            f"Makes: {', '.join(self.get_makes())}\n"
            f"Model Years: {', '.join(map(str, self.get_model_years()))}\n"
            f"Report Dates: {', '.join(map(str, self.get_report_dates()))}"
        )
        return summary