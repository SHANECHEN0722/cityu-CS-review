import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

np.random.seed(59790558) # for reproducibility
majors = ['Computer Science', 'Mathematics', 'Physics']
genders = ['Male', 'Female']

student_data = {
    'Student ID': range(1, 501),
    'Major': np.random.choice(majors, 500, p=[0.4, 0.3, 0.3]),
    'Gender': np.random.choice(genders, 500),
    'GPA': np.clip(np.random.normal(loc=3.2, scale=0.5, size=500), 0.0, 4.0)
}
students = pd.DataFrame(student_data)

plt.figure(figsize=(10, 6))
sns.countplot(x='Major', data=students, order=students['Major'].value_counts().index)
plt.title('Distribution of Students by Major')
plt.xlabel('Major')
plt.ylabel('Count')
plt.savefig('q4_2_by_major_bar.png')
plt.show()
plt.figure(figsize=(8, 8))
major_counts = students['Major'].value_counts()
plt.pie(major_counts, labels=major_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('Distribution of Students by Major')
plt.ylabel('')
plt.savefig('q4_2_by_major_pie.png')
plt.show()

plt.figure(figsize=(10, 6))
sns.countplot(x='Gender', data=students, order=students['Gender'].value_counts().index)
plt.title('Distribution of Students by Gender')
plt.xlabel('Gender')
plt.ylabel('Count')
plt.savefig('q4_2_by_gender_bar.png')
plt.show()

plt.figure(figsize=(8, 8))
gender_counts = students['Gender'].value_counts()
plt.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('Distribution of Students by Gender')
plt.ylabel('') 
plt.savefig('q4_2_by_gender_pie.png')
plt.show()

plt.figure(figsize=(10, 6))
sns.histplot(students['GPA'], bins=20, kde=True)
plt.title('Distribution of Students by GPA')
plt.xlabel('GPA')
plt.ylabel('Frequency')
plt.savefig('q4_2_by_gpa_histogram.png')
plt.show()

plt.figure(figsize=(10, 6))
sns.boxplot(x='Major', y='GPA', data=students)
plt.title('GPA_vs_Major')
plt.xlabel('Major')
plt.ylabel('GPA')
plt.savefig('q4_GPA_vs_Major.png')
plt.show()

plt.figure(figsize=(10, 6))
sns.boxplot(x='Gender', y='GPA', data=students)
plt.title('GPA_vs_Gender')
plt.xlabel('Gender')
plt.ylabel('GPA')
plt.savefig('q4_GPA_vs_Gender.png')
plt.show()

plt.figure(figsize=(12, 7))
sns.countplot(x='Major', hue='Gender', data=students)
plt.title('Major_vs_Gender')
plt.xlabel('Major')
plt.ylabel('Count')
plt.legend(title='Gender')
plt.savefig('q4_Major_vs_Gender.png')
plt.show()

major_gender_crosstab = pd.crosstab(students['Major'], students['Gender'])
plt.figure(figsize=(10, 7))
sns.heatmap(major_gender_crosstab, annot=True, fmt='d', cmap='YlGnBu')
plt.title('Major_vs_Gender Heatmap')
plt.xlabel('Gender')
plt.ylabel('Major')
plt.savefig('q4_Major_vs_Gender_heatmap.png')
plt.show()

plt.figure(figsize=(10, 6))
labels = sns.countplot(x='Major', data=students, order=students['Major'].value_counts().index)
for count in labels.containers:
    labels.bar_label(count, fmt='%d', label_type='edge', padding=3)
plt.title('Compute the number of students in each major')
plt.xlabel('Major')
plt.ylabel('Count')
plt.savefig('q4_3_by_major_bar.png')
plt.show()
def softmax(x):
    e_x = np.exp(x - np.max(x, axis=1, keepdims=True))
    return e_x / e_x.sum(axis=1, keepdims=True)

d = 8
U = np.random.rand(5, d)
V = np.random.rand(5, d)
similarity_matrix = softmax(np.dot(U, V.T) / np.sqrt(d))

plt.figure(figsize=(10, 8))
sns.heatmap(similarity_matrix, annot=True, cmap='viridis', fmt=".2f")
plt.title('U V Correlation Heatmap')
plt.xlabel('Item')
plt.ylabel('User')
plt.savefig('q4_similarity_heatmap.png')
plt.show()