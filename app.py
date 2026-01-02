from preprocessing import load_and_preprocess_data
from stress_index import calculate_stress_index

def main():
    # Step 1: Load and preprocess data
    df = load_and_preprocess_data()

    # Step 2: Calculate stress index and risk
    df = calculate_stress_index(df)

    # Step 3: Display output in terminal
    print("\nFinal Smart City Analysis Output:\n")
    print(df)

if __name__ == "__main__":
    main()
