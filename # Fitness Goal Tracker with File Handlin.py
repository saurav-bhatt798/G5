# Fitness Goal Tracker with File Handling

# Get gender first
gender = input("Enter your gender (M/F): ").lower()
if gender == 'm':
    gender_text = "Male"
elif gender == 'f':
    gender_text = "Female"
else:
    print("Invalid input for gender. Defaulting to 'Male'.")
    gender = 'm'
    gender_text = "Male"

# Then get the name
name = input("Enter your name: ")

# Get other user inputs
weight = float(input("Enter your current weight (kg): "))
height = float(input("Enter your height (m): "))
age = int(input("Enter your age (years): "))
goal_weight = float(input("Enter your goal weight (kg): "))
weeks = int(input("Enter number of weeks to reach goal: "))

print("\nSelect your activity level:")
print("1. Sedentary (little or no exercise)")
print("2. Lightly active (light exercise 1-3 days/week)")
print("3. Moderately active (moderate exercise 3-5 days/week)")
print("4. Very active (hard exercise 6-7 days/week)")
print("5. Extra active (very hard exercise or physical job)")
choice = int(input("Enter choice (1-5): "))

activity_multipliers = [1.2, 1.375, 1.55, 1.725, 1.9]
activity_multiplier = activity_multipliers[choice - 1]

# Calculate BMI
bmi = weight / (height ** 2)
goal_bmi = goal_weight / (height ** 2)

# BMI category function
def bmi_category(bmi_value):
    if bmi_value < 18.5:
        return "Underweight"
    elif bmi_value < 25:
        return "Healthy"
    elif bmi_value < 30:
        return "Overweight"
    else:
        return "Obese"

current_category = bmi_category(bmi)
goal_category = bmi_category(goal_bmi)

# Calculate BMR
if gender == 'm':
    bmr = 88.362 + (13.397 * weight) + (4.799 * (height * 100)) - (5.677 * age)
else:
    bmr = 447.593 + (9.247 * weight) + (3.098 * (height * 100)) - (4.330 * age)

# Maintenance calories
maintenance_calories = bmr * activity_multiplier

# Calculate goal calories based on weight change
calories_per_kg = 7700  # 1 kg fat ≈ 7700 calories
weight_diff = goal_weight - weight
daily_adjustment = (weight_diff * calories_per_kg) / (weeks * 7)
goal_calories = maintenance_calories + daily_adjustment  # add if gain, subtract if loss

# Output
print(f"\nHello {name}, you are currently {current_category} according to the BMI calculator.")
print(f"Your goal is to change {abs(weight_diff):.1f} kg in {weeks} weeks "
      f"({abs(weight_diff) / weeks:.2f} kg/week).")
print(f"Based on your activity level (multiplier {activity_multiplier:.3f}):")
print(f"To reach your goal weight, you should consume about {goal_calories:.0f} calories/day.")

if goal_category != "Healthy":
    print(f"\nHowever, your goal weight still keeps you in the {goal_category} category.")
    print("Try adjusting your goal to fall within a healthy BMI range (18.5–24.9).")
else:
    print("\nNow your goal BMI is in the healthy category according to the BMI range.")

# Healthy weight range
min_healthy_weight = 18.5 * height**2
max_healthy_weight = 24.9 * height**2
print(f"\nHealthy weight range for your height: {min_healthy_weight:.1f} – {max_healthy_weight:.1f} kg")

# Check if goal weight is inside healthy range
if min_healthy_weight <= goal_weight <= max_healthy_weight:
    print("Your goal weight is within the healthy range. Great choice!")
else:
    print("Your goal weight is outside the healthy range. Consider adjusting it for optimal health.")

# --- File handling ---
with open("fitness_tracker.txt", "w") as file:
    file.write(f"\n--- Fitness Report for {name} ---\n")
    file.write(f"Gender: {gender_text}\n")
    file.write(f"Current weight: {weight} kg\n")
    file.write(f"Height: {height} m\n")
    file.write(f"Goal weight: {goal_weight} kg\n")
    file.write(f"Activity multiplier: {activity_multiplier}\n")
    file.write(f"Maintenance calories/day: {maintenance_calories:.0f}\n")
    file.write(f"Goal calories/day: {goal_calories:.0f}\n")
    file.write(f"Current BMI: {bmi:.2f} ({current_category})\n")
    file.write(f"Goal BMI: {goal_bmi:.2f} ({goal_category})\n")
    file.write(f"Healthy weight range: {min_healthy_weight:.1f} – {max_healthy_weight:.1f} kg\n")
    if min_healthy_weight <= goal_weight <= max_healthy_weight:
        file.write("Goal weight is within the healthy range.\n")
    else:
        file.write("Goal weight is outside the healthy range.\n")
    file.write("-----------------------------\n")

print("\nYour progress has been saved to 'fitness_tracker.txt'.")
