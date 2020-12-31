# Picture Calculator
Sille Habakukk, Ilmar Uduste

## Idea
Create a script that, when given an input of a picture, could recognize mathematical operations from the picture, then calculate the whole thing and print out the final result.

This project was made in the 2020/2021 Autumn semester for a course on Artificial Intelligence (LTAT.01.003) in the University of Tartu.

## Stages of Operation
<ol>
    <li>Train an AI that could recognize numbers and basic math symbols in a picture.</li>
        <ol>
            <li>The dataset for pictures of numbers should be MNIST.</li>
            <li>TODO: We should get a dataset for basic math symbols.</li>
            <li>Try out different neural networks, RandomForestClassifiers etc.</li>
            <li>Save the model file.</li>
        </ol>
    <li>Import the trained model into the main Python script.</li>
    <li>Ask the user to import a picture containing numbers and math symbols into the main Python script via GUI.</li>
    <li>Find & classify the numbers/math symbols in the picture (AI and OpenCV).</li>
    <li>Convert the numbers and symbols into a python mathematical operation.</li>
    <li>Print the mathematical operation </li>
</ol>

# Data Preparation

To build an AI that recognizes numbers and basic math symbols, we used a dataset from Kaggle by the name of [Handwritten math symbols dataset](https://www.kaggle.com/xainano/handwrittenmathsymbols). This dataset consists of jpg files (45x45 pixels) of all numbers and different math symbols. 

Since we are doing operations with only basic symbols and numbers, we used the following categories of pictures from the dataset:

- Subtraction operator **-**
- Factorial **!**
- Parentheses **()**
- Decimal Separator **,**
- Addition Operator **+**
- Equals Operator **=**
- Numbers **0 - 9**
- Variables **a, b and c**
- Division Operator **:** (mostly with a line between the two dots) or **/**
- Logarithmic Operator **log**
- **Pi**
- Sinus Operator **sin**
- Cosinus Operator **cos**
- Tangent Operator **tan**
- Multiplication Operator **x**
- Variables **x, y and z**

It also turned out from [a forum post on Kaggle](https://www.kaggle.com/xainano/handwrittenmathsymbols/discussion/85277) that the dataset contained many duplicates (up to 80%!). So we used a script from the same post to delete the duplicates and therefore clean the data. The training data, the data cleaning script and the log of the script can be found in the 'dev' branch of this project.