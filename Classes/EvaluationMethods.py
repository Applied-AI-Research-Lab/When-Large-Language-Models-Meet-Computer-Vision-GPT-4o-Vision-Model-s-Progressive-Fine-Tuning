import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt
import os
import seaborn as sns


class EvaluationMethods:
    def __init__(self, dataset_path=''):
        self.dataset_path = dataset_path
        self.pre_path = '../Datasets/'

    def evaluate_results(self, original, prediction, model_name):
        data = pd.read_csv(self.pre_path + self.dataset_path)
        accuracy = round(accuracy_score(data[original], data[prediction]), 4)
        precision = round(precision_score(data[original], data[prediction], average='weighted'), 4)
        recall = round(recall_score(data[original], data[prediction], average='weighted'), 4)
        f1 = round(f1_score(data[original], data[prediction], average='weighted'), 4)

        # Create a DataFrame with the evaluation results including the 'model' column
        evaluation_df = pd.DataFrame({
            'Model': [model_name],
            'Accuracy': [accuracy],
            'Precision': [precision],
            'Recall': [recall],
            'F1': [f1]
        })

        # Append the results to the existing CSV file or create a new one
        evaluation_df.to_csv(self.pre_path + 'evaluation-results.csv', mode='a',
                             header=not os.path.exists(self.pre_path + 'evaluation-results.csv'), index=False)

        return {'Model': model_name, 'Accuracy': accuracy, 'Precision': precision, 'Recall': recall, 'F1': f1}

    def scatterplot(self, original_column, prediction_column):
        df = pd.read_csv(self.pre_path + self.dataset_path)
        prediction = df[prediction_column]
        original = df[original_column]

        # Calculate Mean Absolute Error
        mae = abs(original - prediction).mean()

        # Create a scatter plot with a regression line
        sns.regplot(x=original, y=prediction, scatter_kws={'alpha': 0.5})

        plt.xlabel(original_column)
        plt.ylabel(prediction_column)

        # Save the scatterplot image to the Datasets folder
        plt.savefig(os.path.join(self.pre_path + 'Plots/', prediction_column + '.png'))

        # Show the plot
        plt.show()

        return mae

    def count_matching_rows(self, original_column, prediction_column):
        df = pd.read_csv(self.pre_path + self.dataset_path)

        # Count the number of same value rows
        matching_rows = df[df[original_column] == df[prediction_column]]

        return len(matching_rows)

    def plot_histograms(self, original_column, prediction_column):
        dataframe = pd.read_csv(self.pre_path + self.dataset_path)

        # Separate predicted probabilities by class
        predicted_probabilities_class_0 = dataframe.loc[dataframe[original_column] == 0, prediction_column]
        predicted_probabilities_class_1 = dataframe.loc[dataframe[original_column] == 1, prediction_column]

        # Plot histograms
        plt.figure(figsize=(10, 5))

        # Histogram for class 0
        plt.subplot(1, 2, 1)
        plt.hist(predicted_probabilities_class_0, bins=20, color='blue', alpha=0.7)
        plt.title('Predicted Probabilities - Class 0')
        plt.xlabel('Probability')
        plt.ylabel('Frequency')

        # Histogram for class 1
        plt.subplot(1, 2, 2)
        plt.hist(predicted_probabilities_class_1, bins=20, color='orange', alpha=0.7)
        plt.title('Predicted Probabilities - Class 1')
        plt.xlabel('Probability')
        plt.ylabel('Frequency')

        plt.tight_layout()
        plt.show()

    def plot_confusion_matrix(self, original_column, prediction_column):
        dataframe = pd.read_csv(self.pre_path + self.dataset_path)

        # Extract data from DataFrame
        y_true = dataframe[original_column]
        y_pred = dataframe[prediction_column]

        cm = confusion_matrix(y_true, y_pred)
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
        plt.xlabel('Predicted')
        plt.ylabel('True')
        plt.title('Confusion Matrix \n('+prediction_column+')')
        plt.show()

    """
    Plot a stacked bar chart showing the distribution of labels across categories in two columns.

    Args:
    column1 (str): The name of the first column with string labels.
    column2 (str): The name of the second column with string labels.
    """

    def plot_stacked_bar_chart(self, original_column, prediction_column):
        data = pd.read_csv(self.pre_path + self.dataset_path)
        cross_tab = pd.crosstab(data[original_column], data[prediction_column])
        # Calculate row-wise percentages
        cross_tab_percent = cross_tab.apply(lambda x: x * 100 / x.sum(), axis=1)

        # Plotting the stacked bar chart
        ax = cross_tab_percent.plot(kind='bar', stacked=True, figsize=(10, 6))

        # Adding labels and title
        plt.title(f'Stacked Bar Chart of {original_column} vs. {prediction_column}')
        plt.xlabel(original_column)
        plt.ylabel('Percentage')
        plt.xticks(rotation=45)

        # Adding percentages as text on each bar segment
        for p in ax.patches:
            width, height = p.get_width(), p.get_height()
            x, y = p.get_xy()
            ax.annotate(f'{height:.1f}%', (x + width / 2, y + height / 2), ha='center', va='center', fontsize=8)

        plt.show()

    """
    Plot a grouped bar chart showing the relationship between labels in two columns.

    Args:
    column1 (str): The name of the first column with string labels.
    column2 (str): The name of the second column with string labels.
    """
    def plot_grouped_bar_chart(self, original_column, prediction_column):
        data = pd.read_csv(self.pre_path + self.dataset_path)
        pivot_table = data.groupby([original_column, prediction_column]).size().unstack(fill_value=0)
        pivot_table.plot(kind='bar', figsize=(10, 6))
        plt.title(f'Relationship between {original_column} and {prediction_column}')
        plt.xlabel(original_column)
        plt.ylabel('Count')
        plt.xticks(rotation=45)
        plt.show()

    """
    Plot a heatmap showing relationships and patterns between label categories in two columns.

    Args:
    column1 (str): The name of the first column with string labels.
    column2 (str): The name of the second column with string labels.
    """
    def plot_heatmap(self, original_column, prediction_column):
        data = pd.read_csv(self.pre_path + self.dataset_path)
        cross_tab = pd.crosstab(data[original_column], data[prediction_column])
        plt.figure(figsize=(10, 8))
        sns.heatmap(cross_tab, annot=True, fmt='d', cmap='YlGnBu')
        plt.title(f'Heatmap of {original_column} vs. {prediction_column}')
        plt.xlabel(prediction_column)
        plt.ylabel(original_column)
        plt.show()


# Example Usage
# Instantiate the DatasetMethods class by providing the (dataset_path)
# EVM = EvaluationMethods(dataset_path='../Datasets/test_set.csv')
# EVM = EvaluationMethods(dataset_path='../ResNet/Datasets/test_set_100_with_predictions.csv')
# EVM = EvaluationMethods(dataset_path='../ResNet/Datasets/test_set_200_with_predictions.csv')
# EVM = EvaluationMethods(dataset_path='../ResNet/Datasets/test_set_400_with_predictions.csv')

# # Count correct predictions
# print(str(EVM.count_matching_rows('Category', 'GPT-4o-Resolution-400')))

# # Evaluate the predictions made by each model
# print(f'GPT-4o-Resolution-400: ' + str(EVM.evaluate_results('Category', 'GPT-4o-Resolution-400', 'GPT-4o-Resolution-400')))
# print(f'GPT-4o-mini-Resolution-400: ' + str(EVM.evaluate_results('Category', 'GPT-4o-mini-Resolution-400', 'GPT-4o-mini-Resolution-400')))
# print(f'Phase-1-Resolution-400: ' + str(EVM.evaluate_results('Category', 'Phase-1-Resolution-400', 'Phase-1-Resolution-400')))
# print(f'Phase-2-Resolution-400: ' + str(EVM.evaluate_results('Category', 'Phase-2-Resolution-400', 'Phase-2-Resolution-400')))
# print(f'Phase-3-Resolution-400: ' + str(EVM.evaluate_results('Category', 'Phase-3-Resolution-400', 'Phase-3-Resolution-400')))
# print(f'Phase-4-Resolution-400: ' + str(EVM.evaluate_results('Category', 'Phase-4-Resolution-400', 'Phase-4-Resolution-400')))
# print(f'ResNet50-400-Predictions: ' + str(EVM.evaluate_results('Category', 'ResNet50-Predictions', 'ResNet50-Predictions')))

# print(f'GPT-4o-Resolution-200: ' + str(EVM.evaluate_results('Category', 'GPT-4o-Resolution-200', 'GPT-4o-Resolution-200')))
# print(f'GPT-4o-mini-Resolution-200: ' + str(EVM.evaluate_results('Category', 'GPT-4o-mini-Resolution-200', 'GPT-4o-mini-Resolution-200')))
# print(f'Phase-1-Resolution-200: ' + str(EVM.evaluate_results('Category', 'Phase-1-Resolution-200', 'Phase-1-Resolution-200')))
# print(f'Phase-2-Resolution-200: ' + str(EVM.evaluate_results('Category', 'Phase-2-Resolution-200', 'Phase-2-Resolution-200')))
# print(f'Phase-3-Resolution-200: ' + str(EVM.evaluate_results('Category', 'Phase-3-Resolution-200', 'Phase-3-Resolution-200')))
# print(f'Phase-4-Resolution-200: ' + str(EVM.evaluate_results('Category', 'Phase-4-Resolution-200', 'Phase-4-Resolution-200')))
# print(f'ResNet50-200-Predictions: ' + str(EVM.evaluate_results('Category', 'ResNet50-Predictions', 'ResNet50-Predictions')))

# print(f'GPT-4o-Resolution-100: ' + str(EVM.evaluate_results('Category', 'GPT-4o-Resolution-100', 'GPT-4o-Resolution-100')))
# print(f'GPT-4o-mini-Resolution-100: ' + str(EVM.evaluate_results('Category', 'GPT-4o-mini-Resolution-100', 'GPT-4o-mini-Resolution-100')))
# print(f'Phase-1-Resolution-100: ' + str(EVM.evaluate_results('Category', 'Phase-1-Resolution-100', 'Phase-1-Resolution-100')))
# print(f'Phase-2-Resolution-100: ' + str(EVM.evaluate_results('Category', 'Phase-2-Resolution-100', 'Phase-2-Resolution-100')))
# print(f'Phase-3-Resolution-100: ' + str(EVM.evaluate_results('Category', 'Phase-3-Resolution-100', 'Phase-3-Resolution-100')))
# print(f'Phase-4-Resolution-100: ' + str(EVM.evaluate_results('Category', 'Phase-4-Resolution-100', 'Phase-4-Resolution-100')))
# print(f'ResNet50-100-Predictions: ' + str(EVM.evaluate_results('Category', 'ResNet50-Predictions', 'ResNet50-Predictions')))

# print(f'Low-to-Higher-Trained-100-Prediction-400: ' + str(EVM.evaluate_results('Category', 'Low-to-Higher-Trained-100-Prediction-400', 'Low-to-Higher-Trained-100-Prediction-400')))
# print(f'Low-to-Higher-Trained-200-Prediction-400: ' + str(EVM.evaluate_results('Category', 'Low-to-Higher-Trained-200-Prediction-400', 'Low-to-Higher-Trained-200-Prediction-400')))

# print(f'High-to-Lower-Trained-200-Prediction-100: ' + str(EVM.evaluate_results('Category', 'High-to-Lower-Trained-200-Prediction-100', 'High-to-Lower-Trained-200-Prediction-100')))
# print(f'High-to-Lower-Trained-400-Prediction-100: ' + str(EVM.evaluate_results('Category', 'High-to-Lower-Trained-400-Prediction-100', 'High-to-Lower-Trained-400-Prediction-100')))

# Create scatterplots
# print(EVM.scatterplot(original_column='Spam', prediction_column='gpt_bm_prediction'))
# print(EVM.scatterplot(original_column='Spam', prediction_column='gpt_ft_prediction'))
# print(EVM.scatterplot(original_column='Spam', prediction_column='roberta_ft_adamw'))
# print(EVM.scatterplot(original_column='Spam', prediction_column='roberta_ft_adam'))

# Create histograms
# EVM.plot_histograms(original_column='Spam', prediction_column='gpt_bm_prediction')

# Create confusion matrix
# EVM.plot_confusion_matrix(original_column='Spam', prediction_column='gpt_bm_prediction')
# EVM.plot_confusion_matrix(original_column='Spam', prediction_column='gpt_ft_prediction')
# EVM.plot_confusion_matrix(original_column='Spam', prediction_column='roberta_ft_adamw')
# EVM.plot_confusion_matrix(original_column='Spam', prediction_column='roberta_ft_adam')

# Plot a stacked bar chart showing the distribution of labels across categories in two columns
# print(EVM.plot_stacked_bar_chart(original_column='sentiment', prediction_column='gpt_bm_prediction'))
# print(EVM.plot_stacked_bar_chart(original_column='sentiment', prediction_column='gpt_ft_prediction'))
# print(EVM.plot_stacked_bar_chart(original_column='sentiment', prediction_column='bert__adamw_ft_prediction'))
# print(EVM.plot_stacked_bar_chart(original_column='sentiment', prediction_column='bert__adam_ft_prediction'))

# Plot a grouped bar chart showing the relationship between labels in two columns
# print(EVM.plot_grouped_bar_chart(original_column='sentiment', prediction_column='gpt_bm_prediction'))
# print(EVM.plot_grouped_bar_chart(original_column='sentiment', prediction_column='gpt_ft_prediction'))
# print(EVM.plot_grouped_bar_chart(original_column='sentiment', prediction_column='bert__adamw_ft_prediction'))
# print(EVM.plot_grouped_bar_chart(original_column='sentiment', prediction_column='bert__adam_ft_prediction'))

# Plot a heatmap showing relationships and patterns between label categories in two columns
# print(EVM.plot_heatmap(original_column='sentiment', prediction_column='gpt_bm_prediction'))
# print(EVM.plot_grouped_bar_chart(original_column='sentiment', prediction_column='gpt_ft_prediction'))
# print(EVM.plot_grouped_bar_chart(original_column='sentiment', prediction_column='bert__adamw_ft_prediction'))
# print(EVM.plot_grouped_bar_chart(original_column='sentiment', prediction_column='bert__adam_ft_prediction'))



