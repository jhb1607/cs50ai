import csv
import sys
import datetime



from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4



def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )
    
    # Train model and make predictions
    model = train_model(X_train, y_train)        
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    with open(filename) as file:
        reader = csv.reader(file)

        # Skip header row
        next(reader)
        evidence = list()
        labels = list()
        
        for row in reader:
            current_evidence = []
            try:
                current_evidence.append(int(row[0]))
                current_evidence.append(float(row[1]))
                current_evidence.append(int(row[2]))
                current_evidence.append(float(row[3]))
                current_evidence.append(int(row[4]))
                for i in range(5, 10):
                    current_evidence.append(float(row[i]))   
                current_evidence.append(month_to_number(row[10]))
                for j in range(11, 15):
                    current_evidence.append(int(row[j]))
                if row[15] == "Returning_Visitor":
                    current_evidence.append(1)
                else:
                    current_evidence.append(0)
                if row[16] == "TRUE":
                    current_evidence.append(1)
                else:
                    current_evidence.append(0)
            except ValueError:
                print("Data doesn't fit required data type")
            
            evidence.append(current_evidence)
            if row[17] == "TRUE":
                labels.append(1)
            else:
                labels.append(0)
        
        # It all didn't work because in the csv file what should have been called "Jun" was called "June" fml.
        i = 0
        for current in evidence:
            for x in current:
                if not (isinstance(x, float) or isinstance(x, int)):
                    print(x)
                    print(current)
                    print(i)
            i += 1

      
            
        return (evidence, labels)   
        

def month_to_number(month):
    if month == "June":
        return 5 
    try:
        date_object = datetime.datetime.strptime(month, "%b")
        return date_object.month - 1
    except ValueError:
        return None


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    
    return model
    

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    # The actual number of positive and negative labels in labels.
    neg_labels = 0
    pos_labels = 0
    for label in labels:
        if label == 0:
            neg_labels += 1
        else: 
            pos_labels += 1
    # The number of actual positive and negative labels that were accurately identified in predictions.
    accurately_identified_neg = 0
    accurately_identified_pos = 0
    for actual, predicted in zip(labels, predictions):
        if actual == predicted == 0:
            accurately_identified_neg += 1
        elif actual == predicted == 1:
            accurately_identified_pos += 1
    
    sensitivity =  accurately_identified_pos / pos_labels
    specificity = accurately_identified_neg / neg_labels
        
    return (sensitivity, specificity)
    


if __name__ == "__main__":
    main()
