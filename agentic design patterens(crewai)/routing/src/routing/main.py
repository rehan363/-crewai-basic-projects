from crewai.flow.flow import Flow, start, listen, router
from litellm import completion 
from typing import Optional, Dict, Any
from dotenv import load_dotenv
import os

load_dotenv()

# Configure logging


class TravelPlannerFlow(Flow):
    def __init__(self):
        super().__init__()
        self.model = "gemini/gemini-1.5-flash"
    
    @start()
    def generate_travel_plan(self) -> str:
        """Generate a travel plan and preferences based on user input and set the 
        travel type in state.
        
        Returns:
            str: The processed user input
        """
        try:
            user_input = input("Enter your travel type (business, family, friends, couple, or other): ").strip().lower()
            
            travel_types = {
                "business": ["business", "professional"],
                "family": ["family", "couple", "friends"],
            }
            
            for travel_type, keywords in travel_types.items():
                if user_input in keywords:
                    self.state["travel_type"] = travel_type
                    break
            else:
                self.state["travel_type"] = "other"
            
            print(f"Travel type set to: {self.state['travel_type']}")
            return "user_input"
            
        except Exception as e:
            print(f"Error in generate_travel_plan: {str(e)}")
            self.state["travel_type"] = "other"
            return "user_input"

    @router(generate_travel_plan)
    def route_travel(self) -> str:
        """Route the flow based on the travel type.
        
        Returns:
            str: The route name to follow
        """
        travel_type = self.state.get("travel_type", "other")
        route_map = {
            "business": "business_route",
            "family": "family_route",
            "other": "general_route"
        }
        return route_map.get(travel_type, "general_route")

    @listen("business_route")
    def suggest_business_travel(self) -> str:
        """Suggest a best business travel destination based on the user's input.
        
        Returns:
            str: AI-generated travel suggestion
        """
        print("Generating business travel suggestions...")
        try:
            response = completion(
                model=self.model,
                api_key=os.getenv("GEMINI_API_KEY"),
                messages=[{
                    "role": "system",
                    "content": "You are a knowledgeable travel assistant specializing in business travel recommendations."
                },
                {
                    "role": "user",
                    "content": f"""Please suggest a business travel destination considering:
                    - Professional networking opportunities
                    - Business infrastructure
                    - Conference and meeting facilities
                    - Transportation connectivity
                    
                    Current travel type: {self.state['travel_type']}
                    """
                }]
            )
            suggestion = response.choices[0].message.content
            print(f"Business travel suggestion generated successfully")
            print(suggestion)
            return suggestion
            
        except Exception as e:
            error_msg = f"Error generating business travel suggestion: {str(e)}"
            print(error_msg)
            return error_msg

    @listen("family_route")
    def suggest_family_travel(self) -> str:
        """Suggest a best family travel destination based on the user's input.
        
        Returns:
            str: AI-generated travel suggestion
        """
        print("Generating family travel suggestions...")
        try:
            response = completion(
                model=self.model,
                api_key=os.getenv("GEMINI_API_KEY"),
                messages=[{
                    "role": "system",
                    "content": "You are a knowledgeable travel assistant specializing in family and group travel recommendations."
                },
                {
                    "role": "user",
                    "content": f"""Please suggest a family-friendly destination considering:
                    - Family activities and attractions
                    - Safety and accommodation
                    - Child-friendly amenities
                    - Entertainment options
                    
                    Current travel type: {self.state['travel_type']}
                    """
                }]
            )
            suggestion = response.choices[0].message.content
            print("Family travel suggestion generated successfully")
            print(suggestion)
            return suggestion
            
        except Exception as e:
            error_msg = f"Error generating family travel suggestion: {str(e)}"
            print(error_msg)
            return error_msg

    @listen("general_route")
    def suggest_general_travel(self) -> str:
        """Suggest a best travel destination based on the user's input.
        
        Returns:
            str: AI-generated travel suggestion
        """
        print("Generating general travel suggestions...")
        try:
            response = completion(
                model=self.model,
                api_key=os.getenv("GEMINI_API_KEY"),
                messages=[{
                    "role": "system",
                    "content": "You are a knowledgeable travel assistant specializing in personalized travel recommendations."
                },
                {
                    "role": "user",
                    "content": f"""Please suggest a travel destination considering:
                    - Popular attractions
                    - Local culture and experiences
                    - Accommodation options
                    - Transportation accessibility
                    
                    Current travel type: {self.state['travel_type']}
                    """
                }]
            )
            suggestion = response.choices[0].message.content
            print("General travel suggestion generated successfully")
            print(suggestion)
            return suggestion
            
        except Exception as e:
            error_msg = f"Error generating general travel suggestion: {str(e)}"
            print(error_msg)
            return error_msg

def main():
    try:
        flow = TravelPlannerFlow()
        flow.kickoff()
    except Exception as e:
        print(f"Error in main execution: {str(e)}")

if __name__ == "__main__":
    main()


