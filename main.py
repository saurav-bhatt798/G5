import customtkinter as ctk
from tkinter import messagebox

# Set appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ----------- Login Window -----------
class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Login - Fitness App")
        self.geometry("400x300")

        self.label = ctk.CTkLabel(self, text="Login to Fitness App", font=("Arial", 20))
        self.label.pack(pady=20)

        self.username = ctk.CTkEntry(self, placeholder_text="Username")
        self.username.pack(pady=10)

        self.password = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password.pack(pady=10)

        self.button = ctk.CTkButton(self, text="Login", command=self.login)
        self.button.pack(pady=20)

    def login(self):
        user = self.username.get()
        pw = self.password.get()
        if user == "admin" and pw == "1234":
            self.destroy()
            app = FitnessApp(user)
            app.mainloop()
        else:
            messagebox.showerror("Error", "Invalid login credentials!")

# ----------- Main Fitness App -----------
class FitnessApp(ctk.CTk):
    def __init__(self, username):
        super().__init__()
        self.title("Fitness Goal Tracker")
        self.geometry("480x800")

        self.label = ctk.CTkLabel(self, text=f"Welcome, {username}!", font=("Arial", 20))
        self.label.pack(pady=10)

        # Gender and Age
        self.gender = ctk.CTkOptionMenu(self, values=["Male", "Female"])
        self.gender.pack(pady=10)
        self.gender.set("Male")

        self.age = ctk.CTkEntry(self, placeholder_text="Age (years)")
        self.age.pack(pady=10)

        # Height & Weight
        self.height = ctk.CTkEntry(self, placeholder_text="Height (cm)")
        self.height.pack(pady=10)

        self.weight = ctk.CTkEntry(self, placeholder_text="Weight (kg)")
        self.weight.pack(pady=10)

        # Goal Weight
        self.goal_weight = ctk.CTkEntry(self, placeholder_text="Goal Weight (kg)")
        self.goal_weight.pack(pady=10)

        # Activity level
        self.activity = ctk.CTkOptionMenu(
            self,
            values=[
                "Sedentary (little or no exercise)",
                "Lightly Active (1-3 days/week)",
                "Moderately Active (3-5 days/week)",
                "Very Active (6-7 days/week)"
            ]
        )
        self.activity.pack(pady=10)
        self.activity.set("Sedentary (little or no exercise)")

        # Buttons
        self.calc_button = ctk.CTkButton(self, text="Calculate BMR & Calories", command=self.calculate_bmr)
        self.calc_button.pack(pady=20)

        self.result_label = ctk.CTkLabel(self, text="", font=("Arial", 14))
        self.result_label.pack(pady=10)

        self.save_button = ctk.CTkButton(self, text="Save Progress", command=self.save_progress)
        self.save_button.pack(pady=10)

        # Credits (team names)
        credits = (
            "Developed by:\n"
            "🧠 Jatin Diwakar\n"
            "💪 Ayush Pathak\n"
            "🏋️ Harish Singh Mehra\n"
            "🔥 Krrish Adhikari"
        )
        self.credit_label = ctk.CTkLabel(self, text=credits, font=("Arial", 12))
        self.credit_label.pack(side="bottom", pady=15)

    def calculate_bmr(self):
        try:
            gender = self.gender.get()
            age = int(self.age.get())
            height = float(self.height.get())
            weight = float(self.weight.get())
            goal_weight = float(self.goal_weight.get())
            activity = self.activity.get()

            # Calculate BMR (Mifflin-St Jeor Formula)
            if gender == "Male":
                bmr = 88.36 + (13.4 * weight) + (4.8 * height) - (5.7 * age)
            else:
                bmr = 447.6 + (9.2 * weight) + (3.1 * height) - (4.3 * age)

            # Activity multiplier
            activity_multipliers = {
                "Sedentary (little or no exercise)": 1.2,
                "Lightly Active (1-3 days/week)": 1.375,
                "Moderately Active (3-5 days/week)": 1.55,
                "Very Active (6-7 days/week)": 1.725
            }
            maintenance_calories = bmr * activity_multipliers.get(activity, 1.2)

            # Weight difference
            weight_diff = goal_weight - weight

            if weight_diff < 0:
                goal_calories = maintenance_calories - 500
                advice = "You need a calorie deficit to lose weight."
            elif weight_diff > 0:
                goal_calories = maintenance_calories + 500
                advice = "You need a calorie surplus to gain weight."
            else:
                goal_calories = maintenance_calories
                advice = "You are already at your goal weight!"

            # BMI and Healthy Weight Range
            height_m = height / 100
            bmi = weight / (height_m ** 2)
            min_weight = 18.5 * (height_m ** 2)
            max_weight = 24.9 * (height_m ** 2)

            # BMI category
            if bmi < 18.5:
                bmi_status = "Underweight"
            elif bmi < 25:
                bmi_status = "Healthy"
            elif bmi < 30:
                bmi_status = "Overweight"
            else:
                bmi_status = "Obese"

            # Estimated weeks to reach target weight
            calorie_diff_per_day = abs(goal_calories - maintenance_calories)
            total_calorie_change = abs(weight_diff) * 7700  # total calories to burn/gain
            if calorie_diff_per_day > 0:
                weeks = total_calorie_change / (calorie_diff_per_day * 7)
                weeks_text = f"Estimated Time to Reach Goal: {weeks:.1f} weeks"
            else:
                weeks_text = "You are already at your goal weight!"

            result = (
                f"BMR: {bmr:.2f} kcal/day\n"
                f"Maintenance Calories: {maintenance_calories:.2f} kcal/day\n"
                f"Goal Calories: {goal_calories:.2f} kcal/day\n"
                f"{advice}\n\n"
                f"Current BMI: {bmi:.2f} ({bmi_status})\n"
                f"Healthy Weight Range: {min_weight:.1f} – {max_weight:.1f} kg\n"
                f"{weeks_text}"
            )

            self.result_label.configure(text=result)

        except ValueError:
            messagebox.showwarning("Input Error", "Please enter valid numeric values!")

    def save_progress(self):
        gender = self.gender.get()
        age = self.age.get()
        h = self.height.get()
        w = self.weight.get()
        g = self.goal_weight.get()
        a = self.activity.get()

        if h and w and g and a and age:
            with open("progress.txt", "a") as f:
                f.write(
                    f"Gender: {gender}, Age: {age}, Height: {h} cm, "
                    f"Weight: {w} kg, Goal Weight: {g} kg, Activity: {a}\n"
                )
            messagebox.showinfo("Saved", "Progress saved successfully!")
        else:
            messagebox.showwarning("Warning", "Please fill all fields!")

# ----------- Run the App -----------
if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()
